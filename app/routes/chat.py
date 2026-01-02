from flask import Blueprint

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
def chat_list():
    """List all conversations"""
    return "Chat page - Coming soon"

@bp.route('/<conversation_id>')
def conversation(conversation_id):
    """Individual conversation"""
    return f"Conversation {conversation_id} - Coming soon"
