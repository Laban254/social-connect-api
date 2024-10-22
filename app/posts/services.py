from app.posts.models import Post, Hashtag, PostHashtag
from app import db

def create_post_service(user_id, content, media_url=None, hashtags=[]):
    """Create a new post."""
    post = Post(user_id=user_id, content=content, media_url=media_url)

    for tag in hashtags:
        tag = tag.strip('#')  
        existing_hashtag = Hashtag.query.filter_by(name=tag).first()
        if not existing_hashtag:
            existing_hashtag = Hashtag(name=tag)
            db.session.add(existing_hashtag)
        post.hashtags.append(existing_hashtag)

    db.session.add(post)
    db.session.commit()
    return post

def get_user_feed_service(user_id):
    """Fetch posts for the user."""
    posts = Post.query.filter_by(user_id=user_id).all()
    return [{
        'id': post.id,
        'content': post.content,
        'media_url': post.media_url,
        'created_at': post.created_at,
        'hashtags': [hashtag.name for hashtag in post.hashtags]
    } for post in posts]

def search_hashtags_service(query):
    """Search for hashtags."""
    hashtags = Hashtag.query.filter(Hashtag.name.ilike(f'%{query}%')).all()
    return [hashtag.name for hashtag in hashtags]
