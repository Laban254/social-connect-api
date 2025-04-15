from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.event import Event, EventAttendee, EventReminder
from app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        event = Event(
            user_id=current_user_id,
            title=data['title'],
            description=data.get('description'),
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            location=data.get('location'),
            is_private=data.get('is_private', False)
        )
        db.session.add(event)
        
        # Add creator as attendee
        attendee = EventAttendee(
            event=event,
            user_id=current_user_id,
            status='going'
        )
        db.session.add(attendee)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Event created successfully',
            'event': {
                'id': event.id,
                'title': event.title,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat(),
                'location': event.location
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400

@events_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    current_user_id = get_jwt_identity()
    events = Event.query.filter(
        Event.user_id == current_user_id
    ).all()
    
    return jsonify({
        'events': [{
            'id': event.id,
            'title': event.title,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'location': event.location,
            'attendee_count': len(event.attendees)
        } for event in events]
    })

@events_bp.route('/events/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)
    
    # Check if user is invited or event is public
    if event.is_private and not any(a.user_id == current_user_id for a in event.attendees):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'event': {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'location': event.location,
            'is_private': event.is_private,
            'attendees': [{
                'user_id': a.user_id,
                'status': a.status
            } for a in event.attendees]
        }
    })

@events_bp.route('/events/<int:event_id>/rsvp', methods=['POST'])
@jwt_required()
def rsvp_event(event_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        attendee = EventAttendee(
            event_id=event_id,
            user_id=current_user_id,
            status=data['status']  # going, maybe, not_going
        )
        db.session.add(attendee)
        db.session.commit()
        
        return jsonify({
            'message': 'RSVP recorded successfully',
            'rsvp': {
                'status': attendee.status
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Already RSVPed for this event'}), 400

@events_bp.route('/events/<int:event_id>/reminders', methods=['POST'])
@jwt_required()
def create_reminder(event_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        reminder = EventReminder(
            event_id=event_id,
            user_id=current_user_id,
            reminder_time=datetime.fromisoformat(data['reminder_time'])
        )
        db.session.add(reminder)
        db.session.commit()
        
        return jsonify({
            'message': 'Reminder created successfully',
            'reminder': {
                'id': reminder.id,
                'reminder_time': reminder.reminder_time.isoformat()
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Reminder already exists'}), 400 