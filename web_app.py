from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import json
from datetime import datetime
import threading
import time

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from firstcrew.enhanced_crew import EnhancedFirstcrew
    from firstcrew.llm_manager import get_llm_status
    Firstcrew = EnhancedFirstcrew
except ImportError:
    try:
        from firstcrew.crew import Firstcrew
        get_llm_status = lambda: {"error": "Enhanced LLM manager not available"}
    except ImportError:
        print("Warning: Could not import Firstcrew. Make sure you're in the correct directory.")
        Firstcrew = None
        get_llm_status = lambda: {"error": "No LLM manager available"}

app = Flask(__name__)

# Store for ongoing research tasks
research_tasks = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_research', methods=['POST'])
def start_research():
    data = request.json
    topic = data.get('topic', 'AI LLMs')
    
    # Generate unique task ID
    task_id = f"task_{int(time.time())}"
    
    # Initialize task status
    research_tasks[task_id] = {
        'status': 'starting',
        'topic': topic,
        'start_time': datetime.now().isoformat(),
        'progress': 'Initializing research...',
        'result': None,
        'error': None
    }
    
    # Start research in background thread
    thread = threading.Thread(target=run_research, args=(task_id, topic))
    thread.daemon = True
    thread.start()
    
    return jsonify({'task_id': task_id, 'status': 'started'})

def run_research(task_id, topic):
    try:
        research_tasks[task_id]['status'] = 'running'
        research_tasks[task_id]['progress'] = 'Starting AI research crew...'
        
        inputs = {
            'topic': topic,
            'current_year': str(datetime.now().year)
        }
        
        research_tasks[task_id]['progress'] = 'Conducting web research...'
        
        # Run the crew
        crew = Firstcrew()
        result = crew.crew().kickoff(inputs=inputs)
        
        research_tasks[task_id]['status'] = 'completed'
        research_tasks[task_id]['progress'] = 'Research completed successfully!'
        research_tasks[task_id]['result'] = str(result)
        research_tasks[task_id]['end_time'] = datetime.now().isoformat()
        
        # Save report to file
        report_filename = f"report_{task_id}.md"
        if os.path.exists('report.md'):
            os.rename('report.md', report_filename)
            research_tasks[task_id]['report_file'] = report_filename
        
    except Exception as e:
        research_tasks[task_id]['status'] = 'failed'
        research_tasks[task_id]['error'] = str(e)
        research_tasks[task_id]['end_time'] = datetime.now().isoformat()

@app.route('/task_status/<task_id>')
def task_status(task_id):
    if task_id in research_tasks:
        return jsonify(research_tasks[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/download_report/<task_id>')
def download_report(task_id):
    if task_id in research_tasks and 'report_file' in research_tasks[task_id]:
        report_file = research_tasks[task_id]['report_file']
        if os.path.exists(report_file):
            return send_file(report_file, as_attachment=True, download_name=f"research_report_{task_id}.md")
    return jsonify({'error': 'Report not found'}), 404

@app.route('/api/reports')
def list_reports():
    """API endpoint to list all completed research reports"""
    completed_tasks = {
        task_id: {
            'topic': task_data['topic'],
            'start_time': task_data['start_time'],
            'end_time': task_data.get('end_time'),
            'status': task_data['status']
        }
        for task_id, task_data in research_tasks.items()
        if task_data['status'] == 'completed'
    }
    return jsonify(completed_tasks)

@app.route('/api/report/<task_id>')
def get_report_content(task_id):
    """API endpoint to get report content as JSON"""
    if task_id in research_tasks and research_tasks[task_id]['status'] == 'completed':
        task_data = research_tasks[task_id]
        report_file = task_data.get('report_file')
        
        if report_file and os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return jsonify({
                'task_id': task_id,
                'topic': task_data['topic'],
                'start_time': task_data['start_time'],
                'end_time': task_data['end_time'],
                'content': content,
                'status': 'success'
            })
    
    return jsonify({'error': 'Report not found'}), 404

@app.route('/api/llm_status')
def llm_status():
    """API endpoint to get LLM status and usage"""
    try:
        status = get_llm_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)