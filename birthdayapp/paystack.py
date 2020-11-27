
@app.route('/confirmation', methods=['GET','POST'])
def confirmation():
    #session['refno], session['username]
    if request.method =='GET':
        data = db.session.query(Transaction,Guest).join(Guest).filter(Transaction.trxref==session['refno']).first()
        return render_template('confirmpay.html',data=data)
    else:
        headers = {
            'Authorization': 'Bearer sk_test_38d5_replace_with_your_sk_key_from_Pastack_Settings',
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
    ref=request.args.get('reference')
    headers = {'Authorization': 'Bearer sk_test_38d5_replace_with_your_sk_key_from_Pastack_Settings',}
    response = requests.get('https://api.paystack.co/transaction/verify/vh8rlngxda', headers=headers)
    rsp =response.json() #"Data from Paystack will land here"
    if rsp['data']['status'] =='success':
        return 'update database and redirect them to the feedback page'
    else:
        return 'Try again'
