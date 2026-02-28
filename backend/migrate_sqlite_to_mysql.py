from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.resume import Resume

# SQLite connection (old database)
sqlite_engine = create_engine("sqlite:///app.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# MySQL connection (XAMPP)
mysql_engine = create_engine("mysql+pymysql://root:@localhost/resume_builder?charset=utf8mb4")
MySQLSession = sessionmaker(bind=mysql_engine)
mysql_session = MySQLSession()

print("Starting migration...")

# Copy Users
users = sqlite_session.query(User).all()
for user in users:
    mysql_session.merge(user)

# Copy Resumes
resumes = sqlite_session.query(Resume).all()
for resume in resumes:
    mysql_session.merge(resume)

mysql_session.commit()

print("Migration completed successfully!")
