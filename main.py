from flask import Flask, request, render_template,redirect,session,url_for
import requests
from pathlib import Path
import json
import os
import pandas as pd
from data import Read_Data


with open("config.json",'r+') as c:
	params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-secret-key'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
	data = None
	d = Read_Data()
	d = d.read()
	if(('user' in session and session['user'] == params['admin_user'])):
		return render_template('dashboard.html',data = d)

	elif('user' in session and session['user'] == params['username']):
		if(request.method == 'POST'):
			name = request.form.get('Name')
			email = request.form.get('Email')
			msg = request.form.get('Msg')

			data = {'Name':name,'Email':email,'Messages':msg}
			check_file = False
			try:
				df = pd.read_csv("Messages.csv",index_col=0)
				check_file = True
			except:
				df = pd.DataFrame(data,index = [0])
				df.to_csv("Messages.csv")

			if(check_file):
				df = df.append(data,ignore_index = True)
				df.to_csv("Messages.csv")
		usr = params['username']
		return render_template('user_dashboard.html',data = d,usr = usr)


	msg = None
	if(request.method == 'POST'):

		usrname = request.form.get('usrname')
		password = request.form.get('pass')

		if(usrname == params['admin_user'] and password == params['admin_pass']):
			session['user'] = usrname
			return render_template('dashboard.html',data = d)
		if(usrname == params['username'] and password == params['password']):
			session['user'] = usrname
			usr = usrname
			return render_template('user_dashboard.html',data = d,usr = usr)

		else:
			msg = 0
			return render_template('Login.html',msg = msg)

	return render_template('Login.html',msg = msg)


@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('dashboard')

@app.route('/change-password',methods=['GET','POST'])
def change_password():
	data = None
	if(('user' in session and session['user'] == params['admin_user'])):

		if(request.method == 'POST'):
			current_pass = request.form.get('curr_pass')
			new_pass = request.form.get('new_pass')

			if(current_pass == params['admin_pass']):
				params['admin_pass'] = new_pass
				with open('config.json','r+') as json_file:
					json_data = json.load(json_file)
					json_data['params']['admin_pass'] = new_pass
					json_file.seek(0)
					json.dump(json_data,json_file)
					json_file.truncate()

				session.pop('user',None)
				return redirect(url_for('dashboard'))
			else:
				msg = 0
				return render_template('update_pass.html',msg = msg)

		return render_template('update_pass.html')

	return render_template('update_pass.html')



@app.route('/user-dashboard')
def user_dashboard():
	return render_template('user_dashboard.html')

if __name__ == '__main__':
     app.run(debug=True)
