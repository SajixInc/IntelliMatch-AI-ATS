import streamlit as st
import requests
import time

# Define the endpoints
SUBSCRIBE_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/Otpgenerate/"
OTP_VERIFICATION_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/OtpVerfication/"
EMAIL_VERIFICATION_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/EmailVerification/"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'already_have_account' not in st.session_state:
    st.session_state.already_have_account = False
if 'otp_message' not in st.session_state:
    st.session_state.otp_message = False
if 'email_exists' not in st.session_state:
    st.session_state.email_exists = None

# Function to subscribe and generate OTP
def subscribe(email):
    api = SUBSCRIBE_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    mail = {"emailid": email}
    r = requests.post(api, json=mail, headers=headers)
    data = r.json()
    
    if data.get("Status") == 200:
        st.session_state.otp_sent = True
        st.session_state.otp_message = True
        st.success(f"OTP sent successfully to {email}")
        time.sleep(1)
        st.session_state.otp_message = False
        st.experimental_rerun()
    else:
        st.error("Failed to subscribe. Please try again.")

# Function to verify OTP
def verify_otp(email, otp):
    api = OTP_VERIFICATION_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    data = {"emailid": email, "otp": otp}
    r = requests.post(api, json=data, headers=headers)
    response = r.json()
    
    return response.get("Status") == 200

# Function to verify if email exists
def check_email_exists(email):
    api = EMAIL_VERIFICATION_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    data = {"emailid": email}
    r = requests.post(api, json=data, headers=headers)
    response = r.json()
    
    return response.get("Status") == 200

# Streamlit UI
st.title("Unlock Free Access to IntelliMatch-AI-ATS!")

if not st.session_state.logged_in:
    if not st.session_state.already_have_account:
        email = st.text_input("Enter your email:", value=st.session_state.email)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Subscribe"):
                if email:
                    st.session_state.email = email
                    subscribe(email)
                else:
                    st.warning("Please enter a valid email address.")
        
        with col2:
            if st.button("Already have an account"):
                st.session_state.already_have_account = True
                st.experimental_rerun()
    
    if st.session_state.already_have_account:
        email = st.text_input("Enter your email for login:", value=st.session_state.email)
        if st.button("Send OTP"):
            if email:
                st.session_state.email = email
                if check_email_exists(email):
                    subscribe(email)
                else:
                    st.session_state.email_exists = False
                    st.warning("You don't have an account! Please subscribe.")
            else:
                st.warning("Please enter a valid email address.")
    
    if st.session_state.otp_sent:
        otp_input = st.text_input('Enter OTP:', key='otp_input')
        if st.button('Resend OTP'):
            subscribe(st.session_state.email)
        if st.button('Login'):
            if otp_input:
                if verify_otp(st.session_state.email, otp_input):
                    st.success("Successfully logged in!")
                    st.session_state.logged_in = True
                else:
                    st.error("Invalid OTP. Please try again.")
            else:
                st.error("Please enter OTP.")
else:
    st.success("You are already logged in.")
