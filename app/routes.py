from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import ParentRegistrationForm, StudentRegistrationForm, \
    TeacherRegistrationForm, AdminRegistrationForm, LoginForm, \
    ResetPasswordForm, RequestPasswordResetForm, VerifyForm,\
    UnsubscribeForm, EmailForm
from app.models import User, Parent, Student, Teacher, Admin,\
    Newsletter_Subscriber, Email
from app.email import send_subscriber_private_email, send_user_private_email
from app.email import send_password_reset_email, thank_you_client
from werkzeug.urls import url_parse
from app.twilio_verify_api import request_email_verification_token, \
    check_email_verification_token
from app import app, db



# =========================================
# NEWSLETTER HOME PAGE
# =========================================


# Client signs up for the newsletter

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    """
    Display the home page
    Seen by anonymous users
    """
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    # Newsletter form
    if request.method == "POST":
        newsletter_client = request.form["email"]
        # Send email owner a verification token in their inbox
        request_email_verification_token(newsletter_client)
        # Save user email in session
        # User not saved in database just yet
        session["email"] = newsletter_client
        flash("Please check your email inbox for a verification code")
        # Email owner redirected to confirm token received
        return redirect(url_for('verify_email_token'))
    return render_template("home.html", title="Home")



# Subscriber verifies email ownership

@app.route("/verify-email-token", methods=["GET", "POST"])
def verify_email_token():
    """
    Subscriber verifies their email address by
    providing token sent to their inbox
    """
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    form = VerifyForm()
    if form.validate_on_submit():
        email = session["email"]
        if check_email_verification_token(email, form.token.data):
            # Get the subscriber's username
            # It will be used to send a personalized thank you note for signing up
            client_email = session['email']
            client_username = client_email.split("@")[0].capitalize()

            # Add subscriber to the database
            client = Newsletter_Subscriber(email=session["email"])
            client.num_newsletter = 0 # determines what newsletter to be sent
            db.session.add(client)
            db.session.commit()
            # Remove the subscriber from the session since they are now added to the database
            del session["email"]

            # Send subscriber a thank you email
            thank_you_client(client, client_username)

            flash("Thank you for subscribing to our newsletter. Please check you inbox.")
            return redirect(url_for("home"))
        form.token.errors.append("Invalid token.")
    return render_template(
        "auth/register_anonymous_user.html",
        title="Verify Your Email",
        form=form)



# Subscriber can unsubscribe from the email newsletter

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    """Client can stop receiving newsletters"""
    if current_user.is_authenticated:
        flash('You need to logout first to unsubscribe from our newsletters.')
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    if request.method == 'POST':
        client = Newsletter_Subscriber.query.filter_by(email=request.form["email"]).first()
        if client is None:
            flash("Please enter the email used during subscription.")
            return redirect(url_for("unsubscribe"))
        if client.is_active():
            client.active = False
            db.session.commit()
            flash("You have successfully unsubscribed from our newsletters.")
            return redirect(url_for("home"))
        if client.active is False:
            flash("You are already unsubscribed from our newsletters")
            return redirect(url_for('home'))
    return render_template(
        "auth/unsubscribe.html",
        title="Unsubscribe From Our Newsletters")

# =========================================
# END OF NEWSLETTER HOME PAGE
# =========================================



# =========================================
# USER AUTHENTICATION
# =========================================


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))



