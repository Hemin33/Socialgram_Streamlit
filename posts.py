import streamlit as st
from firebase_admin import firestore

def app():
    # Initialize Firestore client and get it from session state if not already initialized
    if 'db' not in st.session_state:
        st.session_state.db = firestore.client()
    
    db = st.session_state.db

    # Check if the user is logged in
    if not st.session_state.get('logged_in', False):
        st.error('Please login first.')
        return
    
    # Get the logged-in user's username
    username = st.session_state.get('email', '')
    
    # Title showing the current user
    st.title(f'Posted by: {username}')
    
    # Retrieve the user's posts from Firestore
    result = db.collection('Posts').document(username).get()
    
    # Check if the user document exists
    if result.exists:
        user_data = result.to_dict()
        content = user_data.get('Content', [])
        
        def delete_post(index):
            # Delete a post by its index
            post_to_delete = content[index]
            try:
                db.collection('Posts').document(username).update({
                    'Content': firestore.ArrayRemove([post_to_delete])
                })
                # Show a warning that the post was deleted
                st.warning('Post deleted.')
                # Refresh the page to update content after deletion
                st.experimental_rerun()
            except Exception as e:
                # Handle errors during deletion
                st.error(f'Something went wrong: {e}')
        
        # Display the user's posts
        for i in range(len(content) - 1, -1, -1):
            post_content = content[i]
            st.text_area(label='', value=post_content, disabled=True)
            st.button('Delete Post', on_click=delete_post, args=(i,), key=f'delete_post_{i}')
    
    else:
        st.warning('No posts found for this user.')
