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
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .persona-card { padding: 25px; border-radius: 12px; background-color: white; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); min-height: 350px; }
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
                
                persona_prompt = f"""
                Create 2 detailed UX personas for {product_name}. 
                Product Vision: {product_desc}. 
                Target Segment: {target_audience}. 
                Challenges: {user_goals}.
                
                Return ONLY a JSON object in this format: 
                {{
                  "personas": [
                    {{
                      "name": "Full Name",
                      "role": "Brief Role",
                      "bio": "1-2 sentence background",
                      "pain_points": ["point 1", "point 2"],
                      "goals": ["goal 1", "goal 2"]
                    }}
                  ]
                }}
                """

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a Senior AI Product Manager. You must return ONLY a JSON object."},
                        {"role": "user", "content": persona_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                
                raw_data = json.loads(response.choices[0].message.content)
                status.update(label="✅ User Segments Defined!", state="complete")

            # --- RENDER PERSONA CARDS ---
            st.divider()
            st.header("👤 Strategic User Personas")
            p_cols = st.columns(len(raw_data['personas']))
            
            for i, persona in enumerate(raw_data['personas']):
                with p_cols[i]:
                    pain_points_html = "".join([f"<li>{p}</li>" for p in persona['pain_points']])
                    goals_html = "".join([f"<li>{g}</li>" for g in persona['goals']])
                    
                    st.markdown(f"""
                    <div class="persona-card">
                        <h2 style='margin-top:0;'>{persona['name']}</h2>
                        <p><strong>{persona['role']}</strong></p>
                        <p style='font-style: italic; color: #555;'>"{persona['bio']}"</p>
                        <hr>
                        <strong>Top Pain Points:</strong>
                        <ul>{pain_points_html}</ul>
                        <strong>Primary Goals:</strong>
                        <ul>{goals_html}</ul>
                    </div>
                    """, unsafe_allow_html=True)

            # Step 2: Streaming Journey Map
            st.divider()
            st.header(f"🗺️ User Journey: {raw_data['personas'][0]['name']}")
            
            with st.spinner("Mapping the user journey..."):
                journey_stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Create a 5-stage User Journey Table for an AI Product Manager PRD. Use Markdown table format."},
                        {"role": "user", "content": f"Create a journey for {raw_data['personas'][0]['name']} using {product_name}. Include Awareness, Consideration, Onboarding, Core Action, and Post-Usage."}
                    ],
                    stream=True
                )
                
                placeholder = st.empty()
                full_journey = ""
                for chunk in journey_stream:
                    if chunk.choices[0].delta.content:
                        full_journey += chunk.choices[0].delta.content
                        placeholder.markdown(full_journey + "▌")
                placeholder.markdown(full_journey)

            # --- POST-GENERATION METRICS ---
            end_time = time.time()
            st.success(f"Strategy artifacts generated in {round(end_time - start_time, 2)} seconds.")
            
            st.download_button(
                label="📥 Export Artifacts to PRD",
                data=full_journey,
                file_name=f"{product_name}_UX_Strategy.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Operational Error: {e}")

# --- FOOTER ---
st.divider()
st.markdown(
    "<center class='metric-text'>Developed by <b>Pakhi Garg</b> | B.Arch + MCA | AI Technical Product Manager Portfolio</center>", 
    unsafe_allow_html=True
)