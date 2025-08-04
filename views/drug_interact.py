import streamlit as st
import pandas as pd
from itertools import combinations
from pyDatalog import pyDatalog
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import plotly.express as px
import pyttsx3
import os
import re
import string
from dotenv import load_dotenv

# --- Load credentials from .env ---
load_dotenv()

# --- Authentication Helpers ---
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email Address", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not email and not password:
            st.error("Both email and password fields must be filled!")
        elif not email:
            st.error("Please enter an email address.")
        elif not password:
            st.error("Please enter a password.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address (e.g., example@gmail.com).")
        else:
            emails = os.getenv("USER_EMAILS", "").split(",")
            passwords = os.getenv("USER_PASSWORDS", "").split(",")

            if email in emails:
                index = emails.index(email)
                if password == passwords[index]:
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Invalid email address")

    st.markdown("ℹ️ Note: Only test users may login. Registration is coming soon.")

def show_login():
    login()

# --- Redirect to login if not authenticated ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    show_login()
    st.stop()

# --- PyDatalog Setup ---
pyDatalog.clear()
pyDatalog.create_terms('interaction, check_interaction, Severity, Risk, Recommendation, D1, D2')

define_datalog_rules = lambda: [
    check_interaction(D1, D2, Severity, Risk, Recommendation) <= interaction(D1, D2, Severity, Risk, Recommendation),
    check_interaction(D1, D2, Severity, Risk, Recommendation) <= interaction(D2, D1, Severity, Risk, Recommendation)
]

define_datalog_rules()

