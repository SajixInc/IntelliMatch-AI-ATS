import streamlit as st
import requests

# Define the endpoints
SUBSCRIBE_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/Otpgenerate/"
OTP_VERIFICATION_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/OtpVerfication/"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False

# Function to subscribe and generate OTP
def subscribe(email):
    api = SUBSCRIBE_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    mail = {"emailid": email}
    r = requests.post(api, json=mail, headers=headers)
    data = r.json()
    
    if data.get("Status") == 200:
        st.session_state.otp_sent = True
        st.success(f"OTP sent successfully to {email}")
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

# Streamlit UI
st.title("Unlock Free Access to IntelliMatch-AI-ATS!")

if not st.session_state.logged_in:
    email = st.text_input("Enter your email:", value=st.session_state.email)
    if st.button("Subscribe"):
        if email:
            st.session_state.email = email
            subscribe(email)
        else:
            st.warning("Please enter a valid email address.")

    if st.session_state.otp_sent:
        otp_input = st.text_input('Enter OTP:', key='otp_input')
        if st.button('Resend OTP'):
            subscribe(st.session_state.email)
        if st.button('Login'):
            if otp_input:
                
                api = OTP_VERIFICATION_ENDPOINT
                headers = {'Content-Type': 'application/json'}
                data = {"emailid": email, "otp": otp_input}
                r = requests.post(api, json=data, headers=headers)
                response = r.json()
                if response.get("Status") == 200:
                    st.success("Successfully logged in!")
                    st.session_state.logged_in = True
                else:
                    st.error("Invalid OTP. Please try again.")
            else:
                st.error("Please enter OTP.")
else:
    st.success("You are already logged in.")
