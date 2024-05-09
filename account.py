import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests

# Replace with your Firebase service account key file
SERVICE_ACCOUNT_KEY_FILE = 'socialgram-21bd0-baa62400f5b2.json'

# Replace with your Firebase project's API key
FIREBASE_API_KEY = 'AIzaSyB2J5DBhKudMOZdPhykSEnmPVVZB03MJ_s'

# Initialize Firebase with the credentials
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_FILE)
firebase_admin.initialize_app(cred)

# Function to handle login
def handle_login(email, password):
    # Firebase Authentication REST API endpoint for email/password authentication
    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    
    # Data to send in the POST request
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    # Send POST request to the API
    response = requests.post(auth_url, json=data)
    response_data = response.json()
    
    if response.status_code == 200:
        # Successful authentication
        user_id = response_data.get('localId')
        st.session_state.logged_in = True
        st.session_state.email = email
        st.success(f'Login successful! User ID: {user_id}')
    else:
        # Authentication failed
        error_message = response_data.get('error', {}).get('message', 'Unknown error')
        st.error(f'Login failed: {error_message}')

# Function to handle sign-up
def handle_signup(email, password, username):
    try:
        # Create a new user with the provided email, password, and username
        user = auth.create_user(email=email, password=password, uid=username)
        st.success("Account created successfully")
        st.markdown("Please login using your email and password")
        st.balloons()
        
    except Exception as e:
        # Handle exceptions and display an error message
        st.error(f"Sign-up failed: {e}")

# Function to handle logout
def handle_logout():
    # Clear session state to log out the user
    st.session_state.logged_in = False
    st.session_state.email = ''
    st.success('You have been logged out')

# Define the Streamlit app
def app():
    st.title("Welcome to Socialgram")
    
    # Initialize session state variables if they don't already exist
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "email" not in st.session_state:
        st.session_state.email = ''
    if "password" not in st.session_state:
        st.session_state.password = ''

    # If the user is already logged in
    if st.session_state.logged_in:
        # Display a message that the user is logged in
        st.success(f'You are already logged in as {st.session_state.email}')
        # Provide a logout button
        if st.button("Logout"):
            handle_logout()
    else:
        # Display login and sign-up options
        choice = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'])
        
        if choice == 'Login':
            # Retrieve email and password from session state
            st.session_state.email = st.text_input("Email Address", value=st.session_state.email)
            st.session_state.password = st.text_input("Password", type="password", value=st.session_state.password)
            # Handle login button
            if st.button("Login"):
                handle_login(st.session_state.email, st.session_state.password)
        
        else:
            # Retrieve email and password from session state
            st.session_state.email = st.text_input("Email Address", value=st.session_state.email)
            st.session_state.password = st.text_input("Password", type="password", value=st.session_state.password)
            username = st.text_input("Enter your username")
            # Handle sign-up button
            if st.button("Create my account"):
                handle_signup(st.session_state.email, st.session_state.password, username)