# --- Sample Interactions ---
_ = +interaction('warfarin', 'aspirin', 'high', 'Increased risk of bleeding', 'Monitor INR and avoid concurrent use unless necessary.')
_ = +interaction('warfarin', 'ibuprofen', 'high', 'Gastrointestinal bleeding risk', 'Use acetaminophen instead.')
_ = +interaction('warfarin', 'naproxen', 'high', 'GI bleeding', 'Avoid combination')
_ = +interaction('warfarin', 'clopidogrel', 'high', 'Severe bleeding', 'Use with caution; monitor closely')
_ = +interaction('warfarin', 'amiodarone', 'high', 'Increased INR', 'Reduce warfarin dose and monitor INR')
_ = +interaction('warfarin', 'fluconazole', 'high', 'Increased bleeding due to CYP2C9 inhibition', 'Use alternative antifungal')
_ = +interaction('warfarin', 'metronidazole', 'high', 'Severe increase in INR', 'Avoid or monitor closely')
_ = +interaction('warfarin', 'erythromycin', 'high', 'Increased warfarin effect', 'Monitor INR closely')
_ = +interaction('warfarin', 'cimetidine', 'moderate', 'Increased warfarin plasma levels', 'Consider alternative H2 blocker')
_ = +interaction('warfarin', 'allopurinol', 'moderate', 'Increased anticoagulant effect', 'Monitor INR')
_ = +interaction('aspirin', 'ibuprofen', 'moderate', 'Reduced cardioprotective effect of aspirin', 'Take aspirin 30 minutes before ibuprofen')
_ = +interaction('aspirin', 'clopidogrel', 'high', 'Additive antiplatelet effect', 'Use only with close monitoring')
_ = +interaction('aspirin', 'prednisolone', 'high', 'GI ulcer risk', 'Use PPI as gastroprotection')
_ = +interaction('aspirin', 'heparin', 'high', 'Increased bleeding', 'Avoid unless medically necessary')
_ = +interaction('ibuprofen', 'lithium', 'high', 'Increased lithium levels', 'Monitor lithium serum concentration')
_ = +interaction('ibuprofen', 'methotrexate', 'high', 'Reduced methotrexate clearance', 'Avoid concurrent use')
_ = +interaction('ibuprofen', 'ramipril', 'moderate', 'Reduced antihypertensive effect', 'Monitor blood pressure and renal function')
_ = +interaction('ibuprofen', 'digoxin', 'moderate', 'Increased digoxin concentration', 'Monitor serum digoxin levels')
_ = +interaction('ibuprofen', 'furosemide', 'moderate', 'Reduced diuretic efficacy', 'Monitor fluid retention')
_ = +interaction('erythromycin', 'theophylline', 'high', 'Increased theophylline levels', 'Monitor for toxicity')
_ = +interaction('erythromycin', 'simvastatin', 'high', 'Rhabdomyolysis risk', 'Avoid combination')
_ = +interaction('clarithromycin', 'warfarin', 'high', 'Increased bleeding risk', 'Monitor INR closely')
_ = +interaction('rifampin', 'oral_contraceptives', 'high', 'Reduced contraceptive effectiveness', 'Use backup method')
_ = +interaction('trimethoprim', 'spironolactone', 'high', 'Hyperkalemia', 'Monitor potassium levels')
_ = +interaction('trimethoprim', 'warfarin', 'high', 'Increased INR', 'Adjust warfarin dose accordingly')
_ = +interaction('amoxicillin', 'allopurinol', 'moderate', 'Rash risk', 'Monitor skin reaction')
_ = +interaction('metronidazole', 'alcohol', 'high', 'Disulfiram-like reaction', 'Avoid alcohol')
_ = +interaction('beta_blockers', 'verapamil', 'high', 'Bradycardia and heart block', 'Avoid combination')
_ = +interaction('beta_blockers', 'insulin', 'moderate', 'Masked hypoglycemia', 'Educate patient on symptoms')
_ = +interaction('amlodipine', 'simvastatin', 'moderate', 'Increased simvastatin levels', 'Limit simvastatin to 20 mg')
_ = +interaction('nitrates', 'sildenafil', 'high', 'Severe hypotension', 'Contraindicated')
_ = +interaction('enalapril', 'potassium_supplements', 'high', 'Hyperkalemia', 'Avoid or monitor potassium')
_ = +interaction('spironolactone', 'lisinopril', 'high', 'Additive potassium retention', 'Monitor serum potassium')
_ = +interaction('furosemide', 'digoxin', 'high', 'Hypokalemia increases digoxin toxicity', 'Monitor K+ and digoxin')
_ = +interaction('clonidine', 'beta_blockers', 'high', 'Rebound hypertension on withdrawal', 'Taper beta-blockers gradually')
_ = +interaction('fluoxetine', 'tramadol', 'high', 'Serotonin syndrome', 'Use with caution')
_ = +interaction('fluoxetine', 'warfarin', 'high', 'Increased bleeding', 'Monitor INR')
_ = +interaction('fluoxetine', 'amitriptyline', 'moderate', 'Increased TCA levels', 'Monitor side effects')
_ = +interaction('sertraline', 'NSAIDs', 'moderate', 'Increased bleeding', 'Monitor for signs of GI bleeding')
_ = +interaction('sertraline', 'linezolid', 'high', 'Serotonin syndrome', 'Contraindicated')
_ = +interaction('haloperidol', 'carbamazepine', 'moderate', 'Reduced haloperidol effect', 'Increase dose if needed')
_ = +interaction('haloperidol', 'lithium', 'high', 'Neurotoxicity risk', 'Monitor neurologic function')
_ = +interaction('metformin', 'contrast_dye', 'high', 'Lactic acidosis risk', 'Hold metformin before contrast')
_ = +interaction('insulin', 'beta_blockers', 'moderate', 'Masking of hypoglycemia', 'Caution in diabetic patients')
_ = +interaction('sitagliptin', 'digoxin', 'moderate', 'Increased digoxin levels', 'Monitor digoxin')
_ = +interaction('fluconazole', 'warfarin', 'high', 'Potentiation of warfarin effect', 'Monitor INR')
_ = +interaction('ketoconazole', 'statins', 'high', 'Rhabdomyolysis risk', 'Avoid concurrent use')
_ = +interaction('itraconazole', 'digoxin', 'moderate', 'Increased digoxin concentration', 'Monitor levels')
_ = +interaction('phenytoin', 'warfarin', 'high', 'Fluctuating INR levels', 'Frequent monitoring')
_ = +interaction('phenytoin', 'doxycycline', 'moderate', 'Reduced doxycycline levels', 'Increase dose')
_ = +interaction('valproate', 'lamotrigine', 'high', 'Severe skin rash', 'Start lamotrigine at lower dose')
_ = +interaction('carbamazepine', 'oral_contraceptives', 'high', 'Reduced contraceptive effect', 'Use backup method')
_ = +interaction('ritonavir', 'simvastatin', 'high', 'Rhabdomyolysis risk', 'Use pravastatin instead')
_ = +interaction('ritonavir', 'omeprazole', 'moderate', 'Reduced ritonavir levels', 'Monitor viral load')
_ = +interaction('efavirenz', 'methadone', 'moderate', 'Withdrawal symptoms', 'Increase methadone dose')
_ = +interaction('theophylline', 'ciprofloxacin', 'high', 'Theophylline toxicity', 'Monitor serum levels')
_ = +interaction('digoxin', 'verapamil', 'high', 'Bradycardia risk', 'Monitor heart rate and ECG')
_ = +interaction('levothyroxine', 'calcium_carbonate', 'moderate', 'Reduced thyroid absorption', 'Separate dosing by 4 hours')
_ = +interaction('levothyroxine', 'iron_supplements', 'moderate', 'Reduced efficacy', 'Separate by several hours')
_ = +interaction('simvastatin', 'grapefruit_juice', 'high', 'Increased statin levels', 'Avoid grapefruit')
_ = +interaction('cyclosporine', 'diltiazem', 'high', 'Increased cyclosporine concentration', 'Monitor levels')
_ = +interaction('cyclosporine', 'potassium_sparing_diuretics', 'high', 'Hyperkalemia', 'Monitor potassium closely')
_ = +interaction('allopurinol', 'azathioprine', 'high', 'Bone marrow suppression', 'Reduce azathioprine dose')
_ = +interaction('chlorpromazine', 'metoclopramide', 'high', 'Extrapyramidal symptoms', 'Avoid concurrent use')
_ = +interaction('clozapine', 'ciprofloxacin', 'high', 'Increased clozapine levels', 'Monitor WBC and clozapine level')
_ = +interaction('clopidogrel', 'omeprazole', 'high', 'Reduced antiplatelet effect', 'Use pantoprazole instead')
_ = +interaction('fexofenadine', 'fruit_juice', 'moderate', 'Reduced absorption', 'Avoid juice 4 hrs before/after')
_ = +interaction('paracetamol', 'warfarin', 'moderate', 'Increased INR with prolonged use', 'Monitor INR')
_ = +interaction('paracetamol', 'alcohol', 'high', 'Liver toxicity', 'Avoid heavy alcohol use')
_ = +interaction('bisoprolol', 'verapamil', 'high', 'Bradycardia', 'Avoid combination')
_ = +interaction('loperamide', 'quinidine', 'high', 'Cardiac arrhythmia', 'Avoid combination')
_ = +interaction('naproxen', 'lithium', 'high', 'Increased lithium levels', 'Monitor lithium level')
_ = +interaction('pantoprazole', 'clopidogrel', 'moderate', 'Possible reduced effect of clopidogrel', 'Monitor if used together')
_ = +interaction('loratadine', 'erythromycin', 'moderate', 'QT prolongation risk', 'Monitor ECG in high doses')
_ = +interaction('duloxetine', 'tramadol', 'high', 'Seizure and serotonin syndrome', 'Avoid combination')
_ = +interaction('bupropion', 'sertraline', 'moderate', 'Lowered seizure threshold', 'Avoid high doses')
_ = +interaction('ketorolac', 'enoxaparin', 'high', 'Major bleeding risk', 'Avoid concurrent use')


