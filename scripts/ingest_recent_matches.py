"""Fetch recent matches from Cricbuzz API and insert into MySQL database.
Run: python scripts/ingest_recent_matches.py
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Any, Dict, List

import mysql.connector
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")

if not RAPIDAPI_KEY:
    print("❌ RAPIDAPI_KEY not set in .env")
    sys.exit(1)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "cb_user"),
    "password": os.getenv("DB_PASSWORD", "vicky@123"),
    "database": os.getenv("DB_NAME", "cricbuzz_livestats"),
}

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
}


def api_get(path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    url = f"https://{RAPIDAPI_HOST}/{path.lstrip('/')}"
    response = requests.get(url, headers=HEADERS, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


ALLOWED_FORMATS = {"Test": "Test", "ODI": "ODI", "T20": "T20I", "T20I": "T20I"}
ALLOWED_STATUSES = {
    "upcoming": "Scheduled",
    "scheduled": "Scheduled",
    "live": "Live",
    "inprogress": "Live",
    "result": "Completed",
    "completed": "Completed",
    "abandoned": "Abandoned",
    "washout": "Abandoned",
}


def normalize_format(fmt: str | None) -> str:
    if not fmt:
        return "T20I"
    fmt_upper = fmt.upper()
    return ALLOWED_FORMATS.get(fmt_upper, "T20I")


def normalize_status(status: str | None) -> str:
    if not status:
        return "Scheduled"
    key = status.strip().lower()
    # Handle statuses like "Stumps Day 1", "Match drawn"
    for token, mapped in ALLOWED_STATUSES.items():
        if token in key:
            return mapped
    return "Completed" if "result" in key or "won" in key else "Scheduled"


def parse_matches(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    matches: List[Dict[str, Any]] = []
    for type_match in data.get("typeMatches", []):
        for series_match in type_match.get("seriesMatches", []):
            series_data = series_match.get("seriesAdWrapper") or series_match.get("series", {})
            series_id = series_data.get("seriesId") or series_data.get("id")
            series_name = series_data.get("seriesName") or series_data.get("name")
            host_country = series_data.get("hostCountry") or "Unknown"

            for match_obj in series_data.get("matches", []):
                info = match_obj.get("matchInfo") or match_obj.get("match", {})
                match_id = info.get("matchId") or info.get("id")
                if not match_id:
                    continue

                match_desc = info.get("matchDesc") or info.get("description") or "Match"
                match_format = normalize_format(info.get("matchFormat") or info.get("format"))
                start_date = info.get("startDate")
                try:
                    if start_date and len(str(start_date)) > 10:
                        start_dt = datetime.fromtimestamp(int(start_date) / 1000)
                    elif start_date:
                        start_dt = datetime.fromtimestamp(int(start_date))
                    else:
                        start_dt = datetime.utcnow()
                except Exception:
                    start_dt = datetime.utcnow()

                status = normalize_status(info.get("status") or info.get("state"))

                team1_info = info.get("team1") or {}
                team2_info = info.get("team2") or {}
                team1 = team1_info.get("teamName") or info.get("team1Name") or "Team 1"
                team2 = team2_info.get("teamName") or info.get("team2Name") or "Team 2"

                venue_info = info.get("venueInfo") or info.get("venue") or {}
                venue_name = venue_info.get("ground") or venue_info.get("name") or "Unknown Venue"
                venue_city = venue_info.get("city") or "Unknown"

                matches.append(
                    {
                        "series_id": series_id,
                        "series_name": series_name,
                        "host_country": host_country,
                        "match_id": match_id,
                        "match_desc": match_desc,
                        "match_format": match_format,
                        "match_date": start_dt.date(),
                        "match_status": status,
                        "team1": team1,
                        "team2": team2,
                        "venue": venue_name,
                        "city": venue_city,
                    }
                )
    return matches


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def ensure_team(cursor, name: str):
    cursor.execute("SELECT team_id FROM Teams WHERE team_name=%s", (name,))
    if cursor.fetchone():
        return
    cursor.execute(
        "INSERT INTO Teams (team_name, country, total_wins, total_losses, total_matches) VALUES (%s, %s, 0, 0, 0)",
        (name, name),
    )


def ensure_venue(cursor, venue: str, city: str):
    cursor.execute("SELECT venue_id FROM Venues WHERE venue_name=%s", (venue,))
    if cursor.fetchone():
        return
    cursor.execute(
        "INSERT INTO Venues (venue_name, city, country, capacity) VALUES (%s, %s, %s, %s)",
        (venue, city, "Unknown", 50000),
    )


def ensure_series(cursor, series_id: int, name: str, host_country: str):
    if not series_id:
        return
    cursor.execute("SELECT series_id FROM Series WHERE series_id=%s", (series_id,))
    if cursor.fetchone():
        return
    cursor.execute(
        "INSERT INTO Series (series_id, series_name, host_country, match_type, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)",
        (series_id, name, host_country, "Mixed", datetime.utcnow().date(), datetime.utcnow().date()),
    )


def insert_matches(matches: List[Dict[str, Any]]):
    if not matches:
        print("No matches to insert.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0

    for match in matches:
        ensure_team(cursor, match["team1"])
        ensure_team(cursor, match["team2"])
        ensure_venue(cursor, match["venue"], match["city"])
        ensure_series(cursor, match["series_id"], match["series_name"], match["host_country"])

        cursor.execute("SELECT venue_id FROM Venues WHERE venue_name=%s", (match["venue"],))
        venue_id_row = cursor.fetchone()
        venue_id = venue_id_row[0] if venue_id_row else None

        cursor.execute("SELECT team_id FROM Teams WHERE team_name=%s", (match["team1"],))
        team1_id = cursor.fetchone()[0]
        cursor.execute("SELECT team_id FROM Teams WHERE team_name=%s", (match["team2"],))
        team2_id = cursor.fetchone()[0]

        cursor.execute("SELECT match_id FROM Matches WHERE match_id=%s", (match["match_id"],))
        if cursor.fetchone():
            continue

        match_status = match["match_status"] if match["match_status"] in {"Scheduled", "Live", "Completed", "Abandoned"} else "Scheduled"

        try:
            cursor.execute(
                """
                INSERT INTO Matches (match_id, series_id, team1_id, team2_id, venue_id, match_date,
                                     match_format, match_status, match_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    match["match_id"],
                    match["series_id"],
                    team1_id,
                    team2_id,
                    venue_id,
                    match["match_date"],
                    match["match_format"],
                    match_status,
                    match["match_desc"],
                ),
            )
            inserted += 1
        except mysql.connector.Error as exc:
            print(f"⚠️ Skipping match {match['match_id']} ({match['match_desc']}) due to DB error: {exc}")
            conn.rollback()
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {inserted} new matches.")


def main():
    try:
        recent_data = api_get("matches/v1/recent")
        upcoming_data = api_get("matches/v1/upcoming")
        live_data = api_get("matches/v1/live")
    except Exception as exc:
        print(f"❌ API request failed: {exc}")
        sys.exit(1)

    matches = parse_matches(recent_data) + parse_matches(upcoming_data) + parse_matches(live_data)
    unique_matches = {m["match_id"]: m for m in matches}.values()
    print(f"Fetched {len(matches)} matches ({len(unique_matches)} unique).")
    insert_matches(list(unique_matches))


if __name__ == "__main__":
    main()
