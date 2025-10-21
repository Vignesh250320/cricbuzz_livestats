# utils/api_handler.py
import requests
import logging
from utils.db_connection import run_query  # make sure you have this file!

# ==============================
# CONFIG
# ==============================
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": "43bc69bce7msh1632751028a1f4bp15ac1bjsn919b824c4267",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ==============================
# FETCH LIVE MATCHES
# ==============================
def get_live_matches():
    """Fetch list of currently live matches"""
    url = f"{BASE_URL}/matches/v1/live"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        data = res.json()
        matches = []
        for category in data.get("typeMatches", []):
            for series in category.get("seriesMatches", []):
                series_data = series.get("seriesAdWrapper", {})
                series_name = series_data.get("seriesName", "")
                for match in series_data.get("matches", []):
                    info = match.get("matchInfo", {})
                    matches.append({
                        "id": info.get("matchId"),
                        "series": series_name,
                        "team1": info.get("team1", {}).get("teamName"),
                        "team2": info.get("team2", {}).get("teamName"),
                        "status": info.get("status", "Unknown")
                    })
        return matches
    except Exception as e:
        logging.error(f"Error fetching live matches: {e}")
        return []


# ==============================
# FETCH SCORECARD
# ==============================
def get_match_scorecard(match_id: str):
    """Fetch scorecard details for a specific match"""
    url = f"{BASE_URL}/mcenter/v1/{match_id}/hscard"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        logging.error(f"Error fetching scorecard for match {match_id}: {e}")
        return None


# ==============================
# LOAD PLAYERS INTO DATABASE
# ==============================
def load_players_into_db():
    """
    Example: Load a set of international players from Cricbuzz API into DB.
    This is a demo — real Cricbuzz API does not expose full player lists openly,
    so this populates mock data from live matches instead.
    """
    logging.info("Loading players from Cricbuzz live data...")
    matches = get_live_matches()
    if not matches:
        logging.warning("No live matches found — cannot load players.")
        return 0

    inserted = 0
    for match in matches[:5]:  # limit to a few to avoid overloading
        match_data = get_match_scorecard(match["id"])
        if not match_data:
            continue

        innings = match_data.get("innings", [])
        for inn in innings:
            # collect batsmen and bowlers
            for bat in inn.get("batsmen", []):
                player_id = bat.get("id") or bat.get("playerId") or None
                name = bat.get("name", "")
                runs = bat.get("runs", 0)
                avg = bat.get("average", 0)
                query = """
                INSERT OR IGNORE INTO Players (player_id, name, country, total_runs, batting_average)
                VALUES (?, ?, ?, ?, ?)
                """
                run_query(query, (player_id, name, "Unknown", runs, avg))
                inserted += 1

            for bowl in inn.get("bowlers", []):
                player_id = bowl.get("id") or bowl.get("playerId") or None
                name = bowl.get("name", "")
                wkts = bowl.get("wickets", 0)
                econ = bowl.get("econ", 0)
                avg = bowl.get("average", 0)
                query = """
                INSERT OR IGNORE INTO Players (player_id, name, country, total_wickets, bowling_average, economy_rate)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                run_query(query, (player_id, name, "Unknown", wkts, avg, econ))
                inserted += 1

    logging.info(f"✅ Inserted or updated {inserted} players into DB.")
    return inserted
