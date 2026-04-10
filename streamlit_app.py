import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="GenAI Persona Builder", page_icon="🧑‍🤝‍🧑")
st.title("🧑‍🤝‍🧑 GenAI UX Persona & Journey Builder")
st.markdown("Instantly generate alignment personas and journey maps using Groq (Llama 3).")

# Sidebar for API Key
groq_api_key = st.sidebar.text_input("Enter Groq API Key (gsk_...)", type="password")

with st.form("persona_form"):
    product_desc = st.text_input("Product Description", "e.g., A mobile app for remote workers to find quiet cafes.")
    age_group = st.text_input("Target Audience Age Group", "e.g., 25-40")
    user_goals = st.text_area("Primary User Goals", "e.g., Reliable Wi-Fi, low noise, good coffee.")
    
    submitted = st.form_submit_button("Generate UX Artifacts")

    if not groq_api_key.startswith("gsk_"):
        st.warning("Please enter your Groq API key in the sidebar.")

    if submitted and groq_api_key.startswith("gsk_"):
        with st.spinner("Synthesizing UX profiles at warp speed..."):
            try:
                client = Groq(api_key=groq_api_key)
                
                # Using Llama-3.3-70b - one of the most powerful free models available on Groq
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an Expert UX Researcher specializing in empathy mapping."},
                        {"role": "user", "content": f"""
                        Based on these details, generate 2 personas and a user journey map.
                        Product: {product_desc}
                        Target Age: {age_group}
                        Goals: {user_goals}

                        Task 1: 2 Personas (Name, Age, Occupation, Story, Needs, Pain Points).
                        Task 2: Journey Map for Persona #1 (Awareness, Consideration, First Use, Core Action, Post-Usage).
                        """}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                st.success("Artifacts Generated!")
                st.markdown(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error: {e}")