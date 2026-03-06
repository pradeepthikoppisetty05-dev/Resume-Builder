from flask import Blueprint, request, jsonify
from ai.summary_generator import generate_summary
from ai.experience_enhancer import enhance_experience_batch
from ai.ai_experience_enhancer import enhance_with_ai
from ai.ai_summary_generator import generate_summary_ai

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/api/ai/generate-summary", methods=["POST"])
def ai_generate_summary():
    data = request.get_json()
    resume_data = data.get("resumeData")
    variation = data.get("variation", 0)

    try:
        summary = generate_summary_ai(resume_data, variation)

        if not summary or len(summary.strip()) < 50:
            raise ValueError("AI summary too short")

    except Exception as e:
        print("AI summary failed, falling back to rule-based:", str(e))
        summary = generate_summary(resume_data, variation)

    return jsonify({"summary": summary})



@ai_bp.route("/api/ai/enhance-experience", methods=["POST"])
def ai_enhance_experience():
    data = request.get_json()
    resume_data = data.get("resumeData", {})
    variation = data.get("variation", 0)
    index = data.get("index")

    experience_list = resume_data.get("experience", [])
    
    try:
        enhanced_experience = enhance_with_ai(experience_list, index)
        exp = enhanced_experience[index]
        ai_text = exp.get("description", "")

        if not ai_text or len(ai_text.strip()) < 30:
            raise ValueError("AI returned weak output")

    except Exception as e:
        print("AI experience enhance failed → fallback:", str(e))

        enhanced_experience = enhance_experience_batch(
            experience_list, variation=0
        )


    return jsonify({"experience": enhanced_experience})
