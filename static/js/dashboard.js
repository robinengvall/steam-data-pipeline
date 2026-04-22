const API_BASE = '/api';

const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const contentEl = document.getElementById('content');
const steamIdInput = document.getElementById('steam-id-input');
const fetchButton = document.getElementById('fetch-button');

let currentMode = 'database';

async function initDashboard() {
    fetchButton.addEventListener('click', fetchProfileData);
    steamIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            fetchProfileData();
        }
    });
    
    await loadDatabaseData();
}

async function loadDatabaseData() {
    currentMode = 'database';
    try {
        loadingEl.classList.remove('hidden');
        contentEl.classList.add('hidden');
        errorEl.classList.add('hidden');
        
        const [stats, topGames, deltas, newGames, history] = await Promise.all([
            fetchData('/stats'),
            fetchData('/games/top?limit=10'),
            fetchData('/playtime/deltas?limit=10'),
            fetchData('/games/new'),
            fetchData('/playtime/history?limit=10')
        ]);

        loadingEl.classList.add('hidden');
        contentEl.classList.remove('hidden');

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

async function fetchProfileData() {
    const steamId = steamIdInput.value.trim();
    
    if (!steamId) {
        alert('Please enter a Steam ID');
        return;
    }
    
    currentMode = 'live';
    try {
        fetchButton.disabled = true;
        fetchButton.textContent = 'Fetching...';
        loadingEl.classList.remove('hidden');
        contentEl.classList.add('hidden');
        errorEl.classList.add('hidden');
        
        const response = await fetch(`${API_BASE}/fetch-profile?steam_id=${encodeURIComponent(steamId)}`);
        const json = await response.json();
        
        if (!json.success) {
            throw new Error(json.error || 'Failed to fetch profile');
        }
        
        const profileData = json.data;
        
        loadingEl.classList.add('hidden');
        contentEl.classList.remove('hidden');
        
        renderStats({
            total_games: profileData.total_games,
            total_playtime_hours: profileData.total_playtime_hours,
            total_playtime_minutes: profileData.total_playtime_minutes,
            snapshot_timestamp: profileData.snapshot_timestamp
        });
        
        const topGames = profileData.games.slice(0, 10);
        renderTopGames(topGames);
        
        renderRecentActivity([]);
        renderNewGames([]);
        renderPlaytimeHistory([]);
        
    } catch (error) {
        console.error('Error fetching profile:', error);
        loadingEl.classList.add('hidden');
        errorEl.classList.remove('hidden');
        errorEl.querySelector('p').textContent = error.message || 'Failed to fetch profile data.';
    } finally {
        fetchButton.disabled = false;
        fetchButton.textContent = 'Fetch Profile';
    }
}

async function fetchData(endpoint) {
    const response = await fetch(API_BASE + endpoint);
    if (!response.ok) {
        throw new Error(`API request failed: ${endpoint}`);
    }
    const json = await response.json();
    return json.data;
}

function renderStats(stats) {
    document.getElementById('total-games').textContent = stats.total_games;
    document.getElementById('total-playtime').textContent = 
        formatNumber(stats.total_playtime_hours) + ' hrs';
    document.getElementById('total-playtime-hours').textContent = 
        formatNumber(stats.total_playtime_minutes) + ' minutes';
    
    const date = new Date(stats.snapshot_timestamp);
    document.getElementById('last-updated').textContent = formatDate(date);
}

function renderTopGames(games) {
    const container = document.getElementById('top-games');
    container.innerHTML = '';

    games.forEach((game, index) => {
        const gameEl = document.createElement('div');
        gameEl.className = 'game-item';
        
        const gameInfo = document.createElement('div');
        gameInfo.className = 'game-info';
        
        const gameRank = document.createElement('span');
        gameRank.className = 'game-rank';
        gameRank.textContent = `#${index + 1}`;
        
        const gameName = document.createElement('span');
        gameName.className = 'game-name';
        gameName.textContent = game.name;
        
        gameInfo.appendChild(gameRank);
        gameInfo.appendChild(gameName);
        
        const gameStats = document.createElement('div');
        gameStats.className = 'game-stats';
        
        const statsContainer = document.createElement('div');
        
        const playtime = document.createElement('div');
        playtime.className = 'game-playtime';
        playtime.textContent = `${formatNumber(game.playtime_hours)} hrs`;
        
        const playtimeLabel = document.createElement('div');
        playtimeLabel.className = 'game-playtime-label';
        playtimeLabel.textContent = `${formatNumber(game.playtime_minutes)} minutes`;
        
        statsContainer.appendChild(playtime);
        statsContainer.appendChild(playtimeLabel);
        gameStats.appendChild(statsContainer);
        
        gameEl.appendChild(gameInfo);
        gameEl.appendChild(gameStats);
        container.appendChild(gameEl);
    });
}

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
        
        const activityName = document.createElement('span');
        activityName.className = 'activity-name';
        activityName.textContent = delta.name;
        
        const activityDelta = document.createElement('span');
        activityDelta.className = 'activity-delta';
        activityDelta.textContent = `+${formatNumber(delta.delta_hours)} hrs`;
        
        activityEl.appendChild(activityName);
        activityEl.appendChild(activityDelta);
        activityListEl.appendChild(activityEl);
    });
}

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
        
        const gameInfo = document.createElement('div');
        gameInfo.className = 'game-info';
        
        const gameName = document.createElement('span');
        gameName.className = 'game-name';
        gameName.textContent = game.name;
        
        gameInfo.appendChild(gameName);
        
        const gameStats = document.createElement('div');
        gameStats.className = 'game-stats';
        
        const statsContainer = document.createElement('div');
        
        const playtime = document.createElement('div');
        playtime.className = 'game-playtime';
        playtime.textContent = `${formatNumber(game.playtime_hours)} hrs`;
        
        statsContainer.appendChild(playtime);
        gameStats.appendChild(statsContainer);
        
        gameEl.appendChild(gameInfo);
        gameEl.appendChild(gameStats);
        gamesListEl.appendChild(gameEl);
    });
}

function renderPlaytimeHistory(history) {
    const container = document.getElementById('history-chart');
    container.innerHTML = '';

    if (!history || history.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'No history available. Multiple ingestion runs are required to display trends.';
        container.appendChild(emptyState);
        return;
    }

    const maxHours = Math.max(...history.map(h => h.total_playtime_hours));

    history.forEach(snapshot => {
        const date = new Date(snapshot.timestamp);
        const percentage = (snapshot.total_playtime_hours / maxHours) * 100;

        const historyEl = document.createElement('div');
        historyEl.className = 'history-item';
        
        const historyDate = document.createElement('div');
        historyDate.className = 'history-date';
        historyDate.textContent = formatDate(date);
        
        const barContainer = document.createElement('div');
        barContainer.className = 'history-bar-container';
        
        const bar = document.createElement('div');
        bar.className = 'history-bar';
        bar.style.width = `${percentage}%`;
        bar.textContent = `${formatNumber(snapshot.total_playtime_hours)} hrs`;
        
        barContainer.appendChild(bar);
        historyEl.appendChild(historyDate);
        historyEl.appendChild(barContainer);
        container.appendChild(historyEl);
    });
}

function formatNumber(num) {
    return num.toLocaleString('en-US', { maximumFractionDigits: 1 });
}

function formatDate(date) {
    return date.toLocaleDateString('sv-SE', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

document.addEventListener('DOMContentLoaded', initDashboard);
