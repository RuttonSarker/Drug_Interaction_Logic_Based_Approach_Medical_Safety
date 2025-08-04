import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page layout
about_dev = st.Page(
    page = "views/developer.py",
    title = "About Developer",
    icon = ":material/account_circle:",
    default = True,
)

about_project = st.Page(
    page = "views/project.py",
    title = "About Project",
    icon = ":material/info:",
    default = False,
)

drug_interaction = st.Page(
    page = "views/drug_interact.py",
    title = "Drug Interaction",
    icon = ":material/chat_bubble:",
    default = False,
)

pg = st.navigation(
    {
        "Info": [about_dev, about_project],
        "Drug Search": [drug_interaction],
        
    }
)

# Add logo
st.logo("assets/drug.png") 

# Display text in bold and color in the sidebar
st.sidebar.markdown("<h4 style='color: #00A2E8; font-weight: bold;'>֎ Drug-Interation 2.0</h4>", unsafe_allow_html=True)

# Run Navigation
pg.run()