from flask import Blueprint, request, jsonify
from app.interactions.services import like_post, comment_on_post
from app.utils.auth import get_current_user_id 

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_a_post(post_id):
    """Like a post with the given post_id."""
    current_user_id = get_current_user_id()

    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    if like_post(current_user_id, post_id):
        return jsonify({'message': f'You liked post {post_id}'}), 201
    else:
        return jsonify({'error': 'Already liked this post'}), 409

@interactions_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
def comment_on_a_post(post_id):
    """Comment on a post with the given post_id."""
    current_user_id = get_current_user_id()

    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    comment = comment_on_post(current_user_id, post_id, content)
    return jsonify({
        'message': 'Comment added successfully',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'user_id': current_user_id,
            'post_id': post_id
        }
    }), 201
