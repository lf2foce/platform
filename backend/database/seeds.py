from backend.database.models import Project, User, File
from backend.database.core import SessionLocal, engine, Base


# def fake_user():
#     from sqlalchemy.orm import Session

#     user1 = User(email="a@a.a", hashed_password="123456")
#     project1 = Project(
#         title="Project 1", description="test", run_path="test1.py", owner_id=1
#     )
#     with Session(engine) as session:
#         session.add(user1)
#         session.add(project1)
#         session.commit()


def seed_example():
    from sqlalchemy.orm import Session

    user1 = User(email="a@a.a", hashed_password="123456")
    project1 = Project(
        title="Project 1", description="test", run_path="project1/main.py", owner_id=1
    )
    file1 = File(
        name="file 1", description="x", run_path="project1/main.py", author_id=1
    )
    file2 = File(
        name="file 2", description="y", run_path="project1/test.py", author_id=1
    )
    with Session(engine) as session:
        session.add(user1)
        session.add(project1)
        session.add(file1)
        session.add(file2)
        session.commit()
