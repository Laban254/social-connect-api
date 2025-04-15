from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.group import Group, GroupMember, GroupEvent, EventAttendee, GroupDiscussion, DiscussionComment
from app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        group = Group(
            name=data['name'],
            description=data.get('description'),
            is_private=data.get('is_private', False),
            creator_id=current_user_id
        )
        db.session.add(group)
        db.session.commit()
        
        # Add creator as admin
        member = GroupMember(
            group_id=group.id,
            user_id=current_user_id,
            role='admin'
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'message': 'Group created successfully',
            'group': {
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'is_private': group.is_private
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Group name already exists'}), 400

@groups_bp.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    current_user_id = get_jwt_identity()
    groups = Group.query.join(GroupMember).filter(
        GroupMember.user_id == current_user_id
    ).all()
    
    return jsonify({
        'groups': [{
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'is_private': group.is_private,
            'member_count': len(group.members)
        } for group in groups]
    })

@groups_bp.route('/groups/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    current_user_id = get_jwt_identity()
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member or group is public
    if group.is_private and not any(m.user_id == current_user_id for m in group.members):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'group': {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'is_private': group.is_private,
            'members': [{
                'user_id': m.user_id,
                'role': m.role,
                'joined_at': m.joined_at.isoformat()
            } for m in group.members],
            'events': [{
                'id': e.id,
                'title': e.title,
                'start_time': e.start_time.isoformat(),
                'end_time': e.end_time.isoformat()
            } for e in group.events],
            'discussions': [{
                'id': d.id,
                'title': d.title,
                'created_at': d.created_at.isoformat()
            } for d in group.discussions]
        }
    })

@groups_bp.route('/groups/<int:group_id>/members', methods=['POST'])
@jwt_required()
def add_member(group_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    group = Group.query.get_or_404(group_id)
    
    # Check if current user is admin
    if not any(m.user_id == current_user_id and m.role == 'admin' for m in group.members):
        return jsonify({'error': 'Only admins can add members'}), 403
    
    try:
        member = GroupMember(
            group_id=group_id,
            user_id=user_id,
            role='member'
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'message': 'Member added successfully',
            'member': {
                'user_id': user_id,
                'role': 'member'
            }
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User is already a member'}), 400

@groups_bp.route('/groups/<int:group_id>/events', methods=['POST'])
@jwt_required()
def create_event(group_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member
    if not any(m.user_id == current_user_id for m in group.members):
        return jsonify({'error': 'Only members can create events'}), 403
    
    try:
        event = GroupEvent(
            group_id=group_id,
            title=data['title'],
            description=data.get('description'),
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            location=data.get('location')
        )
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'message': 'Event created successfully',
            'event': {
                'id': event.id,
                'title': event.title,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat()
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400

@groups_bp.route('/groups/<int:group_id>/discussions', methods=['POST'])
@jwt_required()
def create_discussion(group_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member
    if not any(m.user_id == current_user_id for m in group.members):
        return jsonify({'error': 'Only members can create discussions'}), 403
    
    try:
        discussion = GroupDiscussion(
            group_id=group_id,
            title=data['title'],
            content=data['content'],
            created_by=current_user_id
        )
        db.session.add(discussion)
        db.session.commit()
        
        return jsonify({
            'message': 'Discussion created successfully',
            'discussion': {
                'id': discussion.id,
                'title': discussion.title,
                'created_at': discussion.created_at.isoformat()
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400 