from flask import Flask, request, render_template, url_for, redirect, session,flash
import mysql.connector as c
import hashlib


new = Flask(__name__)
new.secret_key = 'supersecretkey'


try:
    con = c.connect(
        host = 'localhost',
        user = 'root',
        password = 'ankit@2004',
        auth_plugin="mysql_native_password"
    ) 
    
except c.Error as e:
    print("Error connecting to MySQL database:", e)
    
try:
    cursor = con.cursor()
    cursor.execute('create database if not exists flask')
    cursor.execute('use flask')
    qry = '''
    create table if not exists user_details(
        username varchar(30),
        name varchar(30),
        email varchar(40),
        password varchar(255)
    )
    '''
    cursor.execute(qry)
except Exception as e:
    print("Error in creating Database or table", e)
    
    
@new.route('/')
def main():
    if 'name' in session:
        return redirect(url_for('home'))
    else:
        return render_template('default.html', name = "Login/Signup")
        


@new.route('/login', methods=['GET','POST'])
def login():
    cursor = con.cursor()
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if not username or not password:
            return render_template('index.html',error="Username and Password required")
        p_hex = hashlib.sha256(password.encode()).hexdigest()
        qry = '''
        select username, password, name, email from user_details
        where username = %s and password = %s
        '''
        cursor.execute(qry, (username, p_hex))
        data = cursor.fetchone()
        if not data:
            flash("❌ User Not found.")
            return redirect(url_for('login'))
        else:
            # SUCCESS LOGIN
            session['username'] = data[0]
            session['name'] = data[2]
            session['email'] = data[3]
            if remember :
                session.permanent = True
            else:
                session.permanent = False
            return redirect(url_for('home'))
    return render_template('index.html')



@new.route('/register', methods=['GET','POST'])
def register():
    cursor = con.cursor()
    if request.method == 'POST':
        errors = []

        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username:
            flash("Username is Required")
        elif not username[0].isalpha():
            flash("❌ Username must start with a letter.")
        else:
            cursor.execute(
                'select username from user_details where username = %s',
                (username,)
            )
            if cursor.fetchone():
                flash("❌ Username already exists. Please login.")
                return redirect(url_for('login'))

        if not email:
            flash("Email is Required")
        elif not email.endswith(".com"):
            flash("❌ Invalid Email.")

        if not password:
            flash("❌ Password is required.")

        if errors:
            return render_template('register.html', error= errors)

        # Hash password
        p_hex = hashlib.sha256(password.encode()).hexdigest()

        qry = '''
        insert into user_details (username, name, email, password)
        values (%s, %s, %s, %s)
        '''
        cursor.execute(qry, (username, name.title(), email, p_hex))
        con.commit()
        flash("✅ Registration Successful. Please Login.")
        return redirect(url_for('login'))

    return render_template('register.html')



@new.route('/home')
def home():
    if 'name' in session:
        return render_template('main.html', name = session['name'], username = session['username'], email = session['email'])
    else:
        return redirect(url_for('login'))


@new.route('/notes')
def notes():
    if 'name' in session:
        return render_template('notes.html', name = session['name'])
    else:
        return redirect(url_for('login'))
    #return render_template('notes.html')


@new.route('/papers')
def papers():
    if 'name' in session:
        return render_template('papers.html', name = session['name'])
    else:
        return redirect(url_for('login'))
    #return render_template('papers.html')


@new.route('/resources')
def resources():
    if 'name' in session:
        return render_template('resources.html', name = session['name'])
    else:
        return redirect(url_for('login'))
    #return render_template('resources.html')


@new.route('/cgpa')
def cgpa():
    if 'name' in session:
        return render_template('cgpa2.html', name = session['name'])
    else:
        return redirect(url_for('login'))
    #return render_template('cgpa2.html')


@new.route('/logout')
def logout():
    session.clear()
    flash("✅ You have been logged out.")
    return redirect(url_for('main'))


if __name__ == '__main__':
    new.run(host="0.0.0.0", port=5000, debug=True)