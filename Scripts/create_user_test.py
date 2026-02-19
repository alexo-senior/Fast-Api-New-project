import os, sys

# ensure imports resolve exactly as when the app is started (cwd=TodoApp)
os.chdir(os.path.join(os.path.dirname(__file__), "TodoApp"))
sys.path.insert(0, os.getcwd())

from database import SessionLocal
from models import Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# try to add a user with a username that already exists
session = SessionLocal()
try:
    user = Users(
        email="foo@bar.com",
        username="CodingwithAlexis",  # duplicate
        first_name="Foo",
        last_name="Bar",
        role="user",
        hashed_password=bcrypt_context.hash("password123"),
        is_active=True
    )
    session.add(user)
    session.commit()
    print("User added")
except Exception as e:
    print("caught exception:", repr(e))
    session.rollback()
finally:
    session.close()