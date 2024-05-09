import streamlit as st
from firebase_admin import firestore

def app():
    # Ensure Firestore client is stored in session state
    if 'db' not in st.session_state:
        st.session_state.db = firestore.client()

    db = st.session_state.db
    custom_css = """
        <style>
            /* Change the font color of the text area and latest posts to black */
            .stTextArea textarea, .stTextArea div {
                color: black !important;
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    # Check if the user is logged in and get their username from session state
    if st.session_state.logged_in:
        username = st.session_state.email
        placeholder_text = 'Post your thought'
    else:
        username = None
        placeholder_text = 'Login to be able to post!!'

    # Allow users to post if they are logged in
    post = st.text_area(label=':orange[+ New Post]', placeholder=placeholder_text, height=None, max_chars=500)

    if st.button('Post', use_container_width=True):
        if username:
            if post:  # Check if post is not empty
                user_document = db.collection('Posts').document(username)
                user_data = user_document.get()

                if user_data.exists:
                    user_data = user_data.to_dict()
                    # Add post to existing user's content list
                    user_document.update({u'Content': firestore.ArrayUnion([u'{}'.format(post)])})
                else:
                    # Create a new document for the user if it does not exist
                    data = {"Content": [post], 'Username': username}
                    db.collection('Posts').document(username).set(data)
                
                st.success('Post uploaded!!')
        else:
            st.error('You must be logged in to post!')

    # Display latest posts
    st.header(':violet[Latest Posts]')
    docs = db.collection('Posts').get()

    for doc in docs:
        d = doc.to_dict()
        try:
            # Display the latest post from each user
            st.text_area(label=':green[Posted by:] :orange[{}]'.format(d['Username']), value=d['Content'][-1], height=20, disabled=True)
        except Exception as e:
            st.error(f'Error displaying posts: {e}')
