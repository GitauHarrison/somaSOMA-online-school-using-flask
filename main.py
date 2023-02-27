from app import app, db
from app.models import User, Parent, Student, Teacher, Admin


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Admin=Admin,
        Teacher=Teacher,
        Parent=Parent,
        Student=Student
        )
