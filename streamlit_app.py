import streamlit as st
from openai import OpenAI

# Configure the Streamlit page
st.set_page_config(page_title="GenAI Persona Builder", page_icon="🧑‍🤝‍🧑")
st.title("🧑‍🤝‍🧑 GenAI UX Persona & Journey Builder")
st.markdown("Instantly generate alignment personas and journey maps.")

# Sidebar for API Token
hf_api_token = st.sidebar.text_input("Enter Hugging Face Token (hf_...)", type="password")

# Form for user inputs
with st.form("persona_form"):
    product_desc = st.text_input("Product Description", "e.g., A mobile app for remote workers to find quiet cafes.")
    age_group = st.text_input("Target Audience Age Group", "e.g., 25-40")
    user_goals = st.text_area("Primary User Goals", "e.g., Reliable Wi-Fi, low noise, good coffee.")
    
    submitted = st.form_submit_button("Generate UX Artifacts")

    # Validation
    if not hf_api_token.startswith("hf_"):
        st.warning("Please enter a valid Hugging Face token in the sidebar.", icon="⚠")

    # Execution
    if submitted and hf_api_token.startswith("hf_"):
        with st.spinner("Synthesizing UX profiles..."):
            try:
                # 1. Initialize the client using the Hugging Face Router URL
                client = OpenAI(
                    base_url="https://router.huggingface.co/v1",
                    api_key=hf_api_token
                )

                # 2. Use a Chat Completion call (matches the 'conversational' requirement)
                # We append ':fastest' to the model name to let HF pick the best provider automatically
                response = client.chat.completions.create(
                    model="mistralai/Mistral-7B-Instruct-v0.3",
                    messages=[
                        {"role": "system", "content": "You are an Expert UX Researcher."},
                        {"role": "user", "content": f"""
                        Generate 2 distinct fictional UX personas and a simple journey map.
                        Product: {product_desc}
                        Age: {age_group}
                        Goals: {user_goals}
                        """}
                    ],
                    max_tokens=1024,
                    temperature=0.7
                )
                
                # 3. Display Result
                st.success("Artifacts Generated Successfully!")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An API error occurred: {e}")