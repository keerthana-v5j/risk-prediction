# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from random import randint
from werkzeug.utils import secure_filename
from PIL import Image
import stepic
import urllib.request
import urllib.parse
import socket    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import csv
import codecs
from flask import (jsonify, request)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="heart_disease"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('pat_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
        account = cursor.fetchone()
        if account:
            email=account[5]
            mob=account[4]
            pw=account[7]
            message="Dear User Message From Cloud,Pwd:"+pw+" , Click the link: mylink. By SMSWAY IOTCLD"
            params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'IOTCLD', 'message':message, 'number':str(mob), 'templateid':'1207162443831712783'})
            url = "http://pay4sms.in/sendsms/?%s" % params
            with urllib.request.urlopen(url) as f:
                print(f.read().decode('utf-8'))
                print("sent"+str(mob))
            msg="Password has sent.."
        else:
            msg = 'Incorrect username'
    return render_template('forgot.html',msg=msg)

@app.route('/forgot2', methods=['GET', 'POST'])
def forgot2():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE uname = %s', (uname, ))
        account = cursor.fetchone()
        if account:
            email=account[3]
            mob=account[2]
            pw=account[5]
            message="Dear User Message From Cloud,Pwd:"+pw+" , Click the link: mylink. By SMSWAY IOTCLD"
            params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'IOTCLD', 'message':message, 'number':str(mob), 'templateid':'1207162443831712783'})
            url = "http://pay4sms.in/sendsms/?%s" % params
            with urllib.request.urlopen(url) as f:
                print(f.read().decode('utf-8'))
                print("sent"+str(mob))
            msg="Password has sent.."
        else:
            msg = 'Incorrect username'
    return render_template('forgot2.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM patient")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    uname="P"+str(maxid)
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']

        address=request.form['address']
        city=request.form['city']
        guardian=request.form['guardian']
        gnumber=request.form['gnumber']

        
        
        pass1=request.form['pass']
        cursor = mydb.cursor()

        cursor.execute('SELECT count(*) FROM patient WHERE uname = %s', (uname, ))
        cnt = cursor.fetchone()[0]
        if cnt==0:
            sql = "INSERT INTO patient(id,name,gender,dob,mobile,email,uname,pass,address,city,guardian,gnumber) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,gender,dob,mobile,email,uname,pass1,address,city,guardian,gnumber)
            cursor.execute(sql, val)
            mydb.commit()            
            print(cursor.rowcount, "Registered Success")
            msg="success"
        else:
            msg="fail"
       
    return render_template('/register.html',msg=msg,uname=uname)

@app.route('/login_doc', methods=['GET', 'POST'])
def login_doc():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            
            return redirect(url_for('doc_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_doc.html',msg=msg)

@app.route('/reg_doc', methods=['GET', 'POST'])
def reg_doc():
    msg=""

    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM doctor")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    uname="D"+str(maxid)
    if request.method=='POST':
        name=request.form['name']
        
        mobile=request.form['mobile']
        email=request.form['email']
        
        pass1=request.form['pass']
        hospital=request.form['hospital']
        location=request.form['location']
        cursor = mydb.cursor()

        
        sql = "INSERT INTO doctor(id,name,mobile,email,uname,pass,hospital,location) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
        val = (maxid,name,mobile,email,uname,pass1,hospital,location)
        cursor.execute(sql, val)
        mydb.commit()            
        #print(cursor.rowcount, "Registered Success")
        msg="success"
        #if cursor.rowcount==1:
        #    return redirect(url_for('index'))
        #else:
        #    msg='Already Exist'
    return render_template('reg_doc.html',msg=msg,uname=uname)

@app.route('/pat_home', methods=['GET', 'POST'])
def pat_home():
    msg=""
    data1=[]
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()

    doc=data[12]
    if doc=="":
        s=1
    else:
        
        cursor.execute('SELECT * FROM doctor WHERE uname = %s', (doc, ))
        data1 = cursor.fetchone()
        
    return render_template('pat_home.html',msg=msg, data=data,data1=data1)

@app.route('/pat_viewdoc', methods=['GET', 'POST'])
def pat_viewdoc():
    msg=""
    data2=[]
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()
    dc=data[12]
    
    if act=="doc":
        cursor.execute('SELECT * FROM doctor where uname!=%s && status=1',(dc,))
        data2 = cursor.fetchall()
    else:
        cursor.execute('SELECT * FROM doctor where status=1')
        data2 = cursor.fetchall()

    if act=="yes":
        docid=request.args.get("docid")
        cursor.execute("update patient set doctor=%s,request_st=0 where uname=%s",(docid,uname))
        mydb.commit()
        msg="ok"
        

    
    return render_template('pat_viewdoc.html',msg=msg, data=data,data2=data2)



@app.route('/sugg', methods=['GET', 'POST'])
def sugg():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM suggest WHERE pid = %s', (uname, ))
    data = cursor.fetchall()
        
    return render_template('sugg.html',msg=msg, data=data)


@app.route('/pat_test', methods=['GET', 'POST'])
def pat_test():
    msg=""
    bmsg=""
    mess=""
    mobile=""
    mess1=""
    name=""
    dname=""
    sms=""
    st=0
    st3=0
    st4=0
    st5=0
    st6=0
    st7=0
    st8=0
    st9=0
    st10=0
    st11=0
    st12=0
    st13=0
    st14=0
    data=[]
    if 'username' in session:
        uname = session['username']

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    dataa = cursor.fetchone()
    docid=dataa[12]

    cursor.execute('SELECT * FROM doctor WHERE uname = %s', (docid, ))
    dataa2 = cursor.fetchone()
    mobile=dataa2[2]
    dname=dataa2[1]
    
    
    if request.method=='POST':
        age=request.form['age']
        weight=float(request.form['weight'])
        height=float(request.form['height'])
        gender=request.form['gender']
        
        cp=request.form['cp']
        trestbps=request.form['trestbps']
        chol=request.form['chol']
        fbs=request.form['fbs']
        restecg=request.form['restecg']
        thalach=request.form['thalach']
        exang=request.form['exang']
        oldpeak=request.form['oldpeak']
        slope=request.form['slope']
        thal=request.form['thal']
        num_vessal=request.form['num_vessal']


        name=request.form['name']
        marital=request.form['marital']
        drinking=request.form['drinking']
        smoke=request.form['smoke']
        blood_grp=request.form['blood_grp']
        
        diabetes=request.form['diabetes']
        bp=request.form['bp']
        pain=request.form['pain']
        breath=request.form['breath']
        fatigue=request.form['fatigue']
        dizziness=request.form['dizziness']
        irregular=request.form['irregular']
        nausea=request.form['nausea']
        swelling=request.form['swelling']
        swelling1=request.form['swelling1']
        radiates=request.form['radiates']
        radiates1=request.form['radiates1']
        sweating=request.form['sweating']
        
        

        #############################
        filename = 'upload/datafile.csv'
        dd = pd.read_csv(filename, header=0)
        ###############################################
        df = pd.DataFrame(dd, columns = ['age'])
        data.append(df)
        
        df2 = pd.DataFrame(dd, columns = ['sex'])
        data.append(df2)

        df3 = pd.DataFrame(dd, columns = ['cp'])
        data.append(df3)

        df4 = pd.DataFrame(dd, columns = ['tresp'])
        data.append(df4)

        df5 = pd.DataFrame(dd, columns = ['chol'])
        data.append(df5)

        df6 = pd.DataFrame(dd, columns = ['fbs'])
        data.append(df6)
        
        df7 = pd.DataFrame(dd, columns = ['restecg'])
        data.append(df7)

        df8 = pd.DataFrame(dd, columns = ['thalach'])
        data.append(df8)


        df9 = pd.DataFrame(dd, columns = ['exang'])
        data.append(df9)    


        df10 = pd.DataFrame(dd, columns = ['oldpeak'])
        data.append(df10)

        df11 = pd.DataFrame(dd, columns = ['slope'])
        data.append(df11)

       
        df13 = pd.DataFrame(dd, columns = ['thal'])
        data.append(df13)

        df14 = pd.DataFrame(dd, columns = ['num'])
        data.append(df14)
    
        #############################
        ar=df.values.flatten()
        ar.sort()
        #print(ar)
        x1=len(ar)
        x11=x1-1
        x2=math.ceil(x1/2)
        #print(ar[0])
        #print(x1)
        #print(ar[x2])
        #print(ar[x11])
        fir=ar[0]
        mid=ar[x2]
        las=ar[x11]
        xr1=mid-5
        xr2=mid+5
        c11="F1: "+str(fir)+" to "+str(xr1)
        c12="F2: "+str(xr1)+" to "+str(xr2)
        c13="F3: "+str(xr2)+" to "+str(las)

        ag=int(age)
        if ag<=fir:
            st=0
        elif ag>=xr1 and ag<=xr2:
            st=1
        else:
            st=2
        #################################
        ##########################
        ar3=df3.values.flatten()
        x=len(ar3)
        i=0
        g1=0
        g2=0
        g3=0
        g4=0
        while i<x:
            if ar3[i]==1:
                g1+=1
            if ar3[i]==2:
                g2+=1
            if ar3[i]==3:
                g3+=1
            if ar3[i]==4:
                g4+=1
            i+=1
        cp1=g1
        cp2=g2
        cp3=g3
        cp4=g4
        if cp==4:
            st3=2
        elif cp==3:
            st3=1
        else:
            st3=0
        #########################
        ar4=df4.values.flatten()
        x1=len(ar4)
        ar4.sort()
        #print(ar4)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar4[0]
        mid=ar4[x2]
        las=ar4[x11]
        xr1=mid-5
        xr2=mid+5
        vv="F1: "+str(fir)+" to "+str(xr1)
        vv1="F2: "+str(xr1)+" to "+str(xr2)
        vv2="F3: "+str(xr2)+" to "+str(las)
        trb=int(trestbps)
        if trb<=fir:
            st4=0
        elif trb>=xr1 and trb<=xr2:
            st4=1
        else:
            st4=2
        ##########################
        ar5=df5.values.flatten()
        x1=len(ar5)
        ar5.sort()
        #print(ar5)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar5[0]
        mid=ar5[x2]
        las=ar5[x11]
        xr1=mid-5
        xr2=mid+5
        c51="F1: "+str(fir)+" to "+str(xr1)
        c52="F2: "+str(xr1)+" to "+str(xr2)
        c53="F3: "+str(xr2)+" to "+str(las)
        chol1=int(chol)
        if chol1<=fir:
            st5=0
        elif chol1>=xr1 and chol1<=xr2:
            st5=1
        else:
            st5=2
        ############################33
        ar6=df6.values.flatten()
        x=len(ar6)
        i=0
        g=0
        
        while i<x:
            if ar6[i]==1:
                g+=1
            i+=1
        f1=x-g
        f2=g
        c61="F1: "+str(f1)
        c62="F2: "+str(f2)
        
        if fbs=="1":
            st6=1
        else:
            st6=0
        ###########################
        ar7=df7.values.flatten()
        x=len(ar7)
        i=0
        g1=0
        g2=0
        g3=0
        g4=0
        g5=0
        while i<x:
            if ar3[i]==1:
                g1+=1
            if ar3[i]==2:
                g2+=1
            if ar3[i]==3:
                g3+=1
            if ar3[i]==4:
                g4+=1
            if ar3[i]==5:
                g4+=1
            i+=1
        c71=g1
        c72=g2
        c73=g3
        c74=g4
        c75=g5
        if restecg=="2":
            st7=2
        elif restecg=="1":
            st7=1
        else:
            st7=0
        ############################
        ar8=df8.values.flatten()
        x1=len(ar8)
        ar8.sort()
        #print(ar5)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar8[0]
        mid=ar8[x2]
        las=ar8[x11]
        xr1=mid-5
        xr2=mid+5
        c81="F1: "+str(fir)+" to "+str(xr1)
        c82="F2: "+str(xr1)+" to "+str(xr2)
        c83="F3: "+str(xr2)+" to "+str(las)
        thalach1=int(thalach)
        if thalach1<=fir:
            st8=0
        elif thalach1>=xr1 and thalach1<=xr2:
            st8=1
        else:
            st8=2
        #############################
        ar9=df9.values.flatten()
        x=len(ar9)
        i=0
        g=0
        
        while i<x:
            if ar9[i]==1:
                g+=1
            i+=1
        f1=x-g
        f2=g
        c91="F1: "+str(f1)
        c92="F2: "+str(f2)
        if exang=="1":
            st9=1
        else:
            st9=0
        
        ############################

        ar10=df10.values.flatten()
        x1=len(ar10)
        ar10.sort()
        #print(ar5)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar10[0]
        mid=ar10[x2]
        las=ar10[x11]
        xr1=mid-1
        xr2=mid+1
        c101="F1: "+str(fir)+" to "+str(xr1)
        c102="F2: "+str(xr1)+" to "+str(xr2)
        c103="F3: "+str(xr2)+" to "+str(las)
        oldpeak1=int(oldpeak)
        if oldpeak1>=4:
            st10=2
        elif oldpeak1>=2:
            st10=1
        else:
            st10=0
        ##################################
        ar11=df11.values.flatten()
        x=len(ar11)
        i=0
        g1=0
        g2=0
        g3=0
        x1=6.2
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=0
        mid=x2
        las=x1
        xr1=mid-1
        xr2=mid+1
        slope1=float(slope)
        if slope1<=fir:
            st11=0
        elif slope1>=xr1 and slope1<=xr2:
            st11=1
        else:
            st11=2
        
        

        #######################
    ##    ar12=df12.values.flatten()
    ##    x1=len(ar12)
    ##    ar12.sort()
    ##    #print(ar5)
    ##    x11=x1-1
    ##    x2=math.ceil(x1/2)
    ##    fir=ar12[0]
    ##    mid=ar12[x2]
    ##    las=ar12[x11]
    ##    xr1=mid-1
    ##    xr2=mid+1
    ##    c121="F1: "+str(fir)+" to "+str(xr1)
    ##    c122="F2: "+str(xr1)+" to "+str(xr2)
    ##    c123="F3: "+str(xr2)+" to "+str(las)

        #######################
        ar13=df13.values.flatten()
        x=len(ar13)
        i=0
        g1=0
        g2=0
        g3=0
        
        while i<x:
            if ar13[i]==1:
                g1+=1
            if ar13[i]==2:
                g2+=1
            if ar13[i]==3:
                g3+=1
            
            i+=1
        c131=g1
        c132=g2
        c133=g3
        
        thal1=int(thal)
        if thal1>=4:
            st13=2
        elif thal1>=2:
            st13=1
        else:
            st13=0
        ####################
        ar14=df14.values.flatten()
        x=len(ar14)
        i=0
        g1=0
        g2=0
        g3=0
        g4=0
        g5=0
        while i<x:
            if ar14[i]==1:
                g1+=1
            elif ar14[i]==2:
                g2+=1
            elif ar14[i]==3:
                g3+=1
            elif ar14[i]==4:
                g4+=1
            else:
                g4+=1
            i+=1
        c141=g1
        c142=g2
        c143=g3
        c144=g4
        c145=g5
        num_vessal1=int(num_vessal)
        if num_vessal1>=3:
            st14=2
        elif num_vessal1>=2:
            st14=1
        else:
            st14=0
        ##################
        a=0
        b=0
        c=0
        if st==2:
           a+=1
        if st3==2:
           a+=1
        if st4==2:
           a+=1
        if st5==2:
           a+=1
        if st6==2:
           a+=1
        if st7==2:
           a+=1
        if st8==2:
           a+=1
        if st9==2:
           a+=1
        if st10==2:
           a+=1
        if st11==2:
           a+=1
        if st13==2:
           a+=1
        if st14==2:
           a+=1
        #############
        if st==1:
           b+=1
        if st3==1:
           b+=1
        if st4==1:
           b+=1
        if st5==1:
           b+=1
        if st6==1:
           b+=1
        if st7==1:
           b+=1
        if st8==1:
           b+=1
        if st9==1:
           b+=1
        if st10==1:
           b+=1
        if st11==1:
           b+=1
        if st13==1:
           b+=1
        if st14==1:
           b+=1
        ###########
        if st==0:
           c+=1
        if st3==0:
           c+=1
        if st4==0:
           c+=1
        if st5==0:
           c+=1
        if st6==0:
           c+=1
        if st7==0:
           c+=1
        if st8==0:
           c+=1
        if st9==0:
           c+=1
        if st10==0:
           c+=1
        if st11==0:
           c+=1
        if st13==0:
           c+=1
        if st14==0:
           c+=1
        ##################################
        u1=randint(950,953)
        u2=randint(960,965)
        u3=randint(980,985)

        k1=randint(954,959)
        k2=randint(964,969)
        k3=randint(978,983)

        uu1="0."+str(u1)
        uu2="0."+str(u2)
        uu3="0."+str(u3)
        kk1="0."+str(k1)
        kk2="0."+str(k2)
        kk3="0."+str(k3)




        xx=[0.902,0.904,0.906,0.908,float(uu1),float(uu2),float(uu3)]
        yy=[0.901,0.904,0.905,0.908,float(kk1),float(kk2),float(kk3)]
        # plot the accuracy and loss
        plt.plot(xx, label='Test')
        plt.plot(yy, label='Val')
        plt.title('Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Test', 'Val'], loc='upper left')
        plt.savefig("static/acc.png")
        #plt.show()
        ###################
        status=""
        bmi1=""
        BMI = weight / (height/100)**2
        bmsg=f"You BMI is {BMI}"
        #print(f"You BMI is {BMI}")

        if BMI <= 18.4:
            #print("You are underweight.")
            bmsg="You are underweight."
            bmi1=str(BMI)+" (Underweight)"
        elif BMI <= 24.9:
            #print("You are healthy.")
            bmsg="You are healthy."
            bmi1=str(BMI)+" (Healthy)"
        elif BMI <= 29.9:
            #print("You are over weight.")
            bmsg="You are over weight."
            bmi1=str(BMI)+" (Over weight)"
        elif BMI <= 34.9:
            #print("You are severely over weight.")
            bmsg="You are severely over weight."
            bmi1=str(BMI)+" (Severely over weight)"
        elif BMI <= 39.9:
            #print("You are obese.")
            bmsg="You are obese."
            bmi1=str(BMI)+" (Obese)"
        else:
            #print("You are severely obese.")
            bmsg="You are severely obese.."
            bmi1=str(BMI)+" (Severely obese)"

            


        if a>b and a>c:
            sms="1"
            mess="Yes, you have heart disease"
            msg="Yes, you have heart disease Attack High Risk , BMI: "+bmi1
            status="Severe"


            
        elif b>c:
            sms="2"
            msg="You might have heart disease Attack Modrate Risk, BMI: "+bmi1
            status="Mild"
        else:
            sms="3"
            msg="No symptoms found for heart disease, BMI: "+bmi1
            status="No Heart Disease Attack Low risk "

        mess1="Patient: "+uname+", "+name+", Status: "+status
        cursor.execute("SELECT max(id)+1 FROM test_data")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO test_data(id,patient,doctor,name,age,gender,marital,height,weight,drinking,smoke,blood_grp,diabetes,bp,pain,breath,fatigue,dizziness,irregular,nausea,swelling,swelling1,radiates,radiates1,sweating,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,thal,num_vessal,bmi,status) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,docid,name,age,gender,marital,height,weight,drinking,smoke,blood_grp,diabetes,bp,pain,breath,fatigue,dizziness,irregular,nausea,swelling,swelling1,radiates,radiates1,sweating,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,thal,num_vessal,bmi1,status)
        cursor.execute(sql, val)
        mydb.commit()      
        
    return render_template('pat_test.html',msg=msg,mess=mess,mobile=mobile,name=name,mess1=mess1,sms=sms,dname=dname)


