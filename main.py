import streamlit as st
import requests



SUBSCRIBE_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/Subscribe/"

LOGIN_ENDPOINT = "http://your-backend-endpoint.com/login"

def subscribe(email):
    api = SUBSCRIBE_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    
    mail = {
      "Name": None,
      "emailid": email,
      "comments": None,
      "Agree_to_Receive_notification": None,
      "subscribe_for": None,
      "Double_opt_in": None
    }
    r = requests.post(api, json=mail, headers=headers)
    print(r)
    data = r.json()
    if data["Status"]==200:
        st.success("You have subscribed successfully!")
    else:
        st.error("Failed to subscribe. Please try again.")


def login(email, username, password1, password2):
    
    payload = {
        "email": email,
        "username": username,
        "password1": password1,
        "password2": password2
    }
    response = requests.post(LOGIN_ENDPOINT, json=payload)
    if response.status_code == 200:  
        return True
    else:
        return False

def main():
    st.title("Unlock Free Access to IntelliMatch-AI-ATS!")

    
    email_subscribe = st.text_input('Email ', placeholder='Enter Your Email', key='subscribe_email')
    if st.button('Subscribe', key='subscribe_button'):
        if email_subscribe:
            subscribe(email_subscribe)
        else:
            st.error("Please enter a valid email address.")

    
    is_login = st.checkbox("Already have an account?")

    if is_login: 
        st.title("Login")
        email_login = st.text_input('Email (Login)', placeholder='Enter Your Email', key='login_email')
        username = st.text_input('Username', placeholder='Enter Your Username', key='login_username')
        password1 = st.text_input('Password', placeholder='Enter Your Password', type='password', key='login_password1')
        password2 = st.text_input('Confirm Password', placeholder='Confirm Your Password', type='password', key='login_password2')
        if st.button('Login', key='login_button'):
            if login(email_login, username, password1, password2):
                st.success("Logged in successfully!")
                # Redirect to another page or perform further actions
            else:
                st.error("Invalid credentials. Please try again.")

if __name__ == "__main__":
    main()
