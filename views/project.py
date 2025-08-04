import streamlit as st

def about_project():
    st.title("💊 Drug Interaction Checker")

    st.header("🔍 Project Overview")

    st.markdown("""
Drug safety is a growing concern in modern healthcare, particularly for patients on **polypharmacy** (multiple medications). This project introduces a logic-based **Drug Interaction Knowledge Base** that 
uses formal logic and inference rules to:
- Detect potential harmful drug interactions
- Explain the rationale behind each conflict
- Improve medical safety through intelligent reasoning

The goal is to provide a **provable, explainable, and research-friendly** alternative to existing static, commercial drug checkers.
""")
    
    st.header("🧰 Tools & Technologies")
    st.markdown("""
- **Language**: Prolog (for logic rules), Python (for integration and UI)  
- **Logic Programming**: PyDatalog  
- **Interface**: Streamlit  
- **Libraries**: streamlit, PyDatalog, pandas, pyvis, plotly, pyttsx3  
- **Future Integration**: Potential OWL ontologies or RDF for structured knowledge  

🛠 This tool is designed for extensibility and could support EHR integration or cloud scaling in future versions.
    """)

    st.header("⚙️ How It Works")
    with st.expander("🔗 Step 1: Knowledge Base Construction"):
        st.markdown("""
- Drug data such as **active ingredients, classes, mechanisms** are stored in a Prolog-style rule base
- Drug interactions are modeled using **logical rules**
- Sample rule: `interaction(drugA, drugB) :- condition, evidence`
        """)
    
    with st.expander("💡 Step 2: Query & Inference"):
        st.markdown("""
- Users input a list of drugs
- The system uses **inference rules** to detect any unsafe combinations
- If an interaction is found, the **rationale** behind it is provided (not just a warning)
        """)

    with st.expander("🧑‍⚕️ Step 3: User Interaction"):
        st.markdown("""
- Healthcare professionals or researchers can query drug combinations
- Output is both **decision** and **explanation** (e.g., "Drug A and Drug B increase toxicity via liver metabolism inhibition")
        """)

    st.header("📈 Results & Benefits")
    st.markdown("""
- ✅ Provides explainable decisions using logical rules  
- ✅ Improves understanding and transparency in drug safety checks  
- ✅ Supports research and education — not locked down like many commercial tools  
- ✅ Can grow into a scalable, intelligent decision support system in healthcare  

⚠️ Excludes integration with real-time hospital data due to privacy/regulatory concerns.
    """)

    st.caption("Built by Rutton Chandra Sarker 👩🏻‍💻 using PyDatalog, pyvis, pandas, pyttsx3 and Streamlit")

# 🔥 CALL the function to display content
about_project()