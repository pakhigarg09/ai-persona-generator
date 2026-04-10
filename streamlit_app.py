import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage

# Configure the Streamlit page
st.set_page_config(page_title="GenAI Persona Builder", page_icon="🧑‍🤝‍🧑")
st.title("🧑‍🤝‍🧑 GenAI UX Persona & Journey Builder")
st.markdown("Instantly generate alignment personas and user journey maps to kickstart your UX discovery phase.")

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
        with st.spinner("Synthesizing UX profiles (This may take a moment if the model is waking up)..."):
            try:
                # 1. Initialize the Endpoint with a NEWER model (v0.3)
                # This model is currently the most stable on the free serverless tier.
                llm = HuggingFaceEndpoint(
                    repo_id="mistralai/Mistral-7B-Instruct-v0.3", 
                    huggingfacehub_api_token=hf_api_token,
                    max_new_tokens=1024,
                    temperature=0.7,
                    timeout=300 # Wait up to 5 mins for the model to load
                )
                
                # 2. Wrap in ChatHuggingFace
                chat_model = ChatHuggingFace(llm=llm)
                
                # 3. Build the prompt
                messages = [
                    SystemMessage(content="You are an Expert UX Researcher."),
                    HumanMessage(content=f"""
                    The product team is building a new product.
                    
                    Product Context:
                    - Description: {product_desc}
                    - Target Age Group: {age_group}
                    - User Goals: {user_goals}
                    
                    Task 1: Generate 2 distinct fictional UX personas for this audience. 
                    Include: Name, Age, Occupation, Background, Needs, and Pain Points.
                    
                    Task 2: Create a simple User Journey Map for Persona #1.
                    Include: Awareness, Consideration, First Use, Core Action, and Post-Usage.
                    For each stage list: User Actions and User Thoughts.
                    """)
                ]
                
                # 4. Get the response
                response = chat_model.invoke(messages)
                
                st.success("Artifacts Generated Successfully!")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"An API error occurred: {e}")
                st.info("💡 Pro-Tip: If you see a '503' error, the model is just 'waking up.' Wait 10 seconds and hit Submit again!")