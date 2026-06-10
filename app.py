from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

VENUES = {
    "MEX": "Estadio Azteca, Mexico City",
    "RSA": "Estadio Azteca, Mexico City",
    "KOR": "Estadio Akron, Guadalajara",
    "CZE": "Estadio Akron, Guadalajara",
    "CAN": "BMO Field, Toronto",
    "BIH": "BMO Field, Toronto",
    "QAT": "BC Place, Vancouver",
    "SUI": "BC Place, Vancouver",
    "BRA": "SoFi Stadium, Los Angeles",
    "MAR": "SoFi Stadium, Los Angeles",
    "HTI": "Levi's Stadium, San Jose",
    "SCO": "Levi's Stadium, San Jose",
    "USA": "SoFi Stadium, Los Angeles",
    "PRY": "SoFi Stadium, Los Angeles",
    "AUS": "Lumen Field, Seattle",
    "TUR": "Lumen Field, Seattle",
    "GER": "Mercedes-Benz Stadium, Atlanta",
    "CUW": "Mercedes-Benz Stadium, Atlanta",
    "SWE": "Lumen Field, Seattle",
    "NED": "Lumen Field, Seattle",
    "JPN": "Levi's Stadium, San Jose",
    "TUN": "Levi's Stadium, San Jose",
    "BEL": "Lumen Field, Seattle",
    "EGY": "Lumen Field, Seattle",
    "IRN": "SoFi Stadium, Los Angeles",
    "NZL": "SoFi Stadium, Los Angeles",
    "ESP": "Hard Rock Stadium, Miami",
    "CPV": "Hard Rock Stadium, Miami",
    "SAU": "Hard Rock Stadium, Miami",
    "URU": "Hard Rock Stadium, Miami",
    "ENG": "AT&T Stadium, Dallas",
    "CRO": "AT&T Stadium, Dallas",
    "GHA": "BMO Field, Toronto",
    "PAN": "BMO Field, Toronto",
    "ARG": "Arrowhead Stadium, Kansas City",
    "ALG": "Arrowhead Stadium, Kansas City",
    "AUT": "Levi's Stadium, San Jose",
    "JOR": "Levi's Stadium, San Jose",
    "POR": "NRG Stadium, Houston",
    "COD": "NRG Stadium, Houston",
    "UZB": "Estadio Azteca, Mexico City",
    "COL": "Estadio Azteca, Mexico City",
    "CIV": "SoFi Stadium, Los Angeles",
    "ECU": "SoFi Stadium, Los Angeles",
    "SRB": "MetLife Stadium, New York",
    "SEN": "MetLife Stadium, New York",
    "IRQ": "Gillette Stadium, Boston",
    "NOR": "Gillette Stadium, Boston",
    "FRA": "MetLife Stadium, New York",
    "IVY": "SoFi Stadium, Los Angeles",
}

FLAG_CODES = {
    "MEX": "mx", "RSA": "za", "KOR": "kr", "CZE": "cz",
    "CAN": "ca", "BIH": "ba", "QAT": "qa", "SUI": "ch",
    "BRA": "br", "MAR": "ma", "HTI": "ht", "SCO": "gb-sct",
    "USA": "us", "PRY": "py", "AUS": "au", "TUR": "tr",
    "ARG": "ar", "FRA": "fr", "ENG": "gb-eng", "ESP": "es",
    "POR": "pt", "GER": "de", "NED": "nl", "BEL": "be",
    "URU": "uy", "COL": "co", "ECU": "ec", "SEN": "sn",
    "GHA": "gh", "CMR": "cm", "JPN": "jp", "IRN": "ir",
    "SAU": "sa", "IRQ": "iq", "NOR": "no", "DEN": "dk",
    "SWE": "se", "AUT": "at", "SRB": "rs", "CRO": "hr",
    "SVK": "sk", "HUN": "hu", "ALG": "dz", "EGY": "eg",
    "TUN": "tn", "NZL": "nz", "PAN": "pa", "JOR": "jo",
    "CPV": "cv", "COD": "cd", "UZB": "uz", "CUW": "cw",
    "CIV": "ci", "PAR": "py", "BOL": "bo", "VEN": "ve",
    "HON": "hn", "SLV": "sv", "JAM": "jm", "NGR": "ng",
    "HTI": "ht", "SCT": "gb-sct", "IRE": "ie", "WAL": "gb-wls",
    "SUI": "ch", "GRE": "gr", "BUL": "bg", "ROU": "ro",
    "NOR": "no", "FIN": "fi", "ISL": "is", "CYP": "cy",
    "SAU": "sa", "UAE": "ae", "KUW": "kw", "BHR": "bh",
    "URU": "uy", "CHI": "cl", "PER": "pe", "BOL": "bo",
    "CIV": "ci", "MLI": "ml", "BFA": "bf", "GUI": "gn",
    "NZL": "nz", "FIJ": "fj", "PNG": "pg", "SOL": "sb",
    "PAN": "pa", "CRC": "cr", "GTM": "gt", "CUB": "cu",
    "HAI": "ht", "KSA": "sa", "URY": "uy",
}

def get_flag_url(tla):
    code = FLAG_CODES.get(tla, "").lower()
    if code:
        return f"https://flagcdn.com/w40/{code}.png"
    return ""

def get_venue(home_tla, away_tla):
    return VENUES.get(home_tla) or VENUES.get(away_tla) or "North America"

def format_match_time(utc_str):
    dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    local = dt.astimezone()
    return local.strftime("%b %d · %I:%M %p %Z")

def safe_get(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200 and resp.content:
            return resp.json()
    except Exception:
        pass
    return {}

@app.route("/")
def home():
    standings = safe_get(f"{BASE_URL}/competitions/WC/standings").get("standings", [])
    for group in standings:
        for entry in group.get("table", []):
            tla = entry["team"].get("tla", "")
            entry["team"]["flag_url"] = get_flag_url(tla)

    all_matches = safe_get(f"{BASE_URL}/competitions/WC/matches?status=SCHEDULED").get("matches", [])
    live_matches = safe_get(f"{BASE_URL}/competitions/WC/matches?status=IN_PLAY").get("matches", [])
    finished = safe_get(f"{BASE_URL}/competitions/WC/matches?status=FINISHED").get("matches", [])
    recent_finished = finished[-4:] if finished else []

    upcoming = (live_matches + all_matches)[:8]

    for m in upcoming + recent_finished:
        m["venue"] = get_venue(m["homeTeam"]["tla"], m["awayTeam"]["tla"])
        m["formatted_time"] = format_match_time(m["utcDate"])
        m["group_label"] = m.get("group", "").replace("GROUP_", "Group ")
        m["homeTeam"]["flag_url"] = get_flag_url(m["homeTeam"]["tla"])
        m["awayTeam"]["flag_url"] = get_flag_url(m["awayTeam"]["tla"])

    return render_template("index.html",
                           standings=standings,
                           upcoming=upcoming,
                           recent_finished=recent_finished)

if __name__ == "__main__":
    app.run(debug=True)