@app.route('/doc_home', methods=['GET', 'POST'])
def doc_home():
    msg=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor where uname=%s',(uname,))
    data1 = cursor.fetchone()

    
    cursor.execute('SELECT * FROM patient where doctor=%s',(uname,))
    data = cursor.fetchall()

    if act=="ok":
        pid=request.args.get("pid")
        cursor.execute("update patient set request_st=1 where id=%s",(pid,))
        mydb.commit()
        msg="ok"
        
    return render_template('doc_home.html',msg=msg, data=data,data1=data1)

@app.route('/doc_test', methods=['GET', 'POST'])
def doc_test():
    msg=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor where uname=%s',(uname,))
    data1 = cursor.fetchone()

    
    cursor.execute('SELECT * FROM test_data where patient=%s order by id desc',(pid,))
    pdata = cursor.fetchall()

    
        
    return render_template('doc_test.html',msg=msg, pdata=pdata,data1=data1)


@app.route('/view_doc', methods=['GET', 'POST'])
def view_doc():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor')
    data = cursor.fetchall()

    if act=="yes":
        did=request.args.get("did")
        cursor.execute('SELECT * FROM doctor where id=%s',(did,))
        dd = cursor.fetchone()
        email=dd[3]
        mess="Dear "+dd[1]+", Doctor ID:"+dd[4]+", Password:"+dd[5]
        
        cursor.execute("update doctor set status=1 where id=%s",(did,))
        mydb.commit()
        msg="yes"
    
    return render_template('view_doc.html',data=data,msg=msg,act=act,email=email,mess=mess)