# --- Logic to Check Interactions ---
def check_all_interactions(drug_list):
    drug_list = [d.strip().lower() for d in drug_list if d.strip()]
    pairs = combinations(drug_list, 2)
    interactions = []
    for d1, d2 in pairs:
        Severity.clear()
        Risk.clear()
        Recommendation.clear()
        query_result = check_interaction(d1, d2, Severity, Risk, Recommendation)

        # If no interaction was found, skip
        if not Severity.data or not Risk.data or not Recommendation.data:
            continue

        for severity, risk, recommendation in zip(Severity.data, Risk.data, Recommendation.data):
            # Extra guard: skip if any of them is None
            if not all([severity, risk, recommendation]):
                continue
            interactions.append({
                'Drug 1': d1.title(),
                'Drug 2': d2.title(),
                'Severity': severity,
                'Risk': risk,
                'Recommendation': recommendation
            })
    return interactions

# --- Graph Rendering with Pyvis ---
def generate_graph(interactions):
    net = Network(height="550px", width="100%", bgcolor="#ffffff", font_color="black")
    net.toggle_physics(True)
    net.barnes_hut()
    for i in interactions:
        d1, d2, severity = i['Drug 1'], i['Drug 2'], i['Severity']
        label = f"{severity.title()}<br>{i['Risk']}"
        color = {'high': 'red', 'moderate': 'orange', 'low': 'green'}.get(severity.lower(), 'gray')
        net.add_node(d1, label=d1)
        net.add_node(d2, label=d2)
        net.add_edge(d1, d2, color=color, title=label)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp_file.name)
    return tmp_file.name

# --- Session State Defaults ---
if "input_drugs" not in st.session_state:
    st.session_state.input_drugs = []
if "results" not in st.session_state:
    st.session_state.results = None

# --- UI Layout ---
st.title("💊 Drug Interaction Checker")
st.markdown("Select drugs to check for possible **harmful interactions**.")