# Login

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login logic"""
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("dashboard")
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {user.username}.')
        return redirect(next_page)
    return render_template(
        "auth/login.html",
        title="Login",
        form=form)



# Logout

@app.route('/logout')
@login_required
def logout():
    """Logged in user can log out"""
    logout_user()
    return redirect(url_for('login'))


# Request password reset

@app.route("/request-password-reset", methods=["GET", "POST"])
def request_password_reset():
    """
    Registerd user can request for a password reset
    If not registered, the application will not tell the anonymous user why not
    """
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send user an email
            send_password_reset_email(user)
        # Conceal database information by giving general information
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("login"))
    return render_template(
        "auth/register_anonymous_user.html",
        title="Request Password Reset",
        form=form)



# Reset password

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Time-bound link to reset password requested by an active user sent to their inbox
    """
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("login"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset. Login to continue")
        return redirect(url_for("login"))
    return render_template(
        "auth/register_anonymous_user.html",
        title="Reset Password",
        form=form)



# Parent registration

@app.route("/register/parent", methods=["GET", "POST"])
def register_parent():
    """Parent registration logic"""
    if current_user.is_authenticated:
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    form = ParentRegistrationForm()
    if form.validate_on_submit():
        parent = Parent(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            current_residence=form.current_residence.data)
        parent.set_password(form.password.data)
        db.session.add(parent)
        db.session.commit()
        # Send parent and email with login credentials
        # send_login_details(parent)
        flash(f"Successfully registered as {parent.username}! "
              "Check your email for further guidance.")
        return redirect(url_for('home'))
    return render_template(
        "auth/register_anonymous_user.html",
        title="Register As A Parent",
        form=form)


# Student registration

@app.route("/register/student", methods=["GET", "POST"])
@login_required
def register_student():
    """Student registration logic"""
    if current_user.type == "parent":
        form = StudentRegistrationForm()
        if form.validate_on_submit():
            student = Student(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                age=form.age.data,
                school=form.school.data,
                coding_experience=form.coding_experience.data,
                program=form.program.data,
                program_schedule=form.program_schedule.data,
                cohort=form.cohort.data,
                parent=current_user)
            student.set_password(form.password.data)
            db.session.add(student)
            db.session.commit()
            # Send parent and email with login credentials
            # send_login_details(student)
            flash(f"Successfully registered your child as {student.username}! "
                "An email has been sent to them on the next steps to take.")
            return redirect(url_for('parent_profile'))
    else:
        flash("You do not have access to this page!")
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "admin":
            return redirect(url_for("admin_profile"))
    return render_template(
        "auth/register_current_user.html",
        title="Register Your Child",
        form=form)



# Teacher registration

@app.route("/register/teacher", methods=["GET", "POST"])
@login_required
def register_teacher():
    """Teacher registration logic"""
    if current_user.type == "admin":
        form = TeacherRegistrationForm()
        if form.validate_on_submit():
            teacher = Parent(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                course=form.course.data,
                current_residence=form.current_residence.data)
            teacher.set_password(form.password.data)
            db.session.add(teacher)
            db.session.commit()
            # Send teacher an email with login credentials
            # send_login_details(parent)
            flash(f"Successfully registered your teacher {teacher.username}! "
                "An email has been sent to the teacher on the next steps.")
            return redirect(url_for('all_teachers'))
    else:
        flash("You do not have access to this page!")
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
    return render_template(
        "auth/register_current_user.html",
        title="Register A Teacher",
        form=form)


# Admin registration

@app.route("/register/admin", methods=["GET", "POST"])
@login_required
def register_admin():
    """Admin registration logic"""
    if current_user.type == "admin":
        form = AdminRegistrationForm()
        if form.validate_on_submit():
            admin = Parent(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                current_residence=form.current_residence.data,
                department=form.department.data)
            admin.set_password(form.password.data)
            db.session.add(admin)
            db.session.commit()
            # Send admin an email with login credentials
            # send_login_details(admin)
            flash(f"Successfully registered your teacher {admin.username}! "
                "An email has been sent to the teacher on the next steps.")
            return redirect(url_for('all_admins'))
    else:
        flash("You do not have access to this page!")
        if current_user.type == "student":
            return redirect(url_for("student_profile"))
        if current_user.type == "teacher":
            return redirect(url_for("teacher_profile"))
        if current_user.type == "parent":
            return redirect(url_for("parent_profile"))
    return render_template(
        "auth/register_current_user.html",
        title="Register An Admin",
        form=form)


# =========================================
# END OF USER AUTHENTICATION
# =========================================




# =========================================
# AUTHENTICATED USERS
# =========================================

# ==========
# DASHBOARD
# ==========


# --------------------------------------
# Teacher profile
# --------------------------------------


@app.route("/dashboard/teacher/profile")
@login_required
def teacher_profile():
    return render_template(
        "teacher/profile.html",
        title="Teacher Profile"
    )


# Compose direct email to teacher

@app.route(
    '/dashboard/compose-direct-email/<email>',
    methods=['GET', 'POST'])
@login_required
def compose_direct_email_to_teacher(email):
    """Write email to individual teacher"""
    # Get the teacher
    teacher = Teacher.query.filter_by(email=email).first()
    teacher_username = teacher.email.split('@')[0].capitalize()

    form = EmailForm()
    form.signature.choices = [
        (current_user.first_name.capitalize(), current_user.first_name.capitalize())]
    if form.validate_on_submit():
        email = Email(
            subject=form.subject.data,
            body=form.body.data,
            closing=form.closing.data,
            signature=form.signature.data,
            bulk='Teacher Email',
            author=current_user)
        db.session.add(email)
        db.session.commit()
        flash(f'Sample private email to {teacher_username} saved')
        return redirect(url_for('emails_to_individual_teachers'))
    return render_template(
        'admin/email_teacher.html',
        title='Compose Private Email',
        form=form,
        teacher=teacher)


# List of emails sent out to individual teachers

@app.route('/dashboard/emails-to-individual-teachers')
@login_required
def emails_to_individual_teachers():
    """Emails sent out to individual teachers"""
    emails_sent_to_individual_teachers = Email.query.filter_by(
        bulk='Teacher Email').all()
    emails = len(emails_sent_to_individual_teachers)
    return render_template(
        'admin/individual_teacher_email.html',
        title='Emails Sent To Individual Teachers',
        emails_sent_to_individual_teachers=emails_sent_to_individual_teachers,
        emails=emails)


# List of all teachers

@app.route("/dashboard/all-teachers")
@login_required
def all_teachers():
    teachers = Teacher.query.all()
    all_registered_teachers = len(teachers)
    return render_template(
        "admin/all_teachers.html",
        title="All Teachers",
        all_registered_teachers=all_registered_teachers
    )


# Deactivate teacher

@app.route("/dashboard/deactivate-teacher/<username>")
@login_required
def deactivate_teacher(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    teacher.active = False
    db.session.add(teacher)
    db.session.commit()
    flash(f'{teacher.username} has been deactivated as a teacher')
    return redirect(url_for('all_teachers'))


# Reactivate admin

@app.route("/dashboard/reactivate-teacher/<username>")
@login_required
def reactivate_teacher(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    teacher.active = True
    db.session.add(teacher)
    db.session.commit()
    flash(f'{teacher.username} has been reactivated as a teacher')
    return redirect(url_for('all_teachers'))



# Delete teacher

@app.route("/dashboard/delete-teacher/<username>")
@login_required
def delete_teacher(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    db.session.delete(teacher)
    db.session.commit()
    flash(f'{teacher.username} has been deleted as a teacher')
    return redirect(url_for('all_teachers'))


# --------------------------------------
# End of teacher profile
# --------------------------------------


# --------------------------------------
# Admin profile
# --------------------------------------


@app.route("/admin/profile")
@login_required
def admin_profile():
    return render_template(
        "admin/profile.html",
        title="Admin Profile"
    )


# Compose direct email to admin

@app.route(
    '/dashboard/compose-direct-email-to-an-admin/<email>',
    methods=['GET', 'POST'])
@login_required
def compose_direct_email_to_admin(email):
    """Write email to individual admin"""
    # Get the teacher
    admin = Admin.query.filter_by(email=email).first()
    admin_username = admin.email.split('@')[0].capitalize()

    form = EmailForm()
    form.signature.choices = [
        (current_user.first_name.capitalize(), current_user.first_name.capitalize())]
    if form.validate_on_submit():
        email = Email(
            subject=form.subject.data,
            body=form.body.data,
            closing=form.closing.data,
            signature=form.signature.data,
            bulk='Admin Email',
            author=current_user)
        db.session.add(email)
        db.session.commit()
        flash(f'Sample private email to {admin_username} saved')
        return redirect(url_for('emails_to_individual_admin'))
    return render_template(
        'admin/email_admin.html',
        title='Compose Private Email',
        form=form,
        admin=admin)


# List of emails sent out to individual admin

@app.route('/dashboard/emails-to-individual-admins')
@login_required
def emails_to_individual_admins():
    """Emails sent out to individual admins"""
    emails_sent_to_individual_admins = Email.query.filter_by(
        bulk='Admin Email').all()
    emails = len(emails_sent_to_individual_admins)
    return render_template(
        'admin/individual_admin_email.html',
        title='Emails Sent To Individual Admins',
        emails_sent_to_individual_admins=emails_sent_to_individual_admins,
        emails=emails)


# List all admins

@app.route("/dashboard/all-admins")
@login_required
def all_admins():
    admins = Admin.query.all()
    all_registered_admins = len(admins)
    return render_template(
        "admin/all_admins.html",
        title="All Admins",
        admins=admins,
        all_registered_admins=all_registered_admins
    )


# Deactivate admin

@app.route("/dashboard/deactivate-admin/<username>")
@login_required
def deactivate_admin(username):
    admin = Admin.query.filter_by(username=username).first_or_404()
    admin.active = False
    db.session.add(admin)
    db.session.commit()
    flash(f'{admin.username} has been deactivated as an admin')
    return redirect(url_for('all_admins'))


# Reactivate admin

@app.route("/dashboard/reactivate-admin/<username>")
@login_required
def reactivate_admin(username):
    admin = Admin.query.filter_by(username=username).first_or_404()
    admin.active = True
    db.session.add(admin)
    db.session.commit()
    flash(f'{admin.username} has been reactivated as an admin')
    return redirect(url_for('all_admins'))



# Delete admin

@app.route("/dashboard/delete-admin/<username>")
@login_required
def delete_admin(username):
    admin = Admin.query.filter_by(username=username).first_or_404()
    db.session.delete(admin)
    db.session.commit()
    flash(f'{admin.username} has been deleted as an admin')
    return redirect(url_for('all_admins'))


# --------------------------------------
# End of admin profile
# --------------------------------------


# --------------------------------------
# All parents
# --------------------------------------


# Compose direct email to parent

@app.route(
    '/dashboard/compose-direct-email-to-a-parent/<email>',
    methods=['GET', 'POST'])
@login_required
def compose_direct_email_to_parent(email):
    """Write email to individual parent"""
    # Get the parent
    parent = Parent.query.filter_by(email=email).first()
    parent_username = parent.email.split('@')[0].capitalize()

    form = EmailForm()
    form.signature.choices = [
        (current_user.first_name.capitalize(), current_user.first_name.capitalize())]
    if form.validate_on_submit():
        email = Email(
            subject=form.subject.data,
            body=form.body.data,
            closing=form.closing.data,
            signature=form.signature.data,
            bulk='Parent Email',
            author=current_user)
        db.session.add(email)
        db.session.commit()
        flash(f'Sample private email to {parent_username} saved')
        return redirect(url_for('emails_to_individual_parent'))
    return render_template(
        'admin/email_parent.html',
        title='Compose Private Email',
        form=form,
        parent=parent)


# List of emails sent out to individual parent

@app.route('/dashboard/emails-to-individual-parents')
@login_required
def emails_to_individual_parents():
    """Emails sent out to individual parents"""
    emails_sent_to_individual_parent = Email.query.filter_by(
        bulk='Parent Email').all()
    emails = len(emails_sent_to_individual_parent)
    return render_template(
        'admin/individual_parent_email.html',
        title='Emails Sent To Individual Parents',
        emails_sent_to_individual_parent=emails_sent_to_individual_parent,
        emails=emails)


# List all parents

@app.route("/dashboard/all-parents")
@login_required
def all_parents():
    parents = Parent.query.all()
    all_registered_parents = len(parents)
    return render_template(
        "admin/all_parents.html",
        title="All Parents",
        parents=parents,
        all_registered_parents=all_registered_parents
    )


# Deactivate parent

@app.route("/dashboard/deactivate-parent/<username>")
@login_required
def deactivate_parent(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    parent.active = False
    db.session.add(parent)
    db.session.commit()
    flash(f'{parent.username} has been deactivated as a parent')
    return redirect(url_for('all_parents'))


# Reactivate parent

@app.route("/dashboard/reactivate-parent/<username>")
@login_required
def reactivate_parent(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    parent.active = True
    db.session.add(parent)
    db.session.commit()
    flash(f'{parent.username} has been reactivated as a parent')
    return redirect(url_for('all_parents'))



# Delete parent

@app.route("/dashboard/delete-parent/<username>")
@login_required
def delete_parent(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    db.session.delete(parent)
    db.session.commit()
    flash(f'{parent.username} has been deleted as a parent')
    return redirect(url_for('all_parents'))


# --------------------------------------
# End of all parents
# --------------------------------------


# --------------------------------------
# All students
# --------------------------------------


# Compose direct email to student

@app.route(
    '/dashboard/compose-direct-email-to-a-student/<email>',
    methods=['GET', 'POST'])
@login_required
def compose_direct_email_to_student(email):
    """Write email to individual student"""
    # Get the parent
    student = Student.query.filter_by(email=email).first()
    student_username = student.email.split('@')[0].capitalize()

    form = EmailForm()
    form.signature.choices = [
        (current_user.first_name.capitalize(), current_user.first_name.capitalize())]
    if form.validate_on_submit():
        email = Email(
            subject=form.subject.data,
            body=form.body.data,
            closing=form.closing.data,
            signature=form.signature.data,
            bulk='Student Email',
            author=current_user)
        db.session.add(email)
        db.session.commit()
        flash(f'Sample private email to {student_username} saved')
        return redirect(url_for('emails_to_individual_student'))
    return render_template(
        'admin/email_student.html',
        title='Compose Private Email',
        form=form,
        student=student)


# List of emails sent out to individual student

@app.route('/dashboard/emails-to-individual-students')
@login_required
def emails_to_individual_students():
    """Emails sent out to individual student"""
    emails_sent_to_individual_student = Email.query.filter_by(
        bulk='Student Email').all()
    emails = len(emails_sent_to_individual_student)
    return render_template(
        'admin/individual_student_email.html',
        title='Emails Sent To Individual Students',
        emails_sent_to_individual_student=emails_sent_to_individual_student,
        emails=emails)



@app.route("/dashboard/all-students")
@login_required
def all_students():
    students = Student.query.all()
    all_registered_students = len(students)
    return render_template(
        "admin/all_students.html",
        title="All Students",
        students=students,
        all_registered_students=all_registered_students
    )


# Deactivate student

@app.route("/dashboard/deactivate-student/<username>")
@login_required
def deactivate_student(username):
    student = Student.query.filter_by(username=username).first_or_404()
    student.active = False
    db.session.add(student)
    db.session.commit()
    flash(f'{student.username} has been deactivated as a student')
    return redirect(url_for('all_students'))


# Reactivate student

@app.route("/dashboard/reactivate-student/<username>")
@login_required
def reactivate_student(username):
    student = Student.query.filter_by(username=username).first_or_404()
    student.active = True
    db.session.add(student)
    db.session.commit()
    flash(f'{student.username} has been reactivated as a student')
    return redirect(url_for('all_students'))



# Delete student

@app.route("/dashboard/delete-parent/<username>")
@login_required
def delete_students(username):
    student = Student.query.filter_by(username=username).first_or_404()
    db.session.delete(student)
    db.session.commit()
    flash(f'{student.username} has been deleted as a student')
    return redirect(url_for('all_students'))


# --------------------------------------
# End of all students
# --------------------------------------


# --------------------------------------
# Bulk emails
# --------------------------------------


# Bulk emails to all teachers

@app.route("/dashboard/bulk-emails/teachers")
@login_required
def bulk_emails_teachers():
    bulk_emails_sent_to_all_teachers = Email.query.filter_by(
        bulk='Parent Email').all()
    emails = len(bulk_emails_sent_to_all_teachers)
    return render_template(
        "admin/bulk_emails_teachers.html",
        title="Bulk Emails Sent To All Teachers",
        bulk_emails_sent_to_all_teachers=bulk_emails_sent_to_all_teachers,
        emails=emails
    )


# Bulk emails to all admins

@app.route("/dashboard/bulk-emails/admins")
@login_required
def bulk_emails_admins():
    bulk_emails_sent_to_all_admins = Email.query.filter_by(
        bulk='Admin Email').all()
    emails = len(bulk_emails_sent_to_all_admins)
    return render_template(
        "admin/bulk_emails_admins.html",
        title="Bulk Emails Sent To All Admins",
        bulk_emails_sent_to_all_admins=bulk_emails_sent_to_all_admins,
        emails=emails
    )


# Bulk emails to all parents

@app.route("/dashboard/bulk-emails/parents")
@login_required
def bulk_emails_parents():
    bulk_emails_sent_to_all_parents = Email.query.filter_by(
        bulk='Parent Email').all()
    emails = len(bulk_emails_sent_to_all_parents)
    return render_template(
        "admin/bulk_emails_parents.html",
        title="Bulk Emails Sent To All Parents",
        bulk_emails_sent_to_all_parents=bulk_emails_sent_to_all_parents,
        emails=emails
    )


# Bulk emails to all students

@app.route("/dashboard/bulk-emails/students")
@login_required
def bulk_emails_students():
    bulk_emails_sent_to_all_students = Email.query.filter_by(
        bulk='Parent Email').all()
    emails = len(bulk_emails_sent_to_all_students)
    return render_template(
        "admin/bulk_emails_students.html",
        title="Bulk Emails Sent To All Students",
        bulk_emails_sent_to_all_students=bulk_emails_sent_to_all_students,
        emails=emails
    )



# --------------------------------------
# End of bulk emails
# --------------------------------------


# ----------------------------------------
# Newsletter subscribers
# ----------------------------------------


@app.route("/dashboard/newsletter-subscribers")
@login_required
def newsletter_subscribers():
    subscribers = Newsletter_Subscriber.query.order_by(
        Newsletter_Subscriber.email_confirmed_at.desc()).all()
    num_subscribers = len(subscribers)
    return render_template(
        "admin/newsletter_subscribers.html",
        title="Newsletter Subscribers",
        subscribers=subscribers, 
        num_subscribers=num_subscribers
    )



# Resubscribe

@app.route('/newsletter/resubscription/<email>')
@login_required
def resubscribe_newsletter_subscriber(email):
    """Resubscribe the client to continue receiving newsletters"""
    subscriber = Newsletter_Subscriber.query.filter_by(email=email).first()
    subscriber.active = True
    db.session.commit()
    flash('The subscriber can now continue receiving newsletters')
    return redirect(url_for('email_newsletter_subscribers'))


# Delete subscriber

@app.route('/newsletter/delete/<email>')
@login_required
def delete_newsletter_subscriber(email):
    """Permanently delete client from the database"""
    subscriber = Newsletter_Subscriber.query.filter_by(email=email).first()
    db.session.delete(subscriber)
    db.session.commit()
    flash('The subscriber can now continue receiving newsletters')
    return redirect(url_for('email_newsletter_subscribers'))


# Compose direct email

@app.route(
    '/newsletter/compose-direct-email/<email>',
    methods=['GET', 'POST'])
@login_required
def newsletter_subscriber_compose_direct_email(email):
    """Write email to individual newsletter subscriber"""
    # Get the client (newsletter)
    subscriber = Newsletter_Subscriber.query.filter_by(email=email).first()
    session['subscriber'] = subscriber.email
    subscriber_username = subscriber.email.split('@')[0].capitalize()

    form = EmailForm()
    form.signature.choices = [
        (current_user.first_name.capitalize(), current_user.first_name.capitalize())]
    if form.validate_on_submit():
        email = Email(
            subject=form.subject.data,
            body=form.body.data,
            closing=form.closing.data,
            signature=form.signature.data,
            bulk='Newsletter Subscriber',
            author=current_user)
        db.session.add(email)
        db.session.commit()
        flash(f'Sample private email to {subscriber_username} saved')
        return redirect(url_for('newsletter_subscribers_email_sent_out'))
    return render_template(
        'admin/email_newsletter_subscriber.html',
        title='Compose Private Email',
        form=form,
        subscriber=subscriber)

# ----------------------------------------
# End of Newsletter subscribers
# ----------------------------------------


# ---------------------------------------
# SAMPLE EMAILS
# ---------------------------------------


# List of individual emails sent out

@app.route('/newsletter/individual-email-to-newsletter-subscriber')
@login_required
def newsletter_subscribers_email_sent_out():
    """Emails sent out to individual newsletter subscribers"""
    emails_sent_to_newsletter_subscribers = Email.query.filter_by(
        bulk='Newsletter Subscriber').all()
    emails = len(emails_sent_to_newsletter_subscribers)
    return render_template(
        'admin/individual_newsletter_subscribers_email.html',
        title='Individual Emails Sent To Newsletter Subscribers',
        emails_sent_to_newsletter_subscribers=emails_sent_to_newsletter_subscribers,
        emails=emails)


# Send email to individual subscriber

@app.route('/newsletter/send-email/<id>')
@login_required
def send_email(id):
    """Send email to subscriber from the database"""
    email = Email.query.filter_by(id=id).first()
    subscriber_email = session['subscriber']

    # Update db so that the email is not sent again
    email.allow = True
    db.session.add(email)
    db.session.commit()

    # Send email to subscriber
    subscriber_username = session['subscriber'].split('@')[0].capitalize()
    send_subscriber_private_email(email, subscriber_email, subscriber_username)

    # Notify user that email has been sent
    flash(f'Email successfully sent to {subscriber_email}')
    del session['subscriber']
    return redirect(url_for('newsletter_subscribers_email_sent_out'))


# Edit sample email

@app.route('/edit-email/<id>', methods=['GET', 'POST'])
@login_required
def edit_email(id):
    """Edit email to user from the database"""
    email = Email.query.filter_by(id=id).first()
    form = EmailForm()
    form.signature.choices = [
        (current_user.first_name.capitalize(), current_user.first_name.capitalize())]
    if form.validate_on_submit():
        email.subject = form.subject.data
        email.body = form.body.data
        email.closing = form.closing.data
        email.signature = form.signature.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('newsletter_subscribers_email_sent_out'))
    if request.method == 'GET':
        form.subject.data = email.subject
        form.body.data = email.body
        form.signature.data = email.signature
    return render_template(
        'admin/edit_email.html', title='Edit Sample Email', form=form)


# Delete email from database

@app.route('/delete-email/<id>')
@login_required
def delete_email(id):
    """Delete email to user from the database"""
    email = Email.query.filter_by(id=id).first()
    db.session.delete(email)
    db.session.commit()
    flash('Email successfully deleted')
    del session['subscriber']
    return redirect(url_for('newsletter_subscribers_email_sent_out'))


# ==========
# END OF DASHBOARD
# ==========




# =========================================
# END OF AUTHENTICATED USERS
# =========================================
