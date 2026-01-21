
from flask import Flask, render_template, redirect, request, url_for, session
import random
from database.tables import create_tables
from database.utility import addUser
from database.utility import checkUserStatus, getPassowordFromDB,updatePassword
from database.utility import addNotesInDB
from emailsend import emailSend

from itsdangerous import URLSafeTimedSerializer,BadSignature,SignatureExpired


app = Flask(__name__)
app.secret_key = "srinubabu@123"

# 
serializer = URLSafeTimedSerializer(app.secret_key)



@app.route('/')
def home():
    return render_template('home.html')

# ---------------- LOGIN ----------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = request.args.get('msg')

    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        if checkUserStatus(username=username):
            if getPassowordFromDB(username=username) == password:
                token = serializer.dumps(username, salt="login-token")
                

                return redirect(url_for('view_notes', token=token))
            else:
                return redirect(url_for('login', msg="Invalid credentials"))
        else:
            return redirect(url_for('login', msg="Invalid credentials"))

    return render_template('login.html', msg=msg)

# ---------------- OTP ----------------
def generate_otp_token(email):
    otp = random.randint(1000, 9999)
    token = serializer.dumps(
        {"email":email, "otp":otp},
        salt ="register_otp"
    )
    return otp, token


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['reg_username'] = request.form['username']
        session['reg_password'] = request.form['password']
        session['reg_email'] = request.form['email']

        otp, token = generate_otp_token(session['reg_email'])
        session['register_otp_token'] = token

        print("Register OTP token:", token)
        
        body = f"""
                Dear customer {session['reg_username']},

                Notes Management account verification OTP:{otp}
                This otp is valid for 2 minutes.

                Regards
                Notes Management App.
            """
        print(emailSend(
            to_email=session['reg_email'],
            header= "Notes Management OTP verification",
            body = body
        ))

        return redirect(url_for('verifyOtp'))

    return render_template('register.html')

# ---------------- VERIFY OTP ----------------
@app.route("/register/verifyOtp", methods=['GET', 'POST'])
def verifyOtp():
    if 'register_otp_token' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        try:

            data = serializer.loads(
                session['register_otp_token'],
                salt = "register_otp",
                max_age = 120
            )

            if str(data['otp']) == entered_otp:
                # save user in database
                add_user = addUser(username=session['reg_username'],
                                email= session['reg_email'],
                                password=session['reg_password'])
                if add_user:

                    # clear session
                    
                    session.pop('reg_username')
                    session.pop('reg_password')
                    session.pop('reg_email')

                    return redirect(url_for('login', msg="Registration successful"))
        except BadSignature:
            return render_template('verifyotp.html', msg="Invalid OTP (token is tampred)")
        except SignatureExpired:
            return render_template('verifyotp.html', msg="Invalid OTP (OTP time expired)")
        return render_template('verifyotp.html', msg="Invalid OTP")

    return render_template('verifyotp.html')


def verify_login_token(token):
    try:
        email = serializer.loads(
            token,
            salt="login-token",
            max_age=7200
        )
        return email
    except (BadSignature, SignatureExpired):
        return None
# ---------------- DASHBOARD ----------------
@app.route('/dashboard/<token>')
def view_notes(token):
    email = verify_login_token(token)
    if not email:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/dashboard/addnote/<token>')
def add_note(token):
    email = verify_login_token(token)
    if not email:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        
    return redirect(url_for('dashboard', token=token))

    return render_template('add_note.html', token=token)
#add notes
def addNotesInDB(title, content, email):
    # function to add notes in database
    try:
        get_userid_query = """SELECT USERID FROM USERS
                        WHERE EMAIL = %s";"""
        cursor.execute(get_userid_query, (email,))
        user = cursor.fetchone()

    except Exception as e:
        print("Error fetching user ID:", e)
        return False

# ---------------- LOGOUT ----------------


# ---------------------forgot password -----------------
@app.route('/forgotPassword', methods = ['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # creating forgot-password token
        if checkUserStatus(username=email):

            token = serializer.dumps(email, salt="forgot-password")
            
            reset_link = url_for('reset_password', token= token, _external =True)
            # send reset link via email
            body = f"""
                    Dear customer,

                    Notes Management Password reset request,
                    Password reset link:{reset_link}

                    This otp is valid for 10  minutes.
                    Don't replay to this email.

                    Regards
                    Notes App.
                """
            emailSend(
                to_email=email,
                header = "Notes app Password reset request!",
                body = body
            )
            return redirect(url_for('login', msg = "successfully Password reset link send"))
        return redirect(url_for('login', msg = "User not registered"))

    return render_template('forgot_password.html')


# ---------------reset password link -------------
@app.route('/forgotPassowd/resetPassword/<token>', methods=['GET','POST'])
def reset_password(token):
    try:
        email = serializer.loads(token,
                                 salt = "forgot-password",
                                 max_age=600
                                )
    except SignatureExpired:
        return redirect(url_for('forgot_password', msg = "Expired time"))
    except BadSignature:
        return redirect(url_for('forgot_password', msg = "Invalid link"))
    if request.method == 'POST':
        new_password = request.form['password']

        # update password in database
        if updatePassword(email=email, password=new_password):
            return redirect(url_for("login", msg = "Reset Password updated"))
        return redirect(url_for("login", msg = "Reset Password not updated"))

    
        # redirect to login page

    return render_template('reset_password.html', token = token)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
