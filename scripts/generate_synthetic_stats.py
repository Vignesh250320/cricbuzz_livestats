"""Populate synthetic matches and performance data to ensure all SQL practice queries return rows.

Creates a Legends Championship series between two teams across multiple quarters,
adds batting & bowling performances, and refreshes aggregate stats.
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "cb_user",
    "password": "vicky@123",
    "database": "cricbuzz_livestats",
}

TEAM_DETAILS = [
    {"name": "Mumbai Legends", "country": "India"},
    {"name": "Delhi Dynamos", "country": "India"},
]

VENUE_DETAILS = {
    "venue_name": "Legends Arena",
    "city": "Mumbai",
    "country": "India",
    "capacity": 55000,
}

SERIES_DETAILS = {
    "series_name": "Legends Championship",
    "host_country": "India",
    "match_type": "Mixed",
}

# Quarter anchor dates from 2023 Q1 through 2025 Q2 (10 quarters -> satisfies 6+ requirement)
QUARTER_DATES = [
    date(2023, 1, 15),
    date(2023, 4, 15),
    date(2023, 7, 15),
    date(2023, 10, 15),
    date(2024, 1, 15),
    date(2024, 4, 15),
    date(2024, 7, 15),
    date(2024, 10, 15),
    date(2025, 1, 15),
    date(2025, 4, 15),
]

MATCH_FORMATS = ["ODI", "T20I", "Test"]
MATCHES_PER_QUARTER = 3


def with_connection(fn):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(**DB_CONFIG)
        try:
            result = fn(conn, *args, **kwargs)
            conn.commit()
            return result
        finally:
            conn.close()

    return wrapper


def get_team(cursor, name: str, country: str) -> int:
    cursor.execute("SELECT team_id FROM Teams WHERE team_name=%s", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO Teams (team_name, country, total_wins, total_losses, total_matches) VALUES (%s, %s, 0, 0, 0)",
        (name, country),
    )
    return cursor.lastrowid


def get_venue(cursor) -> int:
    cursor.execute("SELECT venue_id FROM Venues WHERE venue_name=%s", (VENUE_DETAILS["venue_name"],))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO Venues (venue_name, city, country, capacity) VALUES (%s, %s, %s, %s)",
        (
            VENUE_DETAILS["venue_name"],
            VENUE_DETAILS["city"],
            VENUE_DETAILS["country"],
            VENUE_DETAILS["capacity"],
        ),
    )
    return cursor.lastrowid


def get_series(cursor) -> int:
    cursor.execute("SELECT series_id FROM Series WHERE series_name=%s", (SERIES_DETAILS["series_name"],))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO Series (series_name, host_country, match_type, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
        (
            SERIES_DETAILS["series_name"],
            SERIES_DETAILS["host_country"],
            SERIES_DETAILS["match_type"],
            QUARTER_DATES[0],
            QUARTER_DATES[-1],
        ),
    )
    return cursor.lastrowid


def ensure_players(cursor, team_name: str, count: int = 11) -> list[int]:
    player_ids: list[int] = []
    for idx in range(1, count + 1):
        full_name = f"{team_name} Player {idx}"
        cursor.execute("SELECT player_id FROM Players WHERE full_name=%s", (full_name,))
        row = cursor.fetchone()
        if row:
            player_ids.append(row[0])
            continue
        cursor.execute(
            """
            INSERT INTO Players (full_name, country, playing_role, batting_style, bowling_style, total_runs, total_wickets, total_matches, batting_average, bowling_average, strike_rate, economy_rate)
            VALUES (%s, %s, %s, %s, %s, 0, 0, 0, 0, 0, 0, 0)
            """,
            (
                full_name,
                "India",
                "All-rounder" if idx % 5 == 0 else ("Bowler" if idx % 3 == 0 else "Batsman"),
                "Right-hand bat",
                "Right-arm medium",
            ),
        )
        player_ids.append(cursor.lastrowid)
    return player_ids


def quarter_label(match_date: date) -> str:
    quarter = (match_date.month - 1) // 3 + 1
    return f"Q{quarter} {match_date.year}"


def insert_match(cursor, match_date: date, team1_id: int, team2_id: int, venue_id: int, series_id: int, idx: int, match_number: int) -> int:
    description = f"Legends Championship {quarter_label(match_date)} - Match {match_number + 1}"
    cursor.execute(
        "SELECT match_id FROM Matches WHERE match_description=%s AND match_date=%s AND team1_id=%s AND team2_id=%s",
        (description, match_date, team1_id, team2_id),
    )
    row = cursor.fetchone()
    if row:
        return row[0]

    match_format = MATCH_FORMATS[idx % len(MATCH_FORMATS)]
    victory_type = "runs" if idx % 2 == 0 else "wickets"
    victory_margin = f"{45 + (idx + match_number) * 3} {victory_type}"
    winning_team_id = team1_id if idx % 2 == 0 else team2_id
    toss_winner_id = team1_id if idx % 3 == 0 else team2_id
    toss_decision = "bat" if (idx + match_number) % 2 == 0 else "field"

    cursor.execute(
        """
        INSERT INTO Matches (
            match_description, team1_id, team2_id, venue_id, match_date, match_format,
            winning_team_id, victory_margin, victory_type, toss_winner_id, toss_decision,
            match_status, series_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            description,
            team1_id,
            team2_id,
            venue_id,
            match_date,
            match_format,
            winning_team_id,
            victory_margin,
            victory_type,
            toss_winner_id,
            toss_decision,
            "Completed",
            series_id,
        ),
    )
    return cursor.lastrowid


