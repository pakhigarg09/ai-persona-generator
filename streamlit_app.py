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

# Custom CSS for a professional look
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# --- SIDEBAR: Product Governance ---
with st.sidebar:
    st.title("⚙️ Project Control")
    api_key = st.text_input("Groq API Key", type="password", help="Get yours at console.groq.com")
    st.divider()
    st.markdown("### 📊 Model Metrics")
    st.info("Model: **Llama-3.3-70b-Versatile**\n\nLatency: ~280 tokens/sec")
    st.divider()
    st.markdown("### 🛠️ TPM Methodology")
    st.caption("This tool uses **Few-Shot Prompting** and **System Role-Playing** to reduce hallucination in UX research artifacts.")

# --- MAIN UI ---
st.title("🎯 PersonaStream AI")
st.subheader("Autonomous UX Persona & Journey Mapping for Product Discovery")

# Input Section
col1, col2 = st.columns([1, 1])

with col1:
    product_name = st.text_input("Product Name", placeholder="e.g. EcoRoute")
    product_desc = st.text_area("Product Vision", placeholder="A mobile app for low-carbon travel planning...")

with col2:
    target_audience = st.text_input("Target Segment", placeholder="e.g. Gen-Z Eco-conscious Travelers")
    user_goals = st.text_area("Core User Problems", placeholder="Users find it hard to calculate carbon footprints for multi-modal trips...")

# --- CORE LOGIC ---
if st.button("Generate Discovery Artifacts"):
    if not api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    else:
        try:
            client = Groq(api_key=api_key)
            start_time = time.time()
            
            # 1. GENERATE PERSONAS
            with st.status("🚀 Synthesizing User Segments...", expanded=True) as status:
                st.write("Analyzing product vision...")
                
                # We use a System Prompt to ensure TPM-level quality
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a Senior AI Technical Product Manager. Output only valid JSON."},
                        {"role": "user", "content": f"""
                        Create 2 detailed UX personas for {product_name}. 
                        Context: {product_desc}. Target: {target_audience}. Goals: {user_goals}.
                        Return JSON format: {{"personas": [{{"name": "", "role": "", "bio": "", "pain_points": [], "goals": []}}]}}
                        """}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2 # Lower temperature for consistency
                )
                
                raw_data = json.loads(stream.choices[0].message.content)
                status.update(label="✅ Personas Generated!", state="complete")

            # --- DISPLAY PERSONAS IN CARDS ---
            st.divider()
            st.header("👤 AI-Generated Personas")
            p_cols = st.columns(len(raw_data['personas']))
            
            for i, persona in enumerate(raw_data['personas']):
                with p_cols[i]:
                    st.markdown(f"""
                    <div class="persona-card">
                        <h3>{persona['name']}</h3>
                        <p><b>Role:</b> {persona['role']}</p>
                        <p>{persona['bio']}</p>
                        <hr>
                        <b>Pain Points:</b>
                        <ul>{" ".join([f"<li>{p}</li>" for p in persona['pain_points']])}</ul>
                    </div>
                    """, unsafe_allow_index=True)

            # 2. GENERATE JOURNEY MAP (Streaming for UX)
            st.divider()
            st.header("🗺️ User Journey Map: " + raw_data['personas'][0]['name'])
            
            journey_stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Create a professional 5-stage User Journey Map table."},
                    {"role": "user", "content": f"Generate a journey map for {raw_data['personas'][0]['name']} using {product_name}."}
                ],
                stream=True
            )
            
            # Streaming the text for that "WOW" factor
            placeholder = st.empty()
            full_response = ""
            for chunk in journey_stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

            # --- METRICS BOX (TPM Value Add) ---
            end_time = time.time()
            st.toast(f"Artifacts generated in {round(end_time - start_time, 2)}s", icon="⚡")
            
            with st.expander("📂 Download Artifacts for PRD"):
                st.download_button("Export as Markdown", full_response, file_name="discovery_artifacts.md")

        except Exception as e:
            st.error(f"Product Logic Error: {e}")

# --- FOOTER ---
st.divider()
st.caption("Built by Pakhi Garg | Aspiring AI TPM | Leveraging LPU™ Inference Technology")