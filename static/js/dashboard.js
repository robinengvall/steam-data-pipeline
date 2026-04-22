// Steam Dashboard JavaScript
const API_BASE = '/api';

// DOM Elements
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const contentEl = document.getElementById('content');

// Initialize dashboard
async function initDashboard() {
    try {
        // Fetch all data in parallel
        const [stats, topGames, deltas, newGames, history] = await Promise.all([
            fetchData('/stats'),
            fetchData('/games/top?limit=10'),
            fetchData('/playtime/deltas?limit=10'),
            fetchData('/games/new'),
            fetchData('/playtime/history?limit=10')
        ]);

        // Hide loading, show content
        loadingEl.classList.add('hidden');
        contentEl.classList.remove('hidden');

        // Render all sections
        renderStats(stats);
        renderTopGames(topGames);
        renderRecentActivity(deltas);
        renderNewGames(newGames);
        renderPlaytimeHistory(history);

    } catch (error) {
        console.error('Error loading dashboard:', error);
        loadingEl.classList.add('hidden');
        errorEl.classList.remove('hidden');
    }
}

// Fetch data from API
async function fetchData(endpoint) {
    const response = await fetch(API_BASE + endpoint);
    if (!response.ok) {
        throw new Error(`API request failed: ${endpoint}`);
    }
    const json = await response.json();
    return json.data;
}

// Render overall stats
function renderStats(stats) {
    document.getElementById('total-games').textContent = stats.total_games;
    document.getElementById('total-playtime').textContent = 
        formatNumber(stats.total_playtime_hours) + ' hrs';
    document.getElementById('total-playtime-hours').textContent = 
        formatNumber(stats.total_playtime_hours) + ' hours';
    
    const date = new Date(stats.snapshot_timestamp);
    document.getElementById('last-updated').textContent = formatDate(date);
}

// Render top games
function renderTopGames(games) {
    const container = document.getElementById('top-games');
    container.innerHTML = '';

    games.forEach((game, index) => {
        const gameEl = document.createElement('div');
        gameEl.className = 'game-item';
        gameEl.innerHTML = `
            <div class="game-info">
                <span class="game-rank">#${index + 1}</span>
                <span class="game-name">${escapeHtml(game.name)}</span>
            </div>
            <div class="game-stats">
                <div>
                    <div class="game-playtime">${formatNumber(game.playtime_hours)} hrs</div>
                    <div class="game-playtime-label">${formatNumber(game.playtime_minutes)} minutes</div>
                </div>
            </div>
        `;
        container.appendChild(gameEl);
    });
}

// Render recent activity (playtime deltas)
function renderRecentActivity(deltas) {
    const noActivityEl = document.getElementById('no-activity');
    const activityListEl = document.getElementById('activity-list');

    if (!deltas || deltas.length === 0) {
        noActivityEl.classList.remove('hidden');
        activityListEl.classList.add('hidden');
        return;
    }

    noActivityEl.classList.add('hidden');
    activityListEl.classList.remove('hidden');
    activityListEl.innerHTML = '';

    deltas.forEach(delta => {
        const activityEl = document.createElement('div');
        activityEl.className = 'activity-item';
        activityEl.innerHTML = `
            <span class="activity-name">${escapeHtml(delta.name)}</span>
            <span class="activity-delta">+${formatNumber(delta.delta_hours)} hrs</span>
        `;
        activityListEl.appendChild(activityEl);
    });
}

// Render new games
function renderNewGames(games) {
    const noGamesEl = document.getElementById('no-new-games');
    const gamesListEl = document.getElementById('new-games-list');

    if (!games || games.length === 0) {
        noGamesEl.classList.remove('hidden');
        gamesListEl.classList.add('hidden');
        return;
    }

    noGamesEl.classList.add('hidden');
    gamesListEl.classList.remove('hidden');
    gamesListEl.innerHTML = '';

    games.forEach(game => {
        const gameEl = document.createElement('div');
        gameEl.className = 'game-item';
        gameEl.innerHTML = `
            <div class="game-info">
                <span class="game-name">${escapeHtml(game.name)}</span>
            </div>
            <div class="game-stats">
                <div>
                    <div class="game-playtime">${formatNumber(game.playtime_hours)} hrs</div>
                </div>
            </div>
        `;
        gamesListEl.appendChild(gameEl);
    });
}

// Render playtime history chart
function renderPlaytimeHistory(history) {
    const container = document.getElementById('history-chart');
    container.innerHTML = '';

    if (!history || history.length === 0) {
        container.innerHTML = '<div class="empty-state">No history available yet. Run ingestion multiple times to see trends!</div>';
        return;
    }

    // Find max value for scaling
    const maxHours = Math.max(...history.map(h => h.total_playtime_hours));

    history.forEach(snapshot => {
        const date = new Date(snapshot.timestamp);
        const percentage = (snapshot.total_playtime_hours / maxHours) * 100;

        const historyEl = document.createElement('div');
        historyEl.className = 'history-item';
        historyEl.innerHTML = `
            <div class="history-date">${formatDate(date)}</div>
            <div class="history-bar-container">
                <div class="history-bar" style="width: ${percentage}%">
                    ${formatNumber(snapshot.total_playtime_hours)} hrs
                </div>
            </div>
        `;
        container.appendChild(historyEl);
    });
}

// Utility: Format number with commas
function formatNumber(num) {
    return num.toLocaleString('en-US', { maximumFractionDigits: 1 });
}

// Utility: Format date
function formatDate(date) {
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Start the dashboard when page loads
document.addEventListener('DOMContentLoaded', initDashboard);
