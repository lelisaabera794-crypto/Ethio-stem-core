import streamlit as st
import streamlit.components.v1 as components
from google import genai
import pandas as pd
import json
import re
from datetime import datetime

st.set_page_config(
page_title="ETHIO-STEM National Infrastructure",
page_icon="🇪🇹",
layout="wide"
)

# --- NATIONAL TELEMETRY STATE ---
if "national_db" not in st.session_state:
st.session_state.national_db = [
{
"Date": "2026-11-24",
"Region": "Addis Ababa",
"Subject": "Physics",
"Grade": "Grade 10",
"Concept": "Electric Current (Water-in-Pipe Analogy)",
"Risk_Score": 8.5,
"Root_Cause": "Confuses drift velocity with signal speed; implies empty wires fill up.",
"Action": "Mandatory Textbook Revision"
},
{
"Date": "2026-11-24",
"Region": "Oromia",
"Subject": "Chemistry",
"Grade": "Grade 9",
"Concept": "Atomic Orbitals (Solar System Model)",
"Risk_Score": 9.2,
"Root_Cause": "Teaches fixed circular orbits instead of quantum probability clouds.",
"Action": "Deploy Simulation & Teacher Guide"
},
{
"Date": "2026-11-24",
"Region": "Amhara",
"Subject": "Biology",
"Grade": "Grade 11",
"Concept": "Enzymes (Rigid Lock-and-Key)",
"Risk_Score": 6.8,
"Root_Cause": "Ignores Induced Fit conformational flexibility.",
"Action": "Add Supplementary Digital Lab"
}
]

if "active_concept" not in st.session_state:
st.session_state.active_concept = ""
if "last_audit" not in st.session_state:
st.session_state.last_audit = ""
if "last_sim_html" not in st.session_state:
st.session_state.last_sim_html = ""
if "last_lesson_plan" not in st.session_state:
st.session_state.last_lesson_plan = ""

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
st.title("🇪🇹 ETHIO-STEM CORE")
st.caption("National Curriculum & Simulation Grid")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
api_key = st.text_input("Enter Gemini API Key", type="password", placeholder="AIza...")
else:
st.success("● National AI Grid Online")

st.divider()
region = st.selectbox("Regional Bureau", [
"Addis Ababa", "Oromia", "Amhara", "Tigray", "Sidama",
"South Ethiopia", "Central Ethiopia", "Somali", "Afar", "Dire Dawa"
])
subject = st.selectbox("STEM Subject", ["Physics", "Chemistry", "Biology"])
grade = st.selectbox("Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Freshman University"])
lab_access = st.selectbox("School Infrastructure Tier", [
"Tier 1: Zero Lab Equipment (Chalkboard + Phone)",
"Tier 2: Basic Lab Equipment",
"Tier 3: Smart Classroom / Computer Lab"
])

def get_client():
if not api_key:
st.warning("⚠️ Please enter your Gemini API Key in the sidebar first.")
st.stop()
return genai.Client(api_key=api_key)

# --- MAIN HEADER ---
st.title("🇪🇹 National Analogy Misconception & Simulation Infrastructure")
st.markdown("**Micro-Concept Forensics • Dynamic Parameter Simulations • Offline School-in-a-Box • Ministry Telemetry**")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
"🔬 1. Misconception Forensics",
"🎛️ 2. Simulation Engine",
"📚 3. Lesson Architect",
"📦 4. Offline Export",
"🏛️ 5. Ministry Telemetry"
])

# ==========================================
# TAB 1: MICRO-CONCEPT & ANALOGY FORENSICS
# ==========================================
with tab1:
st.subheader("Word-by-Word Textbook & Analogy Forensics")
default_text = (
"Electric current flows through a wire just like water flows through a garden hose. "
"The battery acts as a water pump pushing electrons through the pipe."
)
user_text = st.text_area("Paste Textbook Excerpt or Classroom Analogy:", value=default_text, height=120)

