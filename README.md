# Steam Data Pipeline

A production-ready data pipeline that ingests Steam user data daily, stores historical snapshots, and exposes analytics through an API.

## Tech Stack

- **Python 3.x**
- **Flask** - API framework
- **MongoDB** - Document database for snapshots
- **requests** - HTTP client for Steam API
- **python-dotenv** - Environment configuration

## Project Structure

```
steam-data-pipeline/
├── config.py                     # Configuration management
├── run_ingestion.py             # Entry point for data ingestion
├── start_mongodb.sh             # Helper script to start MongoDB
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables (not committed)
└── src/
    ├── clients/
    │   └── steam_client.py      # Steam API wrapper
    ├── services/
    │   └── ingestion_service.py # Business logic
    ├── db/
    │   └── mongo_client.py      # MongoDB operations
    └── routes/                  # Flask routes (coming soon)
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

### Example Output

```
Connected to MongoDB: steam_data
Starting data ingestion...
Fetching games from Steam API...
Retrieved 288 games from Steam
Saving snapshot to MongoDB...
Snapshot saved with ID: 69e8a47ac11f574b74ac47d0

=== Ingestion Complete ===
Snapshot ID: 69e8a47ac11f574b74ac47d0
Games stored: 288
Total playtime: 12324.2 hours
MongoDB connection closed
```

## Architecture

### Separation of Concerns

- **clients/**: External API communication (Steam Web API)
- **services/**: Business logic and data orchestration
- **db/**: Database operations (MongoDB)
- **routes/**: HTTP endpoints (Flask API - coming later)

### Why This Structure?

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Changes to Steam API don't affect database code
3. **Scalability**: Easy to add new data sources or storage backends
4. **Production-ready**: Follows industry best practices for data pipelines

## Coming Next

- [ ] Playtime delta calculations (compare snapshots)
- [ ] New game detection
- [ ] Flask API endpoints for analytics
- [ ] Dashboard visualization
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
