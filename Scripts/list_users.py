from TodoApp.database import SessionLocal
from TodoApp.models import Users

session = SessionLocal()
for u in session.query(Users).all():
    print(u.id, u.username, u.hashed_password)