from flask import Flask, request, jsonify
from celery_config import celery, long_running_task

app = Flask(__name__)

@app.route('/start_task', methods=['POST'])
def start_task():
    task = long_running_task.apply_async()
    return jsonify({'task_id': task.id}), 202

@app.route('/stop_task', methods=['POST'])
def stop_task():
    task_id = request.json['task_id']
    celery.control.revoke(task_id, terminate=True)
    return jsonify({'status': 'Task terminated'})

if __name__ == '__main__':
    app.run(debug=True)
