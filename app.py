from flask import Flask,render_template,request,session,redirect,url_for,make_response
from mysql.connector import connect 

con=connect(host='localhost',
            port=3306,
            database='raiseup',
            user='root')
myapp=Flask(__name__)
myapp.secret_key= '2b449a7d94480a7a0ec53c7329ed'
session={}
@myapp.route("/home")
@myapp.route("/")
def hello():
    global l
    l=0
    return render_template("index.html")
# print("hello")
@myapp.route("/log",methods=["GET","POST"])
def myform():
    if request.method=="POST":
        name=request.form["logname"]
        phone=request.form["logphone"]
        email=request.form["logemail"]
        password=request.form["logpass"]
        cur=con.cursor()
        cur.execute("insert into register values(%s,%s,%s,%s)",(name,phone,email,password))
        con.commit()
        session["name"]=name
        return render_template("index.html",user=name)
    else:
        return None

l=0
name=''
@myapp.route("/login",methods=["GET","POST"])
def login():
    global l
    l=0
    if request.method=="POST":
        email=request.form["logemail"]
        password=request.form["logpass"]
        # print(email,password)
        cur=con.cursor()
        cur.execute("SELECT * FROM register where email=%s and password=%s",(email,password))
        res=cur.fetchall()
        if res:
            session['name']=res[0][0]
            l=1
            return redirect(url_for('main'))
            # return res[0][0]
        else:
            return render_template("page_not.html")
        
    else:
        return None 


@myapp.route("/connected",methods=["GET","POST"])
def connected():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        contact=request.form["contact"]
        option=request.form["option"]
        cur=con.cursor()
        cur.execute("insert into connected values(%s,%s,%s,%s)",(name,email,contact,option))
        con.commit()
        return redirect(url_for("getHelp"))
    else:
        return None

@myapp.route("/admin",methods=["GET","POST"])
def admin():
    if request.method=="POST":
        user=request.form["adminuser"]
        password=request.form["adminpass"]
        cur=con.cursor()
        cur.execute("SELECT * FROM admin where user=%s and password=%s",(user,password))
        res=cur.fetchall()
        print(res)
        if res:
            curs=con.cursor()
            curs.execute("SELECT * FROM connected")
            data=curs.fetchall()
            return render_template("userlist.html",data=data)
            # return render_template("welcome.html")
        else:
            return render_template("page_not.html")
    else:
        return None
        


@myapp.route('/display_table')
def display_table():
    # Retrieve rows from database
    curs=con.cursor()
    curs.execute("SELECT * FROM connected")
    data=curs.fetchall()
    # Render template with rows
    print(data)
    return render_template('userlist.html',data=data)

@myapp.route('/delete/<string:name>', methods=['POST'])
def delete_row(name):
    # Delete row from database
    curs=con.cursor()
    curs.execute("DELETE FROM connected where name=%s",(name,))
    # delete_row_from_database(row_id)
    con.commit()
    
    # Redirect to the page that displayed the table
    return redirect(url_for('display_table'))

# @myapp.before_request
# def block_request():
#     if request.path.startswith('/main'):
#         return redirect('/')

@myapp.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@myapp.route("/adminLog")
def adminlogin():
    return render_template("admin.html")
    
@myapp.route("/getHelp")
def getHelp():
    return render_template("getHelp.html")

@myapp.route("/main")
def main():
    if(l==1):
        name=session.get("name")
        return render_template("main.html",name=name)
    else:
        return render_template("page_not.html")

@myapp.route("/logout")
def logout():
    session.get("name",None)
    # response = make_response(render_template('index.html'))
    # response.headers['cache_control'] = 'no-cache'
    # return response
    # return render_template("index.html",name=None)
    return redirect(url_for('index'))

@myapp.route("/sexualViolence")
def sexualviolence():
    return render_template("sexualviolence.html")

@myapp.route("/domesticViolence")
def domesticviolence():
    return render_template("domesticviolence.html")

@myapp.route("/childMarriage")
def childMarriage():
    return render_template("childmarriage.html")

@myapp.route("/cybercrime")
def cybercrime():
    return render_template("cybercrime.html")

@myapp.route("/error")
def error():
    return render_template("error.html")

@myapp.route("/genderdisc")
def genderdesc():
    return render_template("genderdisc.html")

@myapp.route("/womentrafficking")
def womentrafficking():
    return render_template("womentrafficking.html")

if __name__=="__main__":
    myapp.run(debug=True)
    