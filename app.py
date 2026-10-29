"""
Flask Web Application for Tech Support Chatbot
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot_engine import ChatbotEngine
from src.analytics_engine import AnalyticsEngine
from src.export_manager import ExportManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
app.config['SECRET_KEY'] = 'tech-support-chatbot-secret-key-2024'

# Initialize chatbot
print("\n" + "="*60)
print("  Tech Support Assistant - Initializing...")
print("="*60)

chatbot = ChatbotEngine()
analytics = AnalyticsEngine(
    chatbot.context_manager,
    chatbot.sentiment_analyzer,
    chatbot.intent_matcher
)
export_manager = ExportManager(chatbot.context_manager)

print("\n[OK] Chatbot initialized successfully!")
print("="*60 + "\n")


@app.route('/')
def index():
    """Serve main chatbot interface"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    
    Expected JSON:
        {
            "message": "user message",
            "user_id": "user123",
            "language": "en"
        }
    
    Returns:
        {
            "response": "bot response",
            "sentiment": {...},
            "intent": "greeting",
            "confidence": 0.9
        }
    """
    try:
        data = request.get_json()
        
        message = data.get('message', '')
        user_id = data.get('user_id', 'web_user')
        language = data.get('language', 'en')
        
        if not message.strip():
            return jsonify({
                'error': 'Empty message'
            }), 400
        
        # Process message
        response_data = chatbot.process_message(message, user_id, language)
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/context/<user_id>', methods=['GET'])
def get_context(user_id):
    """Get conversation context for a user"""
    try:
        limit = request.args.get('limit', 10, type=int)
        context = chatbot.get_context(user_id, limit)
        
        return jsonify({
            'user_id': user_id,
            'messages': context,
            'count': len(context)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/context/<user_id>', methods=['DELETE'])
def clear_context(user_id):
    """Clear conversation context"""
    try:
        chatbot.clear_context(user_id)
        
        return jsonify({
            'message': 'Context cleared',
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit user feedback
    
    Expected JSON:
        {
            "user_id": "user123",
            "message": "original message",
            "response": "bot response",
            "rating": 5
        }
    """
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'web_user')
        message = data.get('message', '')
        response = data.get('response', '')
        rating = data.get('rating', 3)
        
        chatbot.provide_feedback(user_id, message, response, rating)
        
        return jsonify({
            'message': 'Feedback recorded',
            'rating': rating
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chatbot statistics"""
    try:
        stats = chatbot.get_statistics()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/analytics/<user_id>', methods=['GET'])
def get_analytics(user_id):
    """Get analytics for a specific user"""
    try:
        report = analytics.generate_report(user_id)
        return jsonify(report)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/analytics/all', methods=['GET'])
def get_all_analytics():
    """Get analytics for all users"""
    try:
        report = analytics.generate_report()
        return jsonify(report)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/export/<user_id>', methods=['GET'])
def export_conversation(user_id):
    """
    Export conversation
    
    Query params:
        format: 'json', 'text', or 'pdf'
    """
    try:
        format = request.args.get('format', 'json')
        
        filepath = export_manager.export_conversation(user_id, format)
        
        if filepath and os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=os.path.basename(filepath)
            )
        else:
            return jsonify({
                'error': 'Export failed'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tech Support Chatbot',
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Starting Tech Support Chatbot Web Server")
    print("="*60)
    print("\n  Features:")
    print("  [+] AI-powered tech support")
    print("  [+] Sentiment analysis")
    print("  [+] Multi-language support")
    print("  [+] Conversation memory")
    print("  [+] Analytics dashboard")
    print("  [+] Export functionality")
    print("\n  URL: http://localhost:5000")
    print("\n  Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n[INFO] Shutting down gracefully...")
        chatbot.shutdown()
        print("[OK] Server stopped")
