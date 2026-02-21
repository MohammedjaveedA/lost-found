from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import mongo, jwt  # Import from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints (import after mongo is initialized)
    from routes.auth import auth_bp
    from routes.organizations import org_bp
    from routes.items import items_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(org_bp, url_prefix='/api/organizations')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    
    # Test route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "message": "Lost & Found API is running!"}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, port=Config.PORT)