def insert_batting(cursor, match_id: int, innings_id: int, player_ids: list[int], base_runs: int) -> None:
    cursor.execute(
        "SELECT 1 FROM Batting_Performance WHERE match_id=%s AND innings_id=%s LIMIT 1",
        (match_id, innings_id),
    )
    if cursor.fetchone():
        return

    for pos, player_id in enumerate(player_ids[:6], start=1):
        runs = base_runs + pos * 9
        balls = runs + 8
        strike_rate = round((runs / balls) * 100, 2)
        fours = runs // 10
        sixes = max(0, runs // 20)
        cursor.execute(
            """
            INSERT INTO Batting_Performance (player_id, match_id, innings_id, runs, balls_faced, fours, sixes, strike_rate, batting_position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                player_id,
                match_id,
                innings_id,
                runs,
                balls,
                fours,
                sixes,
                Decimal(strike_rate),
                pos,
            ),
        )


def insert_bowling(cursor, match_id: int, innings_id: int, player_ids: list[int], base_overs: float) -> None:
    cursor.execute(
        "SELECT 1 FROM Bowling_Performance WHERE match_id=%s AND innings_id=%s LIMIT 1",
        (match_id, innings_id),
    )
    if cursor.fetchone():
        return

    for idx, player_id in enumerate(player_ids[:5]):
        overs = base_overs + idx * 0.6
        runs_conceded = int((overs * 5.5) + (idx * 4))
        wickets = 2 + (idx % 3)
        economy = round(runs_conceded / (overs if overs else 1), 2)
        cursor.execute(
            """
            INSERT INTO Bowling_Performance (player_id, match_id, innings_id, overs, wickets, runs_conceded, economy_rate, maidens)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                player_id,
                match_id,
                innings_id,
                Decimal(str(round(overs, 1))),
                wickets,
                runs_conceded,
                Decimal(str(economy)),
                0,
            ),
        )


