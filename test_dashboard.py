from app import create_app
import json


def test_dashboard():
    """Test that the dashboard and all endpoints work."""
    app = create_app()
    client = app.test_client()
    
    print("\nTesting Steam Dashboard\n")
    
    print("1. Testing Dashboard HTML (GET /)")
    response = client.get('/')
    if response.status_code == 200:
        print("   Dashboard HTML loads successfully")
        print(f"   Content-Type: {response.content_type}")
        print(f"   Size: {len(response.data)} bytes")
    else:
        print(f"   Failed with status {response.status_code}")
    print()
    
    print("2. Testing CSS file")
    response = client.get('/static/css/dashboard.css')
    if response.status_code == 200:
        print("   CSS file loads successfully")
        print(f"   Size: {len(response.data)} bytes")
    else:
        print(f"   Failed with status {response.status_code}")
    print()
    
    print("3. Testing JavaScript file")
    response = client.get('/static/js/dashboard.js')
    if response.status_code == 200:
        print("   JavaScript file loads successfully")
        print(f"   Size: {len(response.data)} bytes")
    else:
        print(f"   Failed with status {response.status_code}")
    print()
    
    print("4. Testing API endpoints that dashboard uses")
    
    endpoints = [
        '/api/stats',
        '/api/games/top?limit=10',
        '/api/playtime/deltas?limit=10',
        '/api/games/new',
        '/api/playtime/history?limit=10'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        if response.status_code == 200:
            data = response.json
            if data.get('success'):
                print(f"   {endpoint} - Success")
            else:
                print(f"   {endpoint} - Failed: {data.get('error')}")
        else:
            print(f"   {endpoint} - Status {response.status_code}")
    
    print()
    
    print("5. Checking data availability")
    response = client.get('/api/stats')
    if response.status_code == 200:
        stats = response.json['data']
        print(f"   Total Games: {stats['total_games']}")
        print(f"   Total Playtime: {stats['total_playtime_hours']} hours")
        print(f"   Last Updated: {stats['snapshot_timestamp']}")
    print()
    
    print("Dashboard Test Complete!\n")
    print("To view the dashboard, run:")
    print("  python app.py")
    print("\nThen open in your browser:")
    print("  http://localhost:5000")
    print()
    
    app.db_client.close()


if __name__ == '__main__':
    test_dashboard()
