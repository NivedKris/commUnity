from flask import Flask
from flask_login import LoginManager
from datetime import datetime
import os

# Initialize extensions
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import and register blueprints
    from app.routes import main, auth, events, groups, issues, chat, profile
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(groups.bp)
    app.register_blueprint(issues.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(profile.bp)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get_by_id(user_id)
    
    # Context processor for Firebase config
    @app.context_processor
    def inject_firebase_config():
        from app.config import Config
        return {'firebase_config': Config.get_firebase_config()}
    
    # Add custom Jinja2 filters
    @app.template_filter('timeago')
    def timeago_filter(timestamp):
        """Convert timestamp to 'time ago' format"""
        if not timestamp:
            return 'Recently'
        
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return 'Recently'
        
        now = datetime.utcnow()
        if timestamp.tzinfo:
            from datetime import timezone
            now = datetime.now(timezone.utc)
        
        diff = now - timestamp
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return 'Just now'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        elif seconds < 2592000:
            days = int(seconds / 86400)
            return f'{days} day{"s" if days != 1 else ""} ago'
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            return f'{months} month{"s" if months != 1 else ""} ago'
        else:
            years = int(seconds / 31536000)
            return f'{years} year{"s" if years != 1 else ""} ago'
    
    return app
