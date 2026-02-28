from flask import Blueprint, request, jsonify
from ai.summary_generator import generate_summary
from ai.experience_enhancer import enhance_experience_batch

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/api/ai/generate-summary", methods=["POST"])
def ai_generate_summary():
    data = request.get_json()
    resume_data = data.get("resumeData")
    variation = data.get("variation", 0)

    summary = generate_summary(resume_data, variation)

    return jsonify({"summary": summary})



@ai_bp.route("/api/ai/enhance-experience", methods=["POST"])
def ai_enhance_experience():
    data = request.get_json()
    resume_data = data.get("resumeData", {})
    variation = data.get("variation", 0)

    experience_list = resume_data.get("experience", [])
    enhanced_experience = enhance_experience_batch(experience_list, variation)

    return jsonify({"experience": enhanced_experience})