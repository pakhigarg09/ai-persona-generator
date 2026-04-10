import streamlit as st
from groq import Groq
import json
import time

# --- PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="PersonaStream AI | AI TPM Portfolio", 
    page_icon="🎯", 
    layout="wide"
)

# Professional CSS for a SaaS-ready look
# Fixed the 'unsafe_allow_html' parameter here
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .persona-card { padding: 25px; border-radius: 12px; background-color: white; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .metric-text { font-size: 0.9em; color: #6c757d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Governance & Technical Info ---
with st.sidebar:
    st.title("⚙️ Control Plane")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Enter your gsk_... key from console.groq.com")
    st.divider()
    st.markdown("### 📊 Model Info")
    st.info("**Provider:** Groq LPU™\n\n**Model:** Llama-3.3-70b-Versatile\n\n**Task:** Structural Discovery")
    st.divider()
    st.markdown("### 🛠️ PM Methodology")
    st.caption("This tool implements **System Role Prompting** to act as a Senior TPM, ensuring artifacts follow industry standards for product requirement documents (PRD).")

# --- MAIN UI ---
st.title("🎯 PersonaStream AI")
st.markdown("#### Autonomous Discovery Engine for AI Product Managers")

# Input Section
col1, col2 = st.columns([1, 1])

with col1:
    product_name = st.text_input("Product Name", value="EcoRoute", help="The name of your project or feature.")
    product_desc = st.text_area("Product Vision", placeholder="Describe the 'Why' and 'How' of your product...", height=150)

with col2:
    target_audience = st.text_input("Target Segment", placeholder="e.g. Solo-Preneurs, College Students...")
    user_goals = st.text_area("Primary User Challenges", placeholder="What are the main friction points they face today?", height=150)

# --- EXECUTION ENGINE ---
if st.button("Generate Strategy Artifacts"):
    if not groq_api_key:
        st.error("Missing API Key: Please add your Groq key in the sidebar.")
    elif not product_desc or not target_audience:
        st.warning("Incomplete Data: Please fill out the Product Vision and Target Segment.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            start_time = time.time()
            
            # Step 1: Structured Data Generation (JSON)
            with st.status("🚀 Synthesizing User Archetypes...", expanded=True) as status:
                st.write("Generating structured JSON persona data...")
                
                # Using JSON mode for predictable UI rendering
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a Senior AI Product Manager. You must return ONLY a JSON object."},
                        {"role": "user", "content": f"""
                        Create 2 detailed UX personas for {product_name}. 
                        Product Vision: {product_desc}. Target Segment: {target_audience}. Challenges: {user_goals}.
                        Return in this JSON format: 
                        {{
                          "personas": [
                            {{
                              "name": "Full Name",
                              "role": "Brief Role",
                              "