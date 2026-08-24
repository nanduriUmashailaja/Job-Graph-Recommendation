from flask import Flask, jsonify, request
from flask_cors import CORS
from database import JobGraphDB

app = Flask(__name__)
CORS(app)

db = None
try:
    db = JobGraphDB()
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database error: {e}")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok" if db else "database_error"}), 200

@app.route('/api/candidates', methods=['GET'])
def get_all_candidates():
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    try:
        candidates = db.get_all_people()
        return jsonify(candidates), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    try:
        jobs = db.get_all_jobs()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommendations/<person_name>', methods=['GET'])
def get_recommendations(person_name):
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    try:
        recommendations = db.get_job_recommendations(person_name)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/candidates-for-job/<job_title>', methods=['GET'])
def get_job_candidates(job_title):
    if not db:
        return jsonify({"error": "Database not connected"}), 500
    try:
        candidates = db.get_candidates_for_job(job_title)
        return jsonify(candidates), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)