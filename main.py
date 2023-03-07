from app import app, db
from app import cli
from app.models import User, Parent, Student, Teacher, Admin, Newsletter_Subscriber,\
    Email


cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Admin=Admin,
        Teacher=Teacher,
        Parent=Parent,
        Student=Student,
        Newsletter_Subscriber=Newsletter_Subscriber,
        Email=Email
        )
