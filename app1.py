from flask import Flask, render_template, redirect, request, url_for, session
import random
app = Flask(__name__)
app.secret_key = "srinubabu@123"
users = {
    '123':'123',
    '124':'124'
}
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']#get data from browser
        password = request.form['password']
        if username in users:# data validation
            if users[username] == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'), msg = "invalid credenticals")
        return redirect(url_for('login'), msg = "invalid credenticals")
            
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password= request.form['password']
        email = request.form['email']
        otp = random.randint(1000, 9999) # generated otp
        session['otp'] = otp
        # send this opt via email
        print('----------otp:', session['otp'])
        return redirect(url_for('verifyOtp'))

    return render_template('register.html')

@app.route("/register/verifyOtp", methods=['GET','POST'])
def verifyOtp():
    if 'otp' not in session:
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        enterd_otp = int(request.form['otp'])
        if enterd_otp == session['otp']:
            # add data into users table
            return render_template('login.html',msg ="User registred successfully")
        return redirect(url_for('verifyOtp'),msg ="In valid OTP")
    return render_template('verifyotp.html')
        

        
        

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return "User in dash board"

if __name__ == '__main__':
    app.run(debug=True)