if st.button("🚀 Run Deep Cognitive Forensics", type="primary"):
if user_text.strip():
client = get_client()
with st.spinner("Analyzing micro-concepts, linguistic traps, and scientific accuracy..."):
prompt = f"""
You are the Chief STEM Curriculum Specialist for the Ethiopian Ministry of Education ({subject}, {grade}, {region}, {lab_access}).
Analyze this textbook text or analogy deeply from first principles:
"{user_text}"

Provide 5 clear, rigorous sections:
### 1. First-Principles Micro-Concept Breakdown
Explain the exact underlying physical/chemical/biological mechanism at the fundamental level so there is zero ambiguity.
### 2. Lexical & Analogy Breakdown (Where It Fails)
Quote exact words/phrases that cause student misconceptions and explain the exact scientific boundary where the analogy breaks down.
### 3. Amharic-English Translation Trap Diagnosis
Identify how translating these terms into Amharic creates classroom confusion and give the accurate bilingual phrasing.
### 4. Scientifically Accurate Replacement
Rewrite the explanation so it is vivid, intuitive, adapted to {lab_access}, and misconception-free.
### 5. Diagnostic Check Question
Give 1 Socratic question that exposes whether a student holds this misconception.

At the very end, output ONE line formatted strictly like this:
TELEMETRY_JSON: {{"concept": "Short Concept Name", "risk": 8.5, "root_cause": "Short root cause", "action": "Recommended Action"}}
"""
res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
full_out = res.text
clean_out = full_out

match = re.search(r'TELEMETRY_JSON:\s*(\{.*\})', full_out)
if match:
clean_out = full_out[:match.start()].strip()
try:
meta = json.loads(match.group(1))
st.session_state.active_concept = meta.get("concept", user_text[:35])
st.session_state.national_db.append({
"Date": datetime.now().strftime("%Y-%m-%d"),
"Region": region,
"Subject": subject,
"Grade": grade,
"Concept": st.session_state.active_concept,
"Risk_Score": float(meta.get("risk", 7.5)),
"Root_Cause": meta.get("root_cause", "Analogy breakdown"),
"Action": meta.get("action", "Curriculum Revision")
})
except Exception:
st.session_state.active_concept = user_text[:35]
else:
st.session_state.active_concept = user_text[:35]

st.session_state.last_audit = clean_out
st.success(f"✅ Audited & Logged to Ministry Dashboard: **{st.session_state.active_concept}**")

if st.session_state.last_audit:
st.markdown(st.session_state.last_audit)
st.download_button("📥 Download Forensic Audit (.txt)", st.session_state.last_audit, file_name="Misconception_Audit.txt")

# ==========================================
# TAB 2: UNLIMITED SIMULATION ENGINE
# ==========================================
with tab2:
st.subheader("Dynamic Parameter Simulation Engine")
sim_topic = st.text_input(
"Concept to Simulate:",
value=st.session_state.active_concept,
placeholder="e.g., Ohm's Law, Projectile Motion, Enzyme Kinetics, Ideal Gas Law..."
)

if st.button("⚡ Generate Interactive Simulation", type="primary"):
if sim_topic.strip():
client = get_client()
with st.spinner(f"Deriving governing equations and compiling HTML5 simulation for {sim_topic}..."):
sim_prompt = f"""
Create a complete, self-contained, interactive HTML5 + CSS + JavaScript scientific simulation for {subject} ({grade}) on: "{sim_topic}".
Strict rules:
1. Output ONLY raw valid HTML starting with <!DOCTYPE html> and ending with </html>. Do NOT include ```html markdown fences or any text outside the HTML.
2. Identify 3 to 4 real scientific parameters for "{sim_topic}" with proper units and create smooth HTML range sliders with live numeric readouts.
3. Include an animated HTML5 <canvas> that updates smoothly in real time using requestAnimationFrame based on the real mathematical equations of "{sim_topic}".
4. Include Play/Pause and Reset buttons, plus a small on-screen "Misconception Guardrail" note showing what happens at extreme values.
5. Use a clean dark theme, high-contrast labels, and 100% responsive width suitable for mobile phones.
"""
sim_res = client.models.generate_content(model="gemini-2.5-flash", contents=sim_prompt)
html_code = sim_res.text.strip()
html_code = re.sub(r'^```html\s*', '', html_code)
html_code = re.sub(r'\s*```$', '', html_code)
st.session_state.last_sim_html = html_code
st.session_state.active_concept = sim_topic

if st.session_state.last_sim_html:
st.success(f"🟢 Live Simulation Ready: **{st.session_state.active_concept}**")
components.html(st.session_state.last_sim_html, height=580, scrolling=True)
st.download_button(
"📥 Download Offline Simulation (.html)",
data=st.session_state.last_sim_html,
