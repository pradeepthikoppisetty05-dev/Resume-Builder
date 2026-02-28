from extensions import db
from datetime import datetime

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref("resumes", cascade="all, delete", passive_deletes=True)
    )
    resume_data = db.Column(db.JSON, nullable=False)
    template = db.Column(db.String(50), default="classic")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
