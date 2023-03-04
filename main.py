from app import app, db
from app.models import User, Parent, Student, Teacher, Admin, Client


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Admin=Admin,
        Teacher=Teacher,
        Parent=Parent,
        Student=Student,
        Client=Client
        )
