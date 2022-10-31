
from flask import Flask, render_template, redirect, request
from pymongo import MongoClient 
#import random
from random import randint

app = Flask(__name__, template_folder='templates')

firstname = " "
add = 0
res = " "
patientid = " "
@app.route('/', methods=['GET',"POST"])
def reg():
    return render_template('registration.html')
    

@app.route('/register', methods=['GET',"POST"])
def register():
    global patientid
    global firstname
    middlename=""
    lastname = " "
    gender = " "
    email=""
    birthday = " "
    pin = " "
    #patient_id=0
    patientid = randint(10000000000000,99999999999999)
    print(patientid)
    if request.method == "POST":
    
        firstname = request.form['firstname']
        middlename=request.form['middlename']
        lastname = request.form['lastname']
        gender = request.form['gender']
        email=request.form['email']
        birthday = request.form['birthday']
        pin = request.form["pin"]
      #  patient_id=randompatient_id(14)
        
        Collection.insert_one(
            {"firstname" : firstname,
        "lastname":lastname,
        "middlename":middlename,
        "gender":gender,
        "email":email,
        "birthday":birthday,
        "pin":pin}
        )
    return render_template('index.html',id = patientid ,firstname = firstname,middlename= middlename,lastname =  lastname,email1 = email,gender1 = gender,birthday1 = birthday,pin1 = pin)

    

@app.route('/index', methods=['GET',"POST"])
def home():
    
    if request.method == "POST":
        
        while True:
            first = request.form.get('first')
            second = request.form.get('second')
            third = request.form.get('third')
            fourth = request.form.get('fourth')
            fifth = request.form.get('fifth')
            sixth = request.form.get('sixth')
            Collection.update_one(
                {"firstname":firstname},
            {"$set": {"first" :first,
            'second': second,
             "third":third,
            "fourth":fourth,
            "fifth":fifth,
            "sixth":sixth}}
       
        )
            score = float(first) + float(second)+float(third)+float(fourth) + float(fifth)+float(sixth)
            global add
            add=score  
            global res
            if score>4:
                res="screening needed"
                Collection.update_one(
                {"firstname":firstname},
                {"$set": {"total_count" :add}})
            else:
                res="no need to screen"
                Collection.update_one(
                #{"firstname":firstname},{"$set": {"total_count" :add}})
                 {"id" :patientid,},{"$set": {"total_count" :add,"res" :res}})
            return render_template('result.html', add1=add,res=res)
    return render_template('registration.html')



@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('registration.html')


if __name__ == "__main__":
     try:
        client = MongoClient("mongodb://localhost:27017")
        db = client['mongopython']
        Collection = db["Patient"]
        # client.server_info() #trigger exception if it cannot connect to database
        
     except Exception as e:
        print(e)
        print("Error - Cannot connect to database")
     app.run(debug=True)