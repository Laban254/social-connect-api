from flask import Blueprint, request, jsonify
from app.posts.models import Post, Hashtag
from app.utils.auth import get_current_user_id  
from app.posts.services import create_post_service, get_user_feed_service, search_hashtags_service

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['POST'])
def create_post():
    """Create a new post."""
    current_user_id = get_current_user_id()
    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    content = data.get('content')
    media_url = data.get('media_url') 
    hashtags = data.get('hashtags', [])  

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    post = create_post_service(user_id=current_user_id, content=content, media_url=media_url, hashtags=hashtags)
    
    return jsonify({
        'message': 'Post created successfully',
        'post': {
            'id': post.id,
            'content': post.content,
            'media_url': post.media_url,
            'created_at': post.created_at
        }
    }), 201

@posts_bp.route('/users/<int:user_id>/feed', methods=['GET'])
def get_user_feed(user_id):
    """Get the feed for a specific user."""
    current_user_id = get_current_user_id()
    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    feed = get_user_feed_service(user_id)
    return jsonify(feed), 200

@posts_bp.route('/hashtags', methods=['GET'])
def search_hashtags():
    """Search for hashtags based on a query."""
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    hashtags = search_hashtags_service(query)
    return jsonify({'hashtags': hashtags}), 200
