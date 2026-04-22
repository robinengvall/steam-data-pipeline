# Dashboard Guide

## Overview

The Steam Data Pipeline Dashboard provides an interactive web interface to visualize your gaming statistics.

## Accessing the Dashboard

1. Make sure MongoDB is running:
   ```bash
   ./start_mongodb.sh
   ```

2. Start the Flask application:
   ```bash
   source venv/bin/activate
   python app.py
   ```

3. Open your browser to: **http://localhost:5000**

## Dashboard Sections

### 1. Stats Overview Cards

Three prominent cards display your key metrics:

- **Total Games** - Number of games in your library
- **Total Playtime** - Cumulative hours played across all games
- **Last Updated** - Timestamp of the most recent data snapshot

### 2. Most Played Games

A ranked list showing your top 10 games by playtime:
- Game rank and name
- Total hours and minutes played
- Color-coded with visual indicators

### 3. Recent Activity

Shows games you've played between the last two snapshots:
- Game names
- Hours gained since last snapshot
- Green highlights for active games

**Note**: This section requires at least 2 snapshots with actual gameplay between them.

### 4. New Games

Displays games recently added to your library:
- Game names
- Current playtime

**Note**: Requires 2+ snapshots with library changes to show data.

### 5. Playtime History

A visual bar chart showing total playtime across all snapshots:
- Date/time of each snapshot
- Total hours at that point in time
- Bars scaled relative to your highest playtime

The chart helps you visualize your gaming trends over time.

## Dashboard Features

- **Automatic Data Refresh**: Loads latest data from API on page load
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Error Handling**: Shows clear messages if API is unavailable
- **Loading States**: Visual feedback while data loads
- **No Database Required**: Pure client-side rendering (fetches from API)

## How Data Updates

The dashboard displays data from MongoDB snapshots:

1. Run ingestion to create a snapshot:
   ```bash
   python run_ingestion.py
   ```

2. Play some games

3. Run ingestion again:
   ```bash
   python run_ingestion.py
   ```

4. Refresh the dashboard to see:
   - Updated total playtime
   - Recent activity (games you played)
   - New additions to your library
   - Historical playtime trends

## Color Scheme

- **Purple gradient background** - Modern, gaming-themed aesthetic
- **White cards** - Clean, readable content areas
- **Blue accents** (#667eea) - Highlights and key metrics
- **Green highlights** - Recent activity and changes

## Troubleshooting

**Dashboard shows "Failed to load data":**
- Ensure MongoDB is running: `pgrep mongod`
- Ensure Flask app is running
- Check that you've run ingestion at least once
- Verify API responds: `curl http://localhost:5000/health`

**No recent activity or new games showing:**
- This is normal if you only have one snapshot
- Run ingestion, play games, then run ingestion again

**Playtime history only shows 1-2 bars:**
- Run ingestion multiple times over several days
- Each run creates a new snapshot and data point

## Customization

To customize the dashboard:

- **Styling**: Edit `static/css/dashboard.css`
- **Layout**: Edit `templates/dashboard.html`
- **Data display**: Edit `static/js/dashboard.js`
- **Number of games shown**: Modify API calls in dashboard.js (e.g., `?limit=20`)

## Architecture

```
Browser (dashboard.html)
    ↓ HTTP GET requests
Flask App (app.py)
    ↓ serves HTML/CSS/JS + API endpoints
Analytics Service
    ↓ queries
MongoDB (snapshots)
```

The dashboard is a Single Page Application (SPA) that:
1. Loads static HTML/CSS/JS from Flask
2. Makes AJAX requests to API endpoints
3. Renders data dynamically in the browser
4. No page reloads required
