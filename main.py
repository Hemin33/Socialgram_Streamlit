import streamlit as st
from streamlit_option_menu import option_menu
import home, account, posts, about

st.set_page_config(
    page_title="Socialgram",
)

# Inject custom CSS to style the background colors
custom_css = """
    <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color:#AEC6CF;
        }
        
        /* Main content background color */
        [data-testid="stAppViewContainer"], [data-testid="stAppContainer"] {
            background-color:lightblue;
        }
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Socialgram',
                options=['Home', 'Account', 'Posts', 'About'],
                icons=['house-fill', 'person-circle', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5px!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "grey"},
                }
            )

        if app == 'Home':
            home.app()
        elif app == 'Account':
            account.app()
        elif app == 'Posts':
            posts.app()
        elif app == 'About':
            about.app()

# Create the multi-app and run it
multi_app = MultiApp()
multi_app.add_app('Home', home.app)
multi_app.add_app('Account', account.app)
multi_app.add_app('Posts', posts.app)
multi_app.add_app('About', about.app)
multi_app.run()
