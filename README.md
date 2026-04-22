# Steam Data Pipeline

A production-ready data pipeline that ingests Steam user data daily, stores historical snapshots, and exposes analytics through an API and interactive dashboard.

## Tech Stack

- **Python 3.x**
- **Flask** - API framework and web server
- **MongoDB** - Document database for snapshots
- **requests** - HTTP client for Steam API
- **python-dotenv** - Environment configuration
- **HTML/CSS/JavaScript** - Dashboard frontend

## Project Structure

```
steam-data-pipeline/
├── config.py                     # Configuration management
├── app.py                        # Flask app with API and dashboard
├── run_ingestion.py             # Entry point for data ingestion
├── test_api.py                  # API endpoint tests
├── test_dashboard.py            # Dashboard tests
├── view_snapshots.py            # View stored data
├── start_mongodb.sh             # Helper script to start MongoDB
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables (not committed)
├── templates/
│   └── dashboard.html           # Dashboard HTML
├── static/
│   ├── css/dashboard.css        # Dashboard styles
│   └── js/dashboard.js          # Dashboard JavaScript
└── src/
    ├── clients/
    │   └── steam_client.py      # Steam API wrapper
    ├── services/
    │   ├── ingestion_service.py # Ingestion business logic
    │   └── analytics_service.py # Analytics business logic
    ├── db/
    │   └── mongo_client.py      # MongoDB operations
    └── routes/
        └── api_routes.py        # Flask API routes
```

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your Steam credentials:

```
STEAM_API_KEY=your_steam_api_key_here
STEAM_ID=your_steam_id_here
```

### 3. Start MongoDB

```bash
# Start MongoDB (will create temp data directory)
./start_mongodb.sh
```

## Usage

### Run Data Ingestion

```bash
source venv/bin/activate
python run_ingestion.py
```

This will:
1. Fetch your Steam games from the API
2. Store a timestamped snapshot in MongoDB
3. Display summary statistics

### View the Dashboard

```bash
source venv/bin/activate
python app.py
```

Then open your browser to **`http://localhost:5000`**

The dashboard shows:
- **Overview stats** - Total games, playtime, last update time
- **Top 10 games** - Your most played games with hours
- **Recent activity** - Games played since last snapshot
- **New games** - Games added to your library
- **Playtime history** - Visual chart showing playtime trends

The dashboard automatically fetches data from the API and updates in real-time.

### Use the REST API

The API is also available at `http://localhost:5000/api`

**Available endpoints:**

- `GET /` - Dashboard (web interface)
- `GET /api` - API documentation
- `GET /health` - Health check
- `GET /api/stats` - Overall statistics (total games, playtime, last snapshot time)
- `GET /api/playtime/total` - Total playtime across all games
- `GET /api/playtime/history?limit=10` - Playtime history over snapshots
- `GET /api/playtime/deltas?limit=10` - Recent playtime changes between snapshots
- `GET /api/games/top?limit=10` - Most played games
- `GET /api/games/new` - Newly added games (between last 2 snapshots)

### Example API Responses

**GET /api/stats**
```json
{
  "success": true,
  "data": {
    "total_games": 288,
    "total_playtime_hours": 12324.2,
    "total_playtime_minutes": 739452,
    "snapshot_timestamp": "2026-04-22T10:44:21.502000"
  }
}
```

**GET /api/games/top?limit=3**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "appid": 730,
      "name": "Counter-Strike 2",
      "playtime_hours": 3810.13,
      "playtime_minutes": 228608,
      "last_played": 1774048307
    },
    {
      "appid": 252950,
      "name": "Rocket League",
      "playtime_hours": 1376.32,
      "playtime_minutes": 82579,
      "last_played": 1776714271
    },
    {
      "appid": 236850,
      "name": "Europa Universalis IV",
      "playtime_hours": 1341.33,
      "playtime_minutes": 80480,
      "last_played": 1776700904
    }
  ]
}
```

### Test API Endpoints

```bash
source venv/bin/activate
python test_api.py
```

This runs automated tests against all API endpoints.

### View Stored Data

```bash
source venv/bin/activate
python view_snapshots.py
```

This displays your stored snapshots and top games.

## Architecture

### Separation of Concerns

- **clients/**: External API communication (Steam Web API)
- **services/**: Business logic (ingestion, analytics)
- **db/**: Database operations (MongoDB)
- **routes/**: HTTP endpoints (Flask API)

### Why This Structure?

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Changes to Steam API don't affect database code
3. **Scalability**: Easy to add new data sources or storage backends
4. **Production-ready**: Follows industry best practices for data pipelines

## Features

- [x] Steam API integration (GetOwnedGames)
- [x] MongoDB storage with timestamped snapshots
- [x] Playtime delta calculations (compare snapshots)
- [x] New game detection
- [x] Flask API endpoints for analytics
- [x] Interactive web dashboard
- [ ] Automated scheduling with cron

## MongoDB Management

```bash
# Check if MongoDB is running
pgrep mongod

# Stop MongoDB
pkill mongod

# View logs
tail -f /tmp/mongodb.log

# Query data with mongosh
mongosh
> use steam_data
> db.game_snapshots.countDocuments()
> db.game_snapshots.find().limit(1).pretty()
```

## Troubleshooting

**MongoDB won't start:**
- Check if another instance is running: `pgrep mongod`
- Check logs: `cat /tmp/mongodb.log`
- Kill existing process: `pkill mongod` and retry

**Connection refused:**
- Ensure MongoDB is running: `./start_mongodb.sh`
- Check it's listening: `ss -tlnp | grep 27017`

**Steam API errors:**
- Verify your API key in `.env`
- Check your Steam ID is correct
- Ensure your profile is public
