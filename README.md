# The World Cup Gazette 🏆

A live World Cup 2026 dashboard built with Python and Flask. Pulls real-time data from the football-data.org API to display group standings, upcoming fixtures, and recent results — styled as a vintage newspaper.

## Live Demo
[world-cup-bracket-mcjm.onrender.com](https://world-cup-bracket-mcjm.onrender.com)

## Features
- Live group standings for all 12 groups with country flags
- Upcoming fixture schedule with venues and kickoff times
- Recent match results with animated score counters
- Light and dark mode toggle with saved preference
- Responsive newspaper-style design

## Built With
- Python 3.12
- Flask
- football-data.org API
- HTML / CSS / Vanilla JavaScript
- Deployed on Render

## Run Locally
```bash
git clone https://github.com/satbarseghyan/World-Cup-Bracket.git
cd World-Cup-Bracket
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Create a `.env` file with your API key: