from flask import render_template ,make_response, request, redirect, url_for,session, flash
import os, xmltodict, json
from flask import jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash

from birthdayapp import app,db, mail, Message
from birthdayapp.forms import Signup, Login, ProfileForm,DonationForm, PhotoForm,ContactForm
from birthdayapp.models import Guest, State, Gift,StateTable,Lga,Transaction

import requests,random

@app.route('/hostels')
def hostel_function():
    rsp = requests.get("http://127.0.0.1:5000/api/v1.0/list")
    #connect to a webservice endpoint via curl
    #retrieve data  and send to my template
    return render_template('hostels.html',data=rsp.json())

@app.route('/tolu/<pid>')
def tolu(pid):
    if session.get('carts') != None:
        session['carts'].append([pid])
        return 'camehere'
    else:       
        session['carts'].append(['9'])
        return 'got here'
    return "saved" 

@app.route('/kill')
def destroysession():
    session.pop('carts',[])
    return 'session destroyed!'

@app.route('/showcart')
def showcart():

    return render_template('tolu.html')

@app.route('/donatecash', methods=['GET','POST'])
def donate_cash_function():
    if session.get('username') != None:
        #query the db using this username
        result =db.session.query(Guest).filter(Guest.id==session['username']).first()
        if request.method =='GET':            
            return render_template('cashdonation.html', data=result)
        else:            
            #retrieve amount from the form, populate trnasction table
            amount = request.form['amt']
            ref = random.randrange(10000,99999) #save it in session
            session['refno'] = ref
            guestid = result.id
            trxstatus = 'Pending'
            trans = Transaction(trxamt=amount,trxref=ref,trxstatus=trxstatus,guest_id=guestid)
            db.session.add(trans)
            db.session.commit()
            return redirect('/confirmation')
    else:
        return redirect(url_for('home'))

@app.route('/confirmation', methods=['GET','POST'])
def confirmation():
    #session['refno], session['username]
    if request.method =='GET':
        data = db.session.query(Transaction,Guest).join(Guest).filter(Transaction.trxref==session['refno']).first()
        return render_template('confirmpay.html',data=data)
    else:
        headers = {
            'Authorization': 'Bearer sk_test_3c5244cfb8965dd000f07a4cfa97185aab2e88d5',
            'Content-Type': 'application/json',
        }

        #paydata
        paydata = '{ "email": "customer@email.com", "amount": "20000" }'
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=paydata)
        jsonresponse = response.json() 
        
        authurl = jsonresponse['data']['authorization_url']
        
        return redirect(authurl)

@app.route('/pastack_update')
def paystack_update():
    #connect to paystack verify 
    ref=session['refno']#request.args.get('reference')
    #pick reference from session

    headers = {'Authorization': 'Bearer sk_test_3c5244cfb8965dd000f07a4cfa97185aab2e88d5',}
    url = "https://api.paystack.co/transaction/verify/"+ str(ref)

    response = requests.get("{}".format(url), headers=headers)
    rsp =response.json() #"Data from Paystack will land here"

    return rsp
    if rsp['data']['status'] =='success':
        return 'update database and redirect them to the feedback page'
    else:
        return 'Try again'


@app.route('/ajaxupload', methods=['GET','POST'])
def ajaxupload():
    if request.method =='GET':
        return render_template('ajaxupload.html')
    else:
        file = request.files['photo']
        username = request.form['username']
        if file:
            #do the upload
            
            name, ext = os.path.splitext(file.filename)
            rename = secure_filename(name) + ext
            file.save(app.config['FILE_UPLOAD_PATH']+rename)
            return rename + username
        else:
            return "File Not Found"


@app.route('/check')
def check():
    obj = make_response(json.dumps({"username":'admin', "email":'a@b.com',"id":1}))
    obj.headers['content-type'] ='application/json'
    return obj

    #return json.dumps({"username":'admin', "email":'a@b.com',"id":1})
    #return jsonify (username='admin', email='a@b.com',id=1)

@app.route('/fetchlga')
def fetchlga():
    stateid = request.args.get('userstate')
    lgas = db.session.query(Lga.lga_name,Lga.lga_id).filter(Lga.state_id == stateid).all()

    display = ""
    for i in lgas:
        display = display + "<option>" + i.lga_name + "</option>"
    return display
    # lgasret = json.dumps(lgas)
    # return lgasret



@app.route('/day2ajax',methods=['POST','GET'])
def day2ajax():
    if request.method =='GET':
        states=db.session.query(StateTable).all()
        return render_template('form.html',states=states,form=ProfileForm())
    else:
        #retrieve the data and insert into db
        email = request.form['email']
        fullname = request.form['guest_fullname']
        userstate= request.form['userstate']
        
        guest = Guest(username='random',pwd='1234',email=email,guest_fullname=fullname,guest_state=userstate)
        db.session.add(guest)
        db.session.commit()
        return 'Thank you, your details have been recorded'




@app.route('/myajax',methods=['POST','GET'])
def myajax():
    if request.method =='GET':
        form = ContactForm()
        return render_template('contactme.html', form=form)
    else:
        demail = request.form['email']
        dfullname = request.form['fullname']

        return "Thank you for contacting us " + dfullname + ' Your email is ' + demail

@app.route('/testjson')
def testjson():
    myjson = '{"name":"Alex Tolulope", "favorite":["session","function","modelling"]}'
    obj =json.loads(myjson)
     
    return "Test" + obj['name']

@app.route('/testxml')
def testxml():
    with open('details.txt') as f:
        doc = xmltodict.parse(f.read())
        return doc['person']['name']['firstname']

@app.route('/',methods=['GET','POST'])
def home():
    if request.method =='GET':
        return render_template('index.html', loginform=Login())
    else:
        user = request.form['username']
        pwd = request.form['pwd']

        res = db.session.query(Guest).filter(Guest.username ==user).first()
        if res:
            encrypted_pwd = res.pwd
            check = check_password_hash(encrypted_pwd,pwd)
            if check:
                session['username']=res.id
                return redirect(url_for('userdashboard'))
            else:
                return redirect('home')
        else:
            return redirect(url_for('home'))

@app.route('/signup', methods=['POST','GET'])
def usersignup():
    if request.method =='GET':
        return render_template('signup.html', signform=Signup())
    else:
        #submits a form here by post, #retrieve the form valiables
        obj = Signup()
        if obj.validate_on_submit():
            #validation passed, process the form
            user=request.form['username']
            pwd=request.values.get('pwd')
            encrypted_pwd = generate_password_hash(pwd)
            dguest = Guest(username=user,pwd=encrypted_pwd)


            db.session.add(dguest)
            db.session.commit()
            if dguest.id:
                session['username'] = dguest.id
                return redirect(url_for('userdashboard'))
            else:
                return redirect(url_for('usersignup'))
        else:
            return render_template("signup.html",signform=obj)
        
@app.route('/dashboard')
def userdashboard():
    if session.get('username') != None:
        #query the db using this username
        result =db.session.query(Guest).filter(Guest.id==session['username']).first()
        return render_template('dashboard.html', data=result)
    else:
        return redirect(url_for('home'))

@app.route('/editprofile', methods=['POST','GET'])
def editprofile():
    if session.get('username') !=None:
        if request.method =='GET':
            userdeets=db.session.query(Guest).get(session['username'])
            allstates = db.session.query(State).all()
            return render_template('editprofile.html',userdeets=userdeets, data=ProfileForm(),allstates=allstates)
        else:
            fullname = request.form['guest_fullname']
            email = request.form['email']
            userstate = request.form['userstate']
            id = request.form['id']
            g = db.session.query(Guest).get(id)
            g.email = email
            g.guest_fullname= fullname
            g.guest_state = userstate
            db.session.commit()
            flash('Profile successfully updated!')
            return redirect(url_for('userdashboard'))
            
    else:
        return redirect(url_for('home'))
@app.route('/donate')
def donate():
    if session.get('username') !=None:
        result =db.session.query(Guest).filter(Guest.id==session['username']).first()
        return render_template('donate.html',data=result, form=DonationForm())
    else:
        return redirect(url_for('home'))

@app.route('/submitdonate',methods=['POST'])
def submitdonate():
    if session['username'] !=None:
        gift=request.form.getlist('gift')
    
        if gift:
            for x in gift:
                gift = Gift(gift_name=x, gift_guestid=session['username'])
                db.session.add(gift)

        return render_template('blank.html', data=gift)
    else:
        return redirect(url_for('home'))

@app.route('/contactme', methods=['POST','GET'])
def contactme():
    if request.method =='GET':
        form = ContactForm()
        return render_template('contact.html', form=form)
    else:
        email=request.form['email']
        fullname= request.form['fullname']
        msg = request.form['msg'] 
        #insert teh above into database
        dmessage='You are most Welcome ' + fullname + 'We will get in touch within 24 hours'
        m = Message(subject='Thanks for Contacting Us',recipients=[email],sender='abiolailupeju@gmail.com')
        
        m.html = "<b>"+dmessage+"Signed<br>Management</b>"
        with app.open_resource("invitation.jpg") as fp:
            m.attach("invitation.jpg", "image/jpg", fp.read())
        
        mail.send(m)
        return "Thanks for contacting"


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    data = db.session.query(Guest,State).join(State).all()
    return render_template('admin_dashboard.html',data=data)

@app.route('/deleterecord/<userid>')
def deleterecord(userid):
    #session
    user = db.session.query(Guest).get(userid)
    db.session.delete(user)
    db.session.commit()
    flash("Record Successfully Deleted!")
    return redirect(url_for('admin'))

@app.route('/updateuser/<userid>')
def updateuser(userid):
    #get the record for user userid
    user = db.session.query(Guest).get(userid)
    return render_template('userupdate.html',data=ProfileForm(),userdeets=user)

@app.route('/resize',methods=['POST','GET'])
def resize():
    if session.get('username') !=None:
        if request.method=='GET':
            return render_template('upload_flaskform.html',data=PhotoForm())
        else:
            pix = request.files['photo']            
            image = Image.open('birthdayapp/static/profile/WIN_20201102_16_13_33_Pro.jpg') 
            image.thumbnail((100,100))
            image.save('ytftdg.jpg')
            return 'Done'
            #return 'post and resize'
    else:
        return redirect(url_for('home'))

@app.route('/sendpix', methods=['POST','GET'])
def sendpix():
    if session.get('username') !=None:
        if request.method=='GET':
            return render_template('upload_flaskform.html',data=PhotoForm())
        else:
            form = PhotoForm()
            if form.validate_on_submit():
                #retriev the form data
                userid = session['username']
                user = db.session.query(Guest).get(userid)
                former_image = user.guest_pix
                os.remove(app.config['FILE_UPLOAD_PATH'] + former_image)
                pix = request.files['photo']
                name, ext = os.path.splitext(pix.filename)
                rename = secure_filename(name) + ext
                pix.save(app.config['FILE_UPLOAD_PATH']+rename)
                
                
                user.guest_pix=rename
                db.session.add(user)
                db.session.commit()
                flash('Image successfully uploaded')
                return redirect(url_for('userdashboard'))
            else:
                return render_template('upload_flaskform.html', data=form)
    else:
        return redirect(url_for('home'))

#The following route is for manually created form
@app.route('/uploadpix', methods=['POST','GET'])
def uploadpix():
    if request.method =='GET':
        return render_template('upload_form.html')
    else:
        #form will be submitted to this point,
        #retrieve form data and process it
        allowed =['.jpg','.png']
        pix = request.files['picture']
        name, ext = os.path.splitext(pix.filename)
        if ext in allowed:
            rename= secure_filename(name) + ext
            uploaded_file = pix.save(app.config['FILE_UPLOAD_PATH']+rename)
            return "Success message and action will be here" 
        else:
            return 'Not Allowed!'
        

    