known_drugs = [
    'allopurinol', 'amiodarone', 'amlodipine', 'amoxicillin', 'aspirin', 'azathioprine',
    'beta_blockers', 'bisoprolol', 'bupropion', 'calcium_carbonate', 'carbamazepine',
    'chlorpromazine', 'ciprofloxacin', 'clarithromycin', 'clonidine', 'clopidogrel',
    'clozapine', 'contrast_dye', 'cyclosporine', 'digoxin', 'diltiazem', 'doxycycline',
    'duloxetine', 'efavirenz', 'enalapril', 'enoxaparin', 'erythromycin', 'fluconazole',
    'fluoxetine', 'fruit_juice', 'furosemide', 'grapefruit_juice', 'haloperidol',
    'heparin', 'ibuprofen', 'insulin', 'iron_supplements', 'itraconazole',
    'ketoconazole', 'ketorolac', 'lamotrigine', 'levothyroxine', 'linezolid',
    'lisinopril', 'lithium', 'loperamide', 'loratadine', 'metformin', 'methadone',
    'metoclopramide', 'metronidazole', 'methotrexate', 'naproxen', 'nitrates',
    'NSAIDs', 'omeprazole', 'oral_contraceptives', 'pantoprazole', 'paracetamol',
    'phenytoin', 'potassium_sparing_diuretics', 'potassium_supplements',
    'prednisolone', 'quinidine', 'ramipril', 'rifampin', 'ritonavir', 'sertraline',
    'simvastatin', 'sitagliptin', 'spironolactone', 'statins', 'sildenafil',
    'theophylline', 'tramadol', 'trimethoprim', 'valproate', 'verapamil', 'warfarin'
]

selected_drugs = st.multiselect("Select Drugs:", options=known_drugs, default=st.session_state.input_drugs)

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Check Interactions"):
        st.session_state.input_drugs = selected_drugs
        if len(selected_drugs) < 2:
            st.warning("Please select at least two drugs.")
            st.session_state.results = []
        else:
            st.session_state.results = check_all_interactions(selected_drugs)
with col2:
    if st.button("🧹 Clear"):
        st.session_state.input_drugs = []
        st.session_state.results = None
        st.rerun()

# --- Results Display ---
if st.session_state.results is not None:
    results = st.session_state.results
    if len(results) > 0:
        st.success(f"{len(results)} interaction(s) found.")

        df = pd.DataFrame(results)

        # KPI Tiles
        high = sum(1 for r in results if r['Severity'] == 'high')
        moderate = sum(1 for r in results if r['Severity'] == 'moderate')
        low = sum(1 for r in results if r['Severity'] == 'low')
        k1, k2, k3 = st.columns(3)
        k1.metric("🔴 High Severity", high)
        k2.metric("🟠 Moderate Severity", moderate)
        k3.metric("🟢 Low Severity", low)

        # Expandable Interaction Details
        st.subheader("📋 Interaction Details")

        def severity_badge(severity):
            return {
                'high': '🔴 **High Severity**',
                'moderate': '🟠 **Moderate Severity**',
                'low': '🟢 **Low Severity**'
            }.get(severity.lower(), f"⚪ **{severity.capitalize()}**")

        for i, row in df.iterrows():
            with st.expander(f"💊 {row['Drug 1']} + {row['Drug 2']} — {severity_badge(row['Severity'])}"):
                st.markdown(f"🧪 **Risk:** `{row['Risk']}`")
                st.markdown(f"💡 **Recommendation:** _{row['Recommendation']}_")
                tts_col1, tts_col2 = st.columns([1, 5])
                with tts_col1:
                    if st.button("🔊", key=f"tts_{i}"):
                        engine = pyttsx3.init()
                        engine.say(f"Warning: {row['Risk']}. Recommendation: {row['Recommendation']}")
                        engine.runAndWait()
                with tts_col2:
                    st.markdown("*Click speaker icon to hear this interaction.*")
            st.markdown("---")

        # Pie Chart
        st.subheader("📊 Severity Distribution")
        severity_counts = df['Severity'].value_counts()

        color_map = {
                'high': 'red',
                'moderate': 'orange',
                'low': 'green'
            }

        fig = px.pie(
        names=severity_counts.index,
        values=severity_counts.values,
        title="Severity Breakdown",
        color=severity_counts.index,
        color_discrete_map=color_map
    )
        st.plotly_chart(fig)


        # Network Graph
        st.subheader("🌐 Animated Interaction Network")
        graph_path = generate_graph(results)
        with open(graph_path, 'r', encoding='utf-8') as f:
            html = f.read()
        components.html(html, height=570, scrolling=True)

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "drug_interactions.csv", "text/csv")
    else:
        st.info("✅ No harmful interactions found.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ☕︎ using PyDatalog, Pyvis, Plotly, and Streamlit 1.40")