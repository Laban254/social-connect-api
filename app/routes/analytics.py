from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.analytics import UserAnalytics, ContentAnalytics, AudienceInsight, APIAnalytics, CustomReport
from app import db
from datetime import datetime, timedelta
import pandas as pd
import io
import json

analytics_bp = Blueprint('analytics', __name__)

# User Analytics Routes
@analytics_bp.route('/analytics/user', methods=['GET'])
@jwt_required()
def get_user_analytics():
    current_user_id = get_jwt_identity()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = UserAnalytics.query.filter(
        UserAnalytics.user_id == current_user_id
    )
    
    if start_date:
        query = query.filter(UserAnalytics.date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(UserAnalytics.date <= datetime.fromisoformat(end_date).date())
    
    analytics = query.all()
    
    return jsonify({
        'analytics': [{
            'date': a.date.isoformat(),
            'active_time': a.active_time,
            'post_count': a.post_count,
            'comment_count': a.comment_count,
            'like_count': a.like_count,
            'share_count': a.share_count,
            'story_views': a.story_views,
            'poll_participation': a.poll_participation,
            'event_attendance': a.event_attendance
        } for a in analytics]
    })

# Content Analytics Routes
@analytics_bp.route('/analytics/content', methods=['GET'])
@jwt_required()
def get_content_analytics():
    current_user_id = get_jwt_identity()
    content_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = ContentAnalytics.query.filter(
        ContentAnalytics.user_id == current_user_id
    )
    
    if content_type:
        query = query.filter(ContentAnalytics.content_type == content_type)
    if start_date:
        query = query.filter(ContentAnalytics.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(ContentAnalytics.created_at <= datetime.fromisoformat(end_date))
    
    analytics = query.all()
    
    return jsonify({
        'analytics': [{
            'content_id': a.content_id,
            'content_type': a.content_type,
            'created_at': a.created_at.isoformat(),
            'views': a.views,
            'likes': a.likes,
            'comments': a.comments,
            'shares': a.shares,
            'engagement_rate': a.engagement_rate,
            'reach': a.reach
        } for a in analytics]
    })

# Audience Insights Routes
@analytics_bp.route('/analytics/audience', methods=['GET'])
@jwt_required()
def get_audience_insights():
    current_user_id = get_jwt_identity()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = AudienceInsight.query.filter(
        AudienceInsight.user_id == current_user_id
    )
    
    if start_date:
        query = query.filter(AudienceInsight.date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(AudienceInsight.date <= datetime.fromisoformat(end_date).date())
    
    insights = query.all()
    
    return jsonify({
        'insights': [{
            'date': i.date.isoformat(),
            'age_group': i.age_group,
            'gender': i.gender,
            'location': i.location,
            'interests': i.interests,
            'active_hours': i.active_hours,
            'device_type': i.device_type
        } for i in insights]
    })

# API Analytics Routes
@analytics_bp.route('/analytics/api', methods=['GET'])
@jwt_required()
def get_api_analytics():
    current_user_id = get_jwt_identity()
    endpoint = request.args.get('endpoint')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = APIAnalytics.query.filter(
        APIAnalytics.user_id == current_user_id
    )
    
    if endpoint:
        query = query.filter(APIAnalytics.endpoint == endpoint)
    if start_date:
        query = query.filter(APIAnalytics.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(APIAnalytics.timestamp <= datetime.fromisoformat(end_date))
    
    analytics = query.all()
    
    return jsonify({
        'analytics': [{
            'endpoint': a.endpoint,
            'method': a.method,
            'timestamp': a.timestamp.isoformat(),
            'response_time': a.response_time,
            'status_code': a.status_code,
            'request_size': a.request_size,
            'response_size': a.response_size
        } for a in analytics]
    })

# Custom Reports Routes
@analytics_bp.route('/analytics/reports', methods=['POST'])
@jwt_required()
def create_custom_report():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        report = CustomReport(
            user_id=current_user_id,
            name=data['name'],
            description=data.get('description'),
            report_type=data['report_type'],
            parameters=data.get('parameters', {}),
            schedule=data.get('schedule'),
            export_format=data.get('export_format', 'json')
        )
        
        if report.schedule:
            report.next_generation = calculate_next_generation(report.schedule)
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'message': 'Report created successfully',
            'report': {
                'id': report.id,
                'name': report.name,
                'next_generation': report.next_generation.isoformat() if report.next_generation else None
            }
        }), 201
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400

@analytics_bp.route('/analytics/reports/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    current_user_id = get_jwt_identity()
    report = CustomReport.query.filter_by(
        id=report_id,
        user_id=current_user_id
    ).first_or_404()
    
    # Generate report data based on type and parameters
    data = generate_report_data(report)
    
    if report.export_format == 'csv':
        df = pd.DataFrame(data)
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{report.name}.csv'
        )
    else:  # json
        return jsonify(data)

def calculate_next_generation(schedule):
    now = datetime.utcnow()
    if schedule == 'daily':
        return now + timedelta(days=1)
    elif schedule == 'weekly':
        return now + timedelta(weeks=1)
    elif schedule == 'monthly':
        # Add one month, handling year rollover
        if now.month == 12:
            return now.replace(year=now.year + 1, month=1)
        else:
            return now.replace(month=now.month + 1)
    return None

def generate_report_data(report):
    if report.report_type == 'user':
        query = UserAnalytics.query.filter_by(user_id=report.user_id)
        if 'start_date' in report.parameters:
            query = query.filter(UserAnalytics.date >= datetime.fromisoformat(report.parameters['start_date']).date())
        if 'end_date' in report.parameters:
            query = query.filter(UserAnalytics.date <= datetime.fromisoformat(report.parameters['end_date']).date())
        return [{
            'date': a.date.isoformat(),
            'active_time': a.active_time,
            'post_count': a.post_count,
            'comment_count': a.comment_count,
            'like_count': a.like_count
        } for a in query.all()]
    
    elif report.report_type == 'content':
        query = ContentAnalytics.query.filter_by(user_id=report.user_id)
        if 'content_type' in report.parameters:
            query = query.filter(ContentAnalytics.content_type == report.parameters['content_type'])
        if 'start_date' in report.parameters:
            query = query.filter(ContentAnalytics.created_at >= datetime.fromisoformat(report.parameters['start_date']))
        if 'end_date' in report.parameters:
            query = query.filter(ContentAnalytics.created_at <= datetime.fromisoformat(report.parameters['end_date']))
        return [{
            'content_id': a.content_id,
            'content_type': a.content_type,
            'created_at': a.created_at.isoformat(),
            'views': a.views,
            'likes': a.likes,
            'comments': a.comments
        } for a in query.all()]
    
    elif report.report_type == 'audience':
        query = AudienceInsight.query.filter_by(user_id=report.user_id)
        if 'start_date' in report.parameters:
            query = query.filter(AudienceInsight.date >= datetime.fromisoformat(report.parameters['start_date']).date())
        if 'end_date' in report.parameters:
            query = query.filter(AudienceInsight.date <= datetime.fromisoformat(report.parameters['end_date']).date())
        return [{
            'date': i.date.isoformat(),
            'age_group': i.age_group,
            'gender': i.gender,
            'location': i.location,
            'interests': i.interests
        } for i in query.all()]
    
    elif report.report_type == 'api':
        query = APIAnalytics.query.filter_by(user_id=report.user_id)
        if 'endpoint' in report.parameters:
            query = query.filter(APIAnalytics.endpoint == report.parameters['endpoint'])
        if 'start_date' in report.parameters:
            query = query.filter(APIAnalytics.timestamp >= datetime.fromisoformat(report.parameters['start_date']))
        if 'end_date' in report.parameters:
            query = query.filter(APIAnalytics.timestamp <= datetime.fromisoformat(report.parameters['end_date']))
        return [{
            'endpoint': a.endpoint,
            'method': a.method,
            'timestamp': a.timestamp.isoformat(),
            'response_time': a.response_time,
            'status_code': a.status_code
        } for a in query.all()]
    
    return [] 