def refresh_player_totals(cursor) -> None:
    cursor.execute(
        """
        UPDATE Players p
        SET total_runs = (
                SELECT COALESCE(SUM(runs), 0)
                FROM Batting_Performance bp
                WHERE bp.player_id = p.player_id
            ),
            total_matches = (
                SELECT COALESCE(COUNT(DISTINCT match_id), 0)
                FROM Batting_Performance bp
                WHERE bp.player_id = p.player_id
            ),
            batting_average = (
                SELECT COALESCE(AVG(runs), 0)
                FROM Batting_Performance bp
                WHERE bp.player_id = p.player_id
            ),
            strike_rate = (
                SELECT COALESCE(AVG(strike_rate), 0)
                FROM Batting_Performance bp
                WHERE bp.player_id = p.player_id
            ),
            total_wickets = (
                SELECT COALESCE(SUM(wickets), 0)
                FROM Bowling_Performance bl
                WHERE bl.player_id = p.player_id
            ),
            economy_rate = (
                SELECT COALESCE(AVG(economy_rate), 0)
                FROM Bowling_Performance bl
                WHERE bl.player_id = p.player_id
            )
        """
    )


def refresh_team_totals(cursor) -> None:
    cursor.execute(
        """
        UPDATE Teams t
        SET total_wins = (
                SELECT COALESCE(COUNT(*), 0)
                FROM Matches m
                WHERE m.winning_team_id = t.team_id
            ),
            total_losses = (
                SELECT COALESCE(COUNT(*), 0)
                FROM Matches m
                WHERE (m.team1_id = t.team_id OR m.team2_id = t.team_id) AND m.winning_team_id <> t.team_id
            ),
            total_matches = (
                SELECT COALESCE(COUNT(*), 0)
                FROM Matches m
                WHERE m.team1_id = t.team_id OR m.team2_id = t.team_id
            )
        """
    )


def boost_allrounders(cursor, players_map: dict[str, list[int]]) -> None:
    # Pick first two players from each team and boost cumulative stats to exceed thresholds for advanced queries
    player_ids = [players[0] for players in players_map.values()] + [players[1] for players in players_map.values()]
    for player_id in player_ids:
        cursor.execute(
            """
            UPDATE Players
            SET total_runs = GREATEST(total_runs, 2500),
                total_wickets = GREATEST(total_wickets, 120),
                batting_average = GREATEST(batting_average, 58),
                bowling_average = LEAST(COALESCE(bowling_average, 35), 22),
                strike_rate = GREATEST(strike_rate, 145),
                economy_rate = LEAST(COALESCE(economy_rate, 8), 5.8)
            WHERE player_id = %s
            """,
            (player_id,),
        )


def populate():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    team_ids = [get_team(cursor, team["name"], team["country"]) for team in TEAM_DETAILS]
    players_map = {
        team["name"]: ensure_players(cursor, team["name"])
        for team in TEAM_DETAILS
    }
    venue_id = get_venue(cursor)
    series_id = get_series(cursor)

    for idx, base_date in enumerate(QUARTER_DATES):
        for match_number in range(MATCHES_PER_QUARTER):
            match_date = base_date + timedelta(days=match_number * 6)
            match_id = insert_match(
                cursor,
                match_date,
                team_ids[0],
                team_ids[1],
                venue_id,
                series_id,
                idx,
                match_number,
            )
            base_runs_team1 = 80 + idx * 12 + match_number * 9
            base_runs_team2 = 74 + idx * 11 + match_number * 8
            insert_batting(cursor, match_id, 1, players_map[TEAM_DETAILS[0]["name"]], base_runs_team1)
            insert_bowling(cursor, match_id, 1, players_map[TEAM_DETAILS[1]["name"]], 6 + (idx % 3) + match_number)
            insert_batting(cursor, match_id, 2, players_map[TEAM_DETAILS[1]["name"]], base_runs_team2)
            insert_bowling(cursor, match_id, 2, players_map[TEAM_DETAILS[0]["name"]], 6 + ((idx + 1) % 3) + match_number)

    refresh_player_totals(cursor)
    refresh_team_totals(cursor)
    boost_allrounders(cursor, players_map)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    populate()
    print("✅ Synthetic performance data generated.")
