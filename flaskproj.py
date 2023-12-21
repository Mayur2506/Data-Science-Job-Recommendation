from flask import Flask, render_template, flash, redirect, request, session
from flask_mysqldb import MySQLdb
from flask_mysqldb import MySQL
from forms import *
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import correlation
import MySQLdb.cursors
import pearson
import hamming
import manhattan
import minkowski
import jaccard
import collaborative
import re
import hashlib
import string
# import analysiss

app = Flask(__name__)
# app instance of flask

app.config['SECRET_KEY'] = '4e9c884a5a717a5980682d23c6cbf27c'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'JOBS'

info_list = [
    {
        'Student': '',
        'MIS': '',
        'Address': '',
        'Gender': '',
        'Contact': ''
    }
]

mysql = MySQL(app)


@app.route('/')
@app.route('/home')
# 2 paths handled by same home() function
def home():
    try:
        if session['loggedin']:
            pass

    except:
        info_list = [
            {
                'Student': '',
                'MIS': '',
                'Address': '',
                'Gender': '',
                'Contact': ''
            }
        ]
        flash("Log in to see your profile page", 'warning')
        return render_template('home.html', title='Home', posts=info_list)

    MIS = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Student_Info WHERE MIS = %s', (MIS, ))
    a = cursor.fetchone()
    if not a:
        info_list = [
            {
                'Student': '',
                'MIS': MIS,
                'Address': '',
                'Gender': '',
                'Contact': ''
            }
        ]
    else:
        info_list = [
            {
                'Student': f"{a[1]}  {a[2]}  {a[3]}",
                'MIS': a[0],
                'Address': a[4],
                'Gender': a[5],
                'Contact': a[7]
            }
        ]
    return render_template('home.html', title='Home', posts=info_list)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # check if validated

    msg = ''
    if request.method == 'POST' and form.validate_on_submit() and form.MIS.data and form.password.data:
        MIS = form.MIS.data
        password = form.password.data
        salt = "5gz"
        db_password = password+salt
        h = hashlib.md5(db_password.encode())
        password = h.hexdigest()
        
        cursor = mysql.connection.cursor()
        #cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Login WHERE MIS = % s', (MIS, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            flash(msg, 'danger')
            return render_template('register.html', title='Register', form=form)
        if not form.MIS.data.isnumeric():
            flash("MIS should contain digits only.", 'danger')
            return render_template('register', title='Register', form=form)
        else:
            #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
            cursor.execute(
                'INSERT INTO Login(MIS, password) VALUES (% s, % s)', (MIS, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            # print(msg)
            flash(msg, 'success')
            return redirect('home')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        flash(msg, 'warning')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['loggedin']:
            flash(
                f"You are already logged in as {session['username']}", 'danger')
            return redirect('home')
    except:
        pass
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and form.MIS.data and form.password.data and form.validate_on_submit():
        MIS = form.MIS.data
        password = form.password.data

        salt = "5gz"
        db_password = password+salt
        h = hashlib.md5(db_password.encode())
        password = h.hexdigest()
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM Login WHERE MIS = % s AND password = % s', (MIS, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[0]
            msg = 'Logged in successfully !'
            flash(msg, 'success')
            cursor.execute(
                'SELECT MIS, first_name, middle_name, last_name, student_address FROM Student_Info WHERE MIS = % s', (MIS,))
            stud_data = cursor.fetchone()
            if stud_data:
                global info_list
                info_list[0]['Student'] = f"{stud_data[1]}  {stud_data[2]}  {stud_data[3]}"
                info_list[0]['MIS'] = stud_data[0]
                info_list[0]['Address'] = stud_data[4]
            else:
                info_list[0]['MIS'] = account[0]
                info_list[0]['Student'] = "Full Name"
                flash("Please enter your details.", 'success')
            return redirect('home')
        else:
            msg = 'Incorrect username / password !'
            flash(msg, 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/personal', methods=['GET', 'POST'])
def personal():
    form = PersonalForm()
    try:
        if session['loggedin']:
            pass

    except:
        flash("Log in to edit personal information", 'warning')
        return render_template('personal.html', title='Personal Details', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        MIS = session['username']
        if not form.contact_no.data.isnumeric():
            flash("Contact should contain digits only.", 'danger')
            return render_template('personal.html', title='Personal Details', form=form)
        try:
            cursor.execute(
                'SELECT * FROM Student_Info WHERE MIS = %s', (MIS, ))
            a = cursor.fetchone()
            print("0")
            if not a:
                cursor.execute('INSERT INTO Student_Info VALUES(% s, % s, %s, %s, %s, %s, %s, %s)', (
                    MIS, form.first_name.data, form.middle_name.data, form.last_name.data, form.student_address.data, form.gender.data.capitalize(), form.isNRI.data, form.contact_no.data))
                mysql.connection.commit()
                print("1")
            else:
                cursor.execute('UPDATE Student_Info SET first_name = %s, middle_name = %s, last_name = %s, student_address = %s, gender = %s, isNRI = %s, contact_no = %s where MIS = %s',
                               (form.first_name.data, form.middle_name.data, form.last_name.data, form.student_address.data, form.gender.data.capitalize(), form.isNRI.data, form.contact_no.data, MIS))
                #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
                print("2")
                mysql.connection.commit()
        except Exception as e:
            flash(f"Not committed to database as {e}", 'danger')
            return render_template('personal.html', title='Personal Details', form=form)

        cursor.execute(
            'SELECT * FROM Student_Info WHERE MIS = % s', (form.MIS.data,))
        stud_data = cursor.fetchone()
        if stud_data:
            global info_list
            info_list = [
                {
                    'Student': f"{stud_data[1]}  {stud_data[2]}  {stud_data[3]}",
                    'MIS': stud_data[0],
                    'Address': stud_data[4],
                    'Gender': stud_data[5],
                    'Contact': stud_data[7]
                }
            ]
        return redirect('home')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('personal.html', title='Personal Details', form=form)



@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    form = RecommendForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'danger')
        return redirect('home')
    if request.method == 'POST' and form.validate_on_submit():
        user_skills = form.skills.data.split(",")
        user_experience=form.years_of_experience.data
        jobs_df = pd.read_csv('data2.csv')
        user_job_location = 'Pune'
        filtered_jobs_df = jobs_df[(jobs_df['experience'].apply(lambda x: int(x.split('-')[0])) >= user_experience)]
        filtered_jobs_df = filtered_jobs_df.assign(location_similarity=np.where(filtered_jobs_df['location'].apply(lambda x: x[0]) == user_job_location, 1, 0))
        filtered_jobs_df = filtered_jobs_df.assign(location_similarity=filtered_jobs_df['location_similarity'] * 0.1) 
        filtered_jobs_df = filtered_jobs_df.drop(columns=['job_title'])
        count_vect = CountVectorizer()
        skills_bow = count_vect.fit_transform(filtered_jobs_df['skills'].apply(lambda x: ' '.join(eval(x))))
        user_skills_bow = count_vect.transform([' '.join(user_skills)])
        cosine_sim = cosine_similarity(skills_bow, user_skills_bow)
        filtered_jobs_df = filtered_jobs_df.assign(similarity=cosine_sim.flatten())
        filtered_jobs_df = filtered_jobs_df.sort_values(['similarity', 'location_similarity', 'experience'], ascending=[False, False, True])
        filtered_jobs_df = filtered_jobs_df.drop(columns=['location_similarity','url','Unnamed: 8'])
        recommended_jobs = filtered_jobs_df.head(5)
        table_html = recommended_jobs.to_html(index=False)
        table_html_c=pearson.pearson(user_experience,user_skills)
        table_html_d=manhattan.manhattan(user_experience,user_skills)
        table_html_e=jaccard.jaccard(user_experience,user_skills)
        table_html_f=hamming.hamming(user_experience,user_skills)
        table_html_g=minkowski.minkowski(user_experience,user_skills)

        return render_template('show.html', title='Jobs Available',table_html=table_html,table_html_c=table_html_c,table_html_d=table_html_d,table_html_e=table_html_e,table_html_f=table_html_f,table_html_g=table_html_g)  

    return render_template('recommend.html', title='Find Jobs', form=form)


@app.route('/jrecommend', methods=['GET', 'POST'])
def jrecommend():
    form = JrecommendForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'danger')
        return redirect('home')
    if request.method == 'POST' and form.validate_on_submit():
        user_id = form.userid.data
        table_html,table_html1,years_of_exp,skills=collaborative.py(user_id)
        print(years_of_exp,skills)
        table_html2=pearson.pearson(years_of_exp,skills)
        return render_template('show1.html', title='Jobs Available',table_html=table_html,table_html_c=table_html1,table_html_g=table_html2) 

# table_html_g=table_html2
    return render_template('jrecommend.html', title='Find Jobs', form=form)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'danger')
        return redirect('home')
    return render_template('plot.html', title='Jobs Analysis')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        if session['loggedin']:
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)
    except:
        flash("You are not logged in", 'danger')
    return redirect('login')


# Run directly using python
if __name__ == '__main__':
    app.run(debug=True)
