import pandas as pd

def clean_player_data(api_json):
    """Transform API player JSON to tabular format."""
    players = []
    for p in api_json.get("player", []):
        players.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "role": p.get("role"),
            "country": p.get("country"),
            "matches": p.get("matches", 0),
            "runs": p.get("runs", 0),
            "wickets": p.get("wickets", 0),
        })
    return pd.DataFrame(players)

def standardize_columns(df):
    """Normalize dataframe column names."""
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
    return df
