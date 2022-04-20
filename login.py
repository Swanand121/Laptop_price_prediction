import streamlit as st
import pandas as pd
import pickle 
import numpy as np


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<style>
.navbar{
	background-color:#064663
}
.navbar a {
	color:#fff;
}
</style>
<nav class="navbar fixed-top navbar-expand-lg" >
  <a  href="#" class="navbar-brand mb-0 h1">Laptop Price Prediction</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" style="font-size:30px">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link mb-0 h1" href="https://www.flipkart.com/search?q=macbook&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_3_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_2_3_na_na_ps&as-pos=2&as-type=RECENT&suggestionId=macbook%7CLaptops&requestId=5be9ff4c-b5f9-4b5d-8cf7-2ee60177b883&as-backfill=on" >Ultrabook laptop<span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">
        <a class="nav-link mb-0 h1" href="https://www.flipkart.com/search?q=gaming+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=gaming+laptop%7CLaptops&requestId=aec3757a-574b-4e69-81b9-f08563b12c57&as-searchtext=ga" >Gaming laptop<span class="sr-only">(current)</span></a>
      </li>
	   <li class="nav-item active">
        <a class="nav-link mb-0 h1" href="https://www.flipkart.com/search?q=notebooks+in+laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=notebooks+in+laptops%7CLaptops&requestId=3872556d-09b0-4bb2-9a99-bce58087d0e6&as-backfill=on" >Notebook laptop <span class="sr-only">(current)</span></a>
      </li>
	  <li class="nav-item active">
        <a class="nav-link mb-0 h1" href="https://www.flipkart.com/search?q=notebooks+in+laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=notebooks+in+laptops%7CLaptops&requestId=3872556d-09b0-4bb2-9a99-bce58087d0e6&as-backfill=on&p%5B%5D=facets.type%255B%255D%3D2%2Bin%2B1%2BLaptop" >2 in 1 laptop <span class="sr-only">(current)</span></a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT primary key ,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data 

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def app():
    pipe = pickle.load(open('pipe.pkl','rb'))
    df = pickle.load(open('df.pkl','rb'))
    st.title("Laptop Predction")
    company = st.selectbox('Brand',df['Company'].unique())
    type = st.selectbox('Type',df['TypeName'].unique())
    ram=st.selectbox('RAM',[2,4,6,8,12,16,24,32,64])
    weight=st.number_input('weight of the Laptop')
    touchscreen=st.selectbox('Touchscreen',['No','Yes'])
    ips=st.selectbox('Ips',['Yes','NO'])
    Screen_size=st.number_input('Screen Size')
    resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
    cpu=st.selectbox('CPU',df['Cpu brand'].unique())
    hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])
    ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])
    gpu = st.selectbox('GPU',df['Gpu brand'].unique())
    Os = st.selectbox('OS',df['os'].unique())
    if st.button('Click to Predict'):
        ppi=None
        if touchscreen== 'Yes':
            touchscreen=1
        else:
            touchscreen=0

        if ips == 'Yes':
            ips = 1
        else:
            ips = 0    
        X_res = int(resolution.split('x')[0])
        Y_res = int(resolution.split('x')[1])
        ppi = ((X_res**2) + (Y_res**2))**0.5/Screen_size
        query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,Os])

        query = query.reshape(1,12)
        st.title("The predicted price of this configuration is " + str(int(np.exp(pipe.predict(query)[0]))))


def main():
	"""Welcome to Laptop Price Prediction App"""

	

	menu = ["Login","Admin","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)
	
	if choice == "Admin":
		
		st.title("Admin Login")
		username = st.sidebar.text_input("Username")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Profiles"])
				
				if task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	elif choice == "Login":
		st.subheader("Login Section")
		st.title("User Login")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
		
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				app()
                    
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.title("Signup page")
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
   
