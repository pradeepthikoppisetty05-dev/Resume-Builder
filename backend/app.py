from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from routes.ai import ai_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.resume import Resume
from playwright.sync_api import sync_playwright
import tempfile
from flask import send_file
from io import BytesIO

import os

from templates import classic, modern, twocolumn, creative, academic, corporate, ats, bold, minimal, sidebar, timeline, striped, architect, pastel, warm, technical, typographic

app = Flask(__name__)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/resume_builder?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app,
    resources={r"/api/*": {"origins": "http://localhost:3000"}},supports_credentials=True)
db.init_app(app)
jwt.init_app(app)

@jwt.unauthorized_loader
def missing_token(reason):
    return jsonify({"error": "JWT missing", "reason": reason}), 401

@jwt.invalid_token_loader
def invalid_token(reason):
    return jsonify({"error": "JWT invalid", "reason": reason}), 401

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({"error": "JWT expired"}), 401


app.register_blueprint(auth_bp)
app.register_blueprint(ai_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume Builder API"})

def preprocess_descriptions(data):
    experience = data.get("experience", [])

    for exp in experience:
        desc = exp.get("description", "")
        if isinstance(desc, str):
            exp["description"] = desc.replace("\n", "<br>")

    return data

def render_html(template_name, data):
    data = preprocess_descriptions(data)
    match template_name:
        case "modern":
            return modern.render(data)
        case "classic":
            return classic.render(data)
        case "twocolumn":
            return twocolumn.render(data)
        case "creative":
            return creative.render(data)
        case "corporate":
            return corporate.render(data)
        case "academic":
            return academic.render(data)
        case "ats":
            return ats.render(data)
        case "minimal":
            return minimal.render(data)
        case "sidebar":
            return sidebar.render(data)
        case "timeline":
            return timeline.render(data)
        case "striped":
            return striped.render(data)
        case "architect":
            return architect.render(data)
        case "pastel":
            return pastel.render(data)
        case "warm":
            return warm.render(data)
        case "technical":
            return technical.render(data)
        case "typographic":
            return typographic.render(data)
        case "bold":
            return bold.render(data)
        case _:
            return classic.render(data)

@app.route("/api/resume", methods=["POST"])
@jwt_required()
def create_resume():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    template_name = data.get("template", "classic")
    resume_data = {k: v for k, v in data.items() if k != "template"}

    resume = Resume(
        user_id=user_id,
        resume_data=resume_data,
        template=template_name
    )

    db.session.add(resume)          
    db.session.commit()

    html = render_html(template_name, data)

    return jsonify({
        "message": "Resume created",
        "resume_id": resume.id,
        "resume_html": html
    }), 201

@app.route("/api/resumes", methods=["GET"])
@jwt_required()
def get_all_resumes():
    user_id = int(get_jwt_identity())

    resumes = Resume.query.filter_by(user_id=user_id).all()

    result = []
    for r in resumes:
        data= r.resume_data

        html = render_html(r.template, data)

        result.append({
            "id": r.id,
            "template": r.template,
            "created_at": r.created_at,
            "resume_html": html
        })

    return jsonify(result), 200

@app.route("/api/resume/<int:resume_id>", methods=["GET"])
@jwt_required()
def get_resume(resume_id):
    user_id = int(get_jwt_identity())

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=user_id
    ).first()

    if not resume:
        return jsonify({"error": "Not found"}), 404

    data = {**resume.resume_data, "template": resume.template}
    html = render_html(resume.template, data)

    return jsonify({**data, "resume_html": html}), 200

@app.route("/api/resume/<int:resume_id>", methods=["PUT"])
@jwt_required()
def update_resume(resume_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=user_id
    ).first()

    if not resume:
        return jsonify({"error": "Not found"}), 404

    template_name = data.get("template", "classic")

    resume.resume_data = {k: v for k, v in data.items() if k != "template"}
    resume.template = template_name

    html = render_html(template_name, data)

    db.session.commit()

    return jsonify({"resume_html": html,
                    "id":resume.id,
                    'template': resume.template}), 200

@app.route("/api/resume/<int:resume_id>", methods=["DELETE"])
@jwt_required()
def delete_resume(resume_id):
    user_id = int(get_jwt_identity())

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=user_id
    ).first()

    if not resume:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(resume)
    db.session.commit()

    return jsonify({"message": "Deleted"}), 200


@app.route("/api/resume/<int:resume_id>/download", methods=["GET"])
@jwt_required()
def download_resume(resume_id):

    user_id = int(get_jwt_identity())

    resume = Resume.query.filter_by(
        id=resume_id,
        user_id=user_id
    ).first()

    if not resume:
        return jsonify({"error": "Not found"}), 404

    data = {**resume.resume_data, "template": resume.template}
    html = render_html(resume.template, data)

    from playwright.sync_api import sync_playwright
    import tempfile
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.set_content(html, wait_until="networkidle")

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf_path = temp_pdf.name
        temp_pdf.close()

        # Generate PDF
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "10mm",
                "bottom": "10mm",
                "left": "10mm",
                "right": "10mm"
            }
        )

        browser.close()

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf"
    )



if __name__ == "__main__":
    app.run(debug=True)
