from flask import Blueprint, request, jsonify

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/generate", methods=["POST"])
def generate_resume():
    data = request.get_json()

    print("Received data:", data)  # DEBUG LOG

    if not data:
        return jsonify({"error": "No data provided"}), 400

    return jsonify({
        "status": "success",
        "message": "Resume data received successfully",
        "data": data
    }), 200
