import streamlit as st
import base64

# --- Function to Convert Image to Base64 ---
def convert_to_base64_from_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Load Images from Local Paths ---
banner_base64 = convert_to_base64_from_file("assets/banner.jpg")
profile_base64 = convert_to_base64_from_file("assets/developer.png")

# --- Custom CSS for Layout & Styling ---
st.markdown("""
    <style>
    .main { padding-top: 0rem; }
    
    .banner-container {
        position: relative;
        width: 100%;
        margin-top: -3rem;
        margin-bottom: 2rem;
    }

    .banner-img {
        width: 100%;
        max-height: 250px;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }

    .profile-pic {
        position: absolute;
        bottom: -50px;
        left: 40px;
        width: 110px;
        height: 110px;
        border-radius: 50%;
        border: 5px solid white;
        object-fit: cover;
        box-shadow: 0 0 12px rgba(0,0,0,0.3);
    }

    .info-block {
        margin-top:  15px;
        padding-left:20px;
    }

    h2 {
        font-size: 26px;
        margin-bottom: 0rem;
    }

    p {
        font-size: 16px;
        margin: 0.1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Display Banner + Profile Picture ---
if banner_base64 and profile_base64:
    st.markdown(f"""
        <div class="banner-container">
            <img class="banner-img" src="data:image/png;base64,{banner_base64}" />
            <img class="profile-pic" src="data:image/png;base64,{profile_base64}" />
        </div>
    """, unsafe_allow_html=True)

    # --- Personal Info Section ---
    st.markdown("""
        <div class='info-block'>
            <h2>Rutton Chandra Sarker</h2>
            <p>🚀<strong> AI/ML Enthusiast | Aspiring LLM Expert</p>
            <p> <strong>💻 Coding | ☕ Coffee | 🌎 Travel</p>
            <p>📧 Email: <a href='mailto:sarker.rutton@gmail.com'>sarker.rutton@gmail.com</a></p>
            <p>🌐 <a href='https://github.com/RuttonSarker' target='_blank'>GitHub</a> |
               💻 <a href='https://www.hackerrank.com/profile/RuttonSarker' target='_blank'>HackerRank</a></p>
        </div>
    """, unsafe_allow_html=True)

# --- Spacer Before Education Section ---
st.markdown("<br>", unsafe_allow_html=True)

# --- Education Section ---
st.subheader("👨‍🏫 Education")
st.markdown("""
- 🎓 M.Sc. in Computational Science *(In Progress)* — Laurentian University, Canada 🇨🇦  
- 🎓 B.Sc. in Computer Science & Engineering — North South University, Bangladesh 🇧🇩
""")

# --- Interests Section ---
st.subheader("📌 Area of Interest")
st.markdown("""
- Artificial Intelligence (AI)  
- Machine Learning / Deep Learning (ML/DL)  
- Natural Language Processing (NLP)  
- Large Language Models (LLMs)
""")

# --- Skills Section ---
st.subheader("🎯 Technical Skills")
st.markdown("""
- **Programming Languages**: Python, C++, Java, R  
- **Database**: MySQL, MongoDB  
- **ML/DL**: Scikit-learn, TensorFlow, Keras, PyTorch
- **LLM**: Langchain, Hugging Face Transformers
- **Visualization**: Pandas, NumPy, Matplotlib, Seaborn  
- **Big Data**: Apache Spark, Hadoop, Hive  
- **Scraping**: BeautifulSoup, Selenium  
- **Cloud**: AWS (S3, EC2, SageMaker), Google Cloud Platform  
- **Tools**: Docker, Git, Tableau, Power BI
""")

# --- Footer ---
st.markdown("---")
st.caption("Built with ☕︎ using Streamlit")

# --- upload section ---
# st.sidebar.header("📤 Upload Your Images")
# banner_file = st.sidebar.file_uploader("Upload Banner Image", type=["png", "jpg", "jpeg"])
# profile_file = st.sidebar.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

# def convert_to_base64(uploaded_file):
 #   return base64.b64encode(uploaded_file.read()).decode()

# Convert uploaded files to base64 strings
# banner_base64 = convert_to_base64(banner_file) if banner_file else None
# profile_base64 = convert_to_base64(profile_file) if profile_file else None