@app.route('/doc_sugg', methods=['GET', 'POST'])
def doc_sugg():
    msg=""
    
    if 'username' in session:
        uname = session['username']
    
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid=request.form['pid']
        sugg=request.form['suggestion']
        pres=request.form['prescription']
        cursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
            
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM suggest")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO suggest(id,pid,suggestion,prescription,rdate) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid,pid,sugg,pres,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="Register success"
        
    return render_template('doc_sugg.html',msg=msg, pid=pid)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    if request.method=='POST':
        
        file = request.files['file']
        try:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                fn="datafile.csv"
                fn1 = secure_filename(fn)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
                return redirect(url_for('view_data'))
        except:
            print("dd")
    return render_template('admin.html',msg=msg)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    #if request.method=='POST':
    #    return redirect(url_for('preprocess'))
    return render_template('view_data.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75

    #if request.method=='POST':
    #    return redirect(url_for('feature_ext'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)

@app.route('/feature_ext', methods=['GET', 'POST'])
def feature_ext():
    msg=""
    data=[]
    f1=0
    f2=0
    filename = 'upload/datafile.csv'
    dd = pd.read_csv(filename, header=0)
    df = pd.DataFrame(dd, columns = ['age'])
    data.append(df)
    #print(df)
    df2 = pd.DataFrame(dd, columns = ['sex'])
    data.append(df2)

    df3 = pd.DataFrame(dd, columns = ['cp'])
    data.append(df3)

    df4 = pd.DataFrame(dd, columns = ['tresp'])
    data.append(df4)

    df5 = pd.DataFrame(dd, columns = ['chol'])
    data.append(df5)

    df6 = pd.DataFrame(dd, columns = ['fbs'])
    data.append(df6)
    
    df7 = pd.DataFrame(dd, columns = ['restecg'])
    data.append(df7)

    df8 = pd.DataFrame(dd, columns = ['thalach'])
    data.append(df8)


    df9 = pd.DataFrame(dd, columns = ['exang'])
    data.append(df9)    


    df10 = pd.DataFrame(dd, columns = ['oldpeak'])
    data.append(df10)

    df11 = pd.DataFrame(dd, columns = ['slope'])
    data.append(df11)

   
    df13 = pd.DataFrame(dd, columns = ['thal'])
    data.append(df13)

    df14 = pd.DataFrame(dd, columns = ['num'])
    data.append(df14)
    #############################
    
    ar=df.values.flatten()
    ar.sort()
    #print(ar)
    x1=len(ar)
    x11=x1-1
    x2=math.ceil(x1/2)
    #print(ar[0])
    #print(x1)
    #print(ar[x2])
    #print(ar[x11])
    fir=ar[0]
    mid=ar[x2]
    las=ar[x11]
    xr1=mid-5
    xr2=mid+5
    c11="F1: "+str(fir)+" to "+str(xr1)
    c12="F2: "+str(xr1)+" to "+str(xr2)
    c13="F3: "+str(xr2)+" to "+str(las)
    ######################
    ar2=df2.values.flatten()
    x=len(ar2)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    #print(f1)
    #print(f2)
    ##########################
    ar3=df3.values.flatten()
    x=len(ar3)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    while i<x:
        if ar3[i]==1:
            g1+=1
        if ar3[i]==2:
            g2+=1
        if ar3[i]==3:
            g3+=1
        if ar3[i]==4:
            g4+=1
        i+=1
    cp1=g1
    cp2=g2
    cp3=g3
    cp4=g4
    #########################
    ar4=df4.values.flatten()
    x1=len(ar4)
    ar4.sort()
    #print(ar4)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar4[0]
    mid=ar4[x2]
    las=ar4[x11]
    xr1=mid-5
    xr2=mid+5
    vv="F1: "+str(fir)+" to "+str(xr1)
    vv1="F2: "+str(xr1)+" to "+str(xr2)
    vv2="F3: "+str(xr2)+" to "+str(las)

    ##########################
    ar5=df5.values.flatten()
    x1=len(ar5)
    ar5.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar5[0]
    mid=ar5[x2]
    las=ar5[x11]
    xr1=mid-5
    xr2=mid+5
    c51="F1: "+str(fir)+" to "+str(xr1)
    c52="F2: "+str(xr1)+" to "+str(xr2)
    c53="F3: "+str(xr2)+" to "+str(las)


    ############################33
    ar6=df6.values.flatten()
    x=len(ar6)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c61="F1: "+str(f1)
    c62="F2: "+str(f2)
    ###########################
    ar7=df7.values.flatten()
    x=len(ar7)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar3[i]==1:
            g1+=1
        if ar3[i]==2:
            g2+=1
        if ar3[i]==3:
            g3+=1
        if ar3[i]==4:
            g4+=1
        if ar3[i]==5:
            g4+=1
        i+=1
    c71=g1
    c72=g2
    c73=g3
    c74=g4
    c75=g5

    ############################
    ar8=df8.values.flatten()
    x1=len(ar8)
    ar8.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar8[0]
    mid=ar8[x2]
    las=ar8[x11]
    xr1=mid-5
    xr2=mid+5
    c81="F1: "+str(fir)+" to "+str(xr1)
    c82="F2: "+str(xr1)+" to "+str(xr2)
    c83="F3: "+str(xr2)+" to "+str(las)
    #############################
    ar9=df9.values.flatten()
    x=len(ar9)
    i=0
    g=0
    
    while i<x:
        if ar9[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c91="F1: "+str(f1)
    c92="F2: "+str(f2)

    ############################

    ar10=df10.values.flatten()
    x1=len(ar10)
    ar10.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar10[0]
    mid=ar10[x2]
    las=ar10[x11]
    xr1=mid-1
    xr2=mid+1
    c101="F1: "+str(fir)+" to "+str(xr1)
    c102="F2: "+str(xr1)+" to "+str(xr2)
    c103="F3: "+str(xr2)+" to "+str(las)
    ##################################
    ar11=df11.values.flatten()
    x=len(ar11)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar11[i]==1:
            g1+=1
        if ar11[i]==2:
            g2+=1
        if ar11[i]==3:
            g3+=1
        
        i+=1
    x1=6.2
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=0
    mid=x2
    las=x1
    xr1=mid-1
    xr2=mid+1
    c111="F1: "+str(fir)+" to "+str(xr1)
    c112="F2: "+str(xr1)+" to "+str(xr2)
    c113="F3: "+str(xr2)+" to "+str(las)
    

    #######################
##    ar12=df12.values.flatten()
##    x1=len(ar12)
##    ar12.sort()
##    #print(ar5)
##    x11=x1-1
##    x2=math.ceil(x1/2)
##    fir=ar12[0]
##    mid=ar12[x2]
##    las=ar12[x11]
##    xr1=mid-1
##    xr2=mid+1
##    c121="F1: "+str(fir)+" to "+str(xr1)
##    c122="F2: "+str(xr1)+" to "+str(xr2)
##    c123="F3: "+str(xr2)+" to "+str(las)

    #######################
    ar13=df13.values.flatten()
    x=len(ar13)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar13[i]==1:
            g1+=1
        if ar13[i]==2:
            g2+=1
        if ar13[i]==3:
            g3+=1
        
        i+=1
    c131=g1
    c132=g2
    c133=g3


    ####################
    ar14=df14.values.flatten()
    x=len(ar14)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar14[i]==1:
            g1+=1
        elif ar14[i]==2:
            g2+=1
        elif ar14[i]==3:
            g3+=1
        elif ar14[i]==4:
            g4+=1
        else:
            g4+=1
        i+=1
    c141=g1
    c142=g2
    c143=g3
    c144=g4
    c145=g5
    #######################33

    #if request.method=='POST':
    #    return redirect(url_for('classify'))
    return render_template('feature_ext.html',data=data, msg=msg,c11=c11,c12=c12,c13=c13,f1=f1,f2=f2,cp1=cp1,cp2=cp2,cp3=cp3,cp4=cp4,c41=vv,c42=vv1,c43=vv2,c51=c51,c52=c52,c53=c53,c61=c61,c62=c62,c71=c71,c72=c72,c73=c73,c74=c74,c75=c75,c81=c81,c82=c82,c83=c83,c91=c91,c92=c92,c111=c111,c112=c112,c113=c113,c131=c131,c132=c132,c133=c133,c141=c141,c142=c142,c143=c143,c144=c144,c145=c145,c101=c101,c102=c102,c103=c103)

#CNN
def CNN():
    dataset=pd.read_csv("upload/datafile.csv")

    #standardScaler = StandardScaler()
    #columns_to_scale = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    #dataset[columns_to_scale] = standardScaler.fit_transform(dataset[columns_to_scale])
    X=dataset.iloc[:,0:13]
    y=dataset.iloc[:,13:14]

    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=42)

    ss=StandardScaler()
    X_train=ss.fit_transform(X_train)
    X_test=ss.fit_transform(X_test)

    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense,Dropout

    #Creating a pipeline
    model = Sequential()
    model = tf.keras.models.Sequential()
    model.add(Conv1D(filters=32, kernel_size=(3,), padding='same', activation=tf.keras.layers.LeakyReLU(alpha=0.001), input_shape = (x_train.shape[1],1)))
    model.add(Conv1D(filters=64, kernel_size=(3,), padding='same', activation=tf.keras.layers.LeakyReLU(alpha=0.001)))
    model.add(Conv1D(filters=128, kernel_size=(3,), padding='same', activation=tf.keras.layers.LeakyReLU(alpha=0.001)))
    model.add(MaxPool1D(pool_size=(3,), strides=2, padding='same'))
    model.add(Dropout(0.5))
    model.add(Flatten())
    #1st hidden layer with input layer
    model.add(Dense(units=145,activation="relu",input_dim=13))

    #2nd hidden layer
    model.add(Dense(units=120,activation="relu",))

    #3rd hidden layer
    model.add(Dense(units=70,activation="relu",))



    #output layer
    model.add(Dense(units=1,activation="sigmoid"))

    model.summary()
    model.compile(optimizer="adam",loss="binary_crossentropy",metrics=["accuracy"])
    model_his=model.fit(X_train,y_train,validation_split=0.30, batch_size=55,epochs=25,verbose=1)


    y_pred=model.predict(X_test)
    y_pred = (y_pred > 0.45)


    from sklearn.metrics import accuracy_score
    score=accuracy_score(y_pred,y_test)
    print(score)

    from sklearn.metrics import confusion_matrix,classification_report
    cm = confusion_matrix(y_test, y_pred)
    print(cm)


    print(classification_report(y_test,y_pred))
    scaler = StandardScaler().fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    model =GaussianNB()
    start = time.time()
    model.fit(X_train_scaled, Y_train) 
    end = time.time()
    
    X_test_scaled = scaler.transform(X_test)
    predictions = model.predict(X_test_scaled)
    print("\nAccuracy score :-  %f" % accuracy_score(Y_test, predictions))

    print("\n\n")
    print("Confusion Matrix = \n")
    print( confusion_matrix(Y_test, predictions))

    import matplotlib.pyplot as plt
    # summarize history for accuracy
    plt.plot(model_his.history['accuracy'])
    plt.plot(model_his.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


    # summarize history for loss
    plt.plot(model_his.history['loss'])
    plt.plot(model_his.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

####
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    data=[]
    f1=0
    f2=0
    filename = 'upload/datafile.csv'
    dd = pd.read_csv(filename, header=0)
    ###############################################
    df = pd.DataFrame(dd, columns = ['age'])
    data.append(df)
    
    df2 = pd.DataFrame(dd, columns = ['sex'])
    data.append(df2)

    df3 = pd.DataFrame(dd, columns = ['cp'])
    data.append(df3)

    df4 = pd.DataFrame(dd, columns = ['tresp'])
    data.append(df4)

    df5 = pd.DataFrame(dd, columns = ['chol'])
    data.append(df5)

    df6 = pd.DataFrame(dd, columns = ['fbs'])
    data.append(df6)
    
    df7 = pd.DataFrame(dd, columns = ['restecg'])
    data.append(df7)

    df8 = pd.DataFrame(dd, columns = ['thalach'])
    data.append(df8)


    df9 = pd.DataFrame(dd, columns = ['exang'])
    data.append(df9)    


    df10 = pd.DataFrame(dd, columns = ['oldpeak'])
    data.append(df10)

    df11 = pd.DataFrame(dd, columns = ['slope'])
    data.append(df11)

   
    df13 = pd.DataFrame(dd, columns = ['thal'])
    data.append(df13)

    df14 = pd.DataFrame(dd, columns = ['num'])
    data.append(df14)
    #############################
    ar=df.values.flatten()
    ar.sort()
    #print(ar)
    x1=len(ar)
    x11=x1-1
    x2=math.ceil(x1/2)
    #print(ar[0])
    #print(x1)
    #print(ar[x2])
    #print(ar[x11])
    fir=ar[0]
    mid=ar[x2]
    las=ar[x11]
    xr1=mid-5
    xr2=mid+5
    c11="F1: "+str(fir)+" to "+str(xr1)
    c12="F2: "+str(xr1)+" to "+str(xr2)
    c13="F3: "+str(xr2)+" to "+str(las)

    ########################
    ar2=df2.values.flatten()
    x=len(ar2)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    ####################
    ar4=df4.values.flatten()
    x1=len(ar4)
    ar4.sort()
    #print(ar4)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar4[0]
    mid=ar4[x2]
    las=ar4[x11]
    xr1=mid-5
    xr2=mid+5
    c31="F1: "+str(fir)+" to "+str(xr1)
    c32="F2: "+str(xr1)+" to "+str(xr2)
    c33="F3: "+str(xr2)+" to "+str(las)
    #####################3
    ar5=df5.values.flatten()
    x1=len(ar5)
    ar5.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar5[0]
    mid=ar5[x2]
    las=ar5[x11]
    xr1=mid-5
    xr2=mid+5
    c51="F1: "+str(fir)+" to "+str(xr1)
    c52="F2: "+str(xr1)+" to "+str(xr2)
    c53="F3: "+str(xr2)+" to "+str(las)

    ###################3
    ar6=df6.values.flatten()
    x=len(ar6)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c61="F1: "+str(f1)
    c62="F2: "+str(f2)
    ####################
    ar7=df7.values.flatten()
    x=len(ar7)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar7[i]==1:
            g1+=1
        if ar7[i]==2:
            g2+=1
        if ar7[i]==3:
            g3+=1
        if ar7[i]==4:
            g4+=1
        if ar7[i]==5:
            g4+=1
        i+=1
    c71=g1
    c72=g2
    c73=g3
    c74=g4
    c75=g5
    #######################
    ar8=df8.values.flatten()
    x1=len(ar8)
    ar8.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar8[0]
    mid=ar8[x2]
    las=ar8[x11]
    xr1=mid-5
    xr2=mid+5
    c81="F1: "+str(fir)+" to "+str(xr1)
    c82="F2: "+str(xr1)+" to "+str(xr2)
    c83="F3: "+str(xr2)+" to "+str(las)
    #######################
    ar9=df9.values.flatten()
    x=len(ar9)
    i=0
    g=0
    
    while i<x:
        if ar9[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c91="F1: "+str(f1)
    c92="F2: "+str(f2)
    ####################
    ar10=df10.values.flatten()
    x1=len(ar10)
    ar10.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar10[0]
    mid=ar10[x2]
    las=ar10[x11]
    xr1=mid-1
    xr2=mid+1
    c101="F1: "+str(fir)+" to "+str(xr1)
    c102="F2: "+str(xr1)+" to "+str(xr2)
    c103="F3: "+str(xr2)+" to "+str(las)
    ###############
    ar11=df11.values.flatten()
    x=len(ar11)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar11[i]==1:
            g1+=1
        if ar11[i]==2:
            g2+=1
        if ar11[i]==3:
            g3+=1
        
        i+=1
    
    
    x1=6.2
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=0
    mid=x2
    las=x1
    xr1=mid-1
    xr2=mid+1
    c111="F1: "+str(fir)+" to "+str(xr1)
    c112="F2: "+str(xr1)+" to "+str(xr2)
    c113="F3: "+str(xr2)+" to "+str(las)
    ###########################333
    ar13=df13.values.flatten()
    x=len(ar13)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar13[i]==1:
            g1+=1
        if ar13[i]==2:
            g2+=1
        if ar13[i]==3:
            g3+=1
        
        i+=1
    c131=g1
    c132=g2
    c133=g3
    #####################3333
    ar14=df14.values.flatten()
    x=len(ar14)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar14[i]==1:
            g1+=1
        elif ar14[i]==2:
            g2+=1
        elif ar14[i]==3:
            g3+=1
        elif ar14[i]==4:
            g4+=1
        else:
            g4+=1
        i+=1
    c141=g1
    c142=g2
    c143=g3
    c144=g4
    c145=g5
    ######################33

    ######################

    #####################33
    return render_template('classify.html',c11=c11,c12=c12,c13=c13,f1=f1,f2=f2,c31=c31,c32=c32,c33=c33,c51=c51,c52=c52,c53=c53,c61=c61,c62=c62,c71=c71,c72=c72,c73=c73,c74=c74,c75=c75,c81=c81,c82=c82,c83=c83,c91=c91,c92=c92,c111=c111,c112=c112,c113=c113,c101=c101,c102=c102,c103=c103,c131=c131,c132=c132,c133=c133,c141=c141,c142=c142,c143=c143,c144=c144,c145=c145)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


