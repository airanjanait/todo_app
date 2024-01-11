from flask import Flask,request,render_template,redirect,flash,url_for
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user,login_required
from function import Function
import hashlib
from flask import g
import os

obj=Function()
app=Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.urandom(24)

registered_users=[]


class User(UserMixin):
    try:
        def __init__(self,id,Email,Password):
            self.id=id
            self.Email=Email
            self.Password=Password
    except Exception as e:
            e

@app.before_request
def before_request():
    try:
        g.user=current_user
    except Exception as e:
        e

@login_manager.user_loader
def load_user(user_id):
    try:
        with app.app_context():
            user = obj.user_id(user_id)
           
        if user: 
           return User(user.id,user.Email,user.Password)
    except Exception as e:
        e
        
        
    
@app.route('/login',methods=['POST','GET'])
def login():
        if request.method=='POST':
            Email=request.form.get("Email")
            Password=request.form.get("Password")
            salt = "5gz"
            dataBase_password = Password+salt
            hashed = hashlib.md5(dataBase_password.encode())
            pwd=hashed.hexdigest()
            with app.app_context():
                user=obj.user_login(Email,pwd)
            if user:
                user_data={
                    "id":user.id,
                    "Email":user.Email,
                    "Password":Password
                }
                login_user(User(user_data['id'],user_data['Email'],user_data['Password']))
                return render_template('welcome.html')
            else:
                flash('Invalid credentials','error')
                return render_template('login.html')
        return render_template('login.html')
    
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
    


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

# @app.errorhandler(404)
# def page_not_found():
#     return redirect('/')


#________________home page _____________________

@app.route("/")
def home3():
    return render_template("registration.html")

#_______________registration ____________________

@app.route("/register",methods=['POST','GET'])
def registrationinfo():
    if request.method=="POST":
        Name=request.form.get("Name")
        Password=request.form.get("Password")
        Email=request.form.get("Email")

        salt = "5gz"
        dataBase_password = Password+salt
        hashed = hashlib.md5(dataBase_password.encode())
        pwd=hashed.hexdigest()
        
        data_front=Name,Email,pwd
        
        verify_data=obj.verify_register(Name,Email,pwd)
        if verify_data:
            verify_Name=verify_data.Name
            verify_Email=verify_data.Email
            verify_Password=verify_data.Password
            data_back=verify_Name,verify_Email,verify_Password
            if data_front==data_back:
                return render_template("reapet_registration.html")
        else:
            obj.registration(Name,Email,pwd)
            return render_template("welcome.html")
 
        
    return render_template("registration.html")

#___________________ add task ________________________

@app.route("/addtask",methods=['POST','GET'])
@login_required
def addtasks():
    if request.method=="POST":
        TaskName=request.form.get("TaskName")
        StartDate=request.form.get("StartDate")
        StartTime=request.form.get("StartTime")
        DueDate=request.form.get("DueDate")
        data=obj.addtask(TaskName,StartDate,StartTime,DueDate)
    return render_template("addtask.html")

#__________________ fetch task detail ______________________

@app.route("/fetchtask/<ID>")
@login_required
def fetchtaskdetailes(ID):
    task_info=obj.fetchtask(ID)
    return render_template("fetchtask.html",task_info=task_info)



#___________________list of all tasks together___________________

@app.route("/tasklist")
@login_required
def alltasklist():
    tasks=obj.taskilist()
    flash('Data Deleted ','error')
    return render_template('tasklist.html',tasks=tasks)
    
    
#____________________delete task ____________________________

@app.route("/deletetask/<ID>")
def delete(ID):
    data=obj.DeleteTask(ID)
    flash(data,'errors')
    return redirect("/tasklist")

#_________________fetch to update and to update________________

@app.route("/fetchtoupdate/<ID>")
def fetchtoupdate(ID):
    data=obj.fetchonetask(ID)
    return render_template("update.html",data=data)

@app.route("/updatetask",methods=['POST','GET'])
def update():
    data=""
    if request.method=="POST":
        ID=request.form.get("ID")
        TaskName=request.form.get("TaskName")
        StartDate=request.form.get("StartDate")
        StartTime=request.form.get("StartTime")
        DueDate=request.form.get("DueDate")
        obj.update_task(ID,TaskName,StartDate,StartTime,DueDate)
    return redirect("/tasklist")
    
#__________________make history of tasks_______________________


@app.route("/maketaskhistory/<ID>")
def makehistoryoftask(ID):
    data1=""
    data1=obj.makehistory(ID)
    flash(data1,'Data')
    return redirect(url_for("fetchtaskdetailes",ID=ID))

#_____________________get history of task______________________

@app.route("/gettaskhistory",methods=['POST','GET'])
@login_required
def gettaskhistory():
    data=""
    if request.form.get("date"):
        date=request.form.get("date")
        
        data=obj.gettaskhistory(date)
        if "On there is not any task assigned" in data:
            return data
    return render_template("gettaskhistory.html",data=data)

if __name__=="__main__":
    app.run(debug=True)