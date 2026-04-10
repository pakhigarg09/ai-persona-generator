import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

# Configure the Streamlit page
st.set_page_config(page_title="GenAI Persona Builder", page_icon="🧑‍🤝‍🧑")
st.title("🧑‍🤝‍🧑 GenAI UX Persona & Journey Builder")
st.markdown("Instantly generate alignment personas and user journey maps to kickstart your UX discovery phase.")

# Sidebar for API Key
hf_api_token = st.sidebar.text_input("Enter Hugging Face Token (hf_...)", type="password")

# Form for user inputs
with st.form("persona_form"):
    product_desc = st.text_input("Product Description", "e.g., A mobile app that helps remote workers find quiet cafes.")
    age_group = st.text_input("Target Audience Age Group", "e.g., 25-40")
    user_goals = st.text_area("Primary User Goals", "e.g., Find reliable Wi-Fi, avoid loud environments, discover new neighborhoods.")
    
    submitted = st.form_submit_button("Generate UX Artifacts")

    # Validation
    if not hf_api_token.startswith("hf_"):
        st.warning("Please enter a valid Hugging Face token in the sidebar.", icon="⚠")

    # Execution
    if submitted and hf_api_token.startswith("hf_"):
        with st.spinner("Synthesizing UX profiles..."):
            try:
                # Initialize the free Hugging Face model (Mistral)
                llm = HuggingFaceEndpoint(
                    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                    temperature=0.7,
                    huggingfacehub_api_token=hf_api_token,
                    max_new_tokens=1024
                )
                
                # Craft the UX-specific prompt
                prompt_text = """
                You are an Expert UX Researcher. The product team is building a new product.
                
                Product Context:
                - Description: {product}
                - Target Age Group: {age}
                - User Goals: {goals}
                
                Task 1: Generate 2 distinct fictional UX personas for this audience.
                For each persona include: Name, Age, Occupation, Background story, Needs & Goals, and Pain Points.
                
                Task 2: Create a simple User Journey Map for Persona #1.
                Include these stages: 1) Awareness, 2) Consideration, 3) First Use/Onboarding, 4) Core Action, 5) Post-Usage.
                For each stage list: User Actions, User Thoughts, and Potential Frustrations.
                """
                
                prompt = PromptTemplate.from_template(prompt_text)
                chain = prompt | llm
                
                # Run the chain
                response = chain.invoke({
                    "product": product_desc,
                    "age": age_group,
                    "goals": user_goals
                })
                
                st.success("Artifacts Generated Successfully!")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"An API error occurred: {e}")