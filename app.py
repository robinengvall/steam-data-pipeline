"""
Flask application for Steam Data Pipeline API.
Exposes analytics endpoints for game statistics.
"""
from flask import Flask, jsonify
from src.db.mongo_client import MongoDBClient
from src.services.analytics_service import AnalyticsService
from src.routes.api_routes import create_routes


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Initialize database client
    db_client = MongoDBClient()
    db_client.connect()
    
    # Initialize analytics service
    analytics_service = AnalyticsService(db_client)
    
    # Register routes
    api_blueprint = create_routes(analytics_service)
    app.register_blueprint(api_blueprint)
    
    # Root endpoint
    @app.route('/')
    def index():
        """API information endpoint."""
        return jsonify({
            "name": "Steam Data Pipeline API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "stats": "/api/stats",
                "playtime": {
                    "total": "/api/playtime/total",
                    "history": "/api/playtime/history?limit=10",
                    "deltas": "/api/playtime/deltas?limit=10"
                },
                "games": {
                    "top": "/api/games/top?limit=10",
                    "new": "/api/games/new"
                }
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check endpoint."""
        try:
            # Test database connection
            db_client.client.admin.command('ping')
            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 503
    
    # Store db_client for cleanup
    app.db_client = db_client
    
    return app


def main():
    """Run the Flask application."""
    app = create_app()
    
    try:
        print("\n" + "="*50)
        print("Steam Data Pipeline API")
        print("="*50)
        print("\nAPI is starting...")
        print("Available at: http://localhost:5000")
        print("\nEndpoints:")
        print("  GET /              - API info")
        print("  GET /health        - Health check")
        print("  GET /api/stats     - Overall statistics")
        print("  GET /api/playtime/total    - Total playtime")
        print("  GET /api/playtime/history  - Playtime history")
        print("  GET /api/playtime/deltas   - Recent playtime changes")
        print("  GET /api/games/top         - Most played games")
        print("  GET /api/games/new         - Newly added games")
        print("\nPress CTRL+C to stop\n")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    finally:
        # Cleanup
        if hasattr(app, 'db_client'):
            app.db_client.close()


if __name__ == '__main__':
    main()
