import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Configure the Streamlit page
st.set_page_config(page_title="GenAI Persona Builder", page_icon="🧑‍🤝‍🧑")
st.title("🧑‍🤝‍🧑 GenAI UX Persona & Journey Builder")
st.markdown("Instantly generate alignment personas and user journey maps to kickstart your UX discovery phase.")

# Sidebar for API Key
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Form for user inputs
with st.form("persona_form"):
    product_desc = st.text_input("Product Description", "e.g., A mobile app that helps remote workers find quiet cafes.")
    age_group = st.text_input("Target Audience Age Group", "e.g., 25-40")
    user_goals = st.text_area("Primary User Goals", "e.g., Find reliable Wi-Fi, avoid loud environments, discover new neighborhoods.")
    
    submitted = st.form_submit_button("Generate UX Artifacts")

    # Validation
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter a valid OpenAI API key in the sidebar.", icon="⚠")

    # Execution
    if submitted and openai_api_key.startswith("sk-"):
        with st.spinner("Synthesizing UX profiles..."):
            
            # Initialize the LLM
            llm = ChatOpenAI(temperature=0.7, api_key=openai_api_key, model="gpt-3.5-turbo")
            
            # Craft the UX-specific prompt
            prompt_text = """
            You are an Expert UX Researcher. The product team is building a new product.
            
            Product Context:
            - Description: {product}
            - Target Age Group: {age}
            - User Goals: {goals}
            
            Task 1: Generate 2 distinct fictional UX personas (assumptions-based) for this audience.
            For each persona, format clearly and include:
            - Name, Age, and Occupation
            - A brief background story
            - Needs & Goals
            - Pain Points & Frustrations
            
            Task 2: Create a simple User Journey Map for Persona #1 interacting with this product.
            Include these stages: 1) Awareness, 2) Consideration, 3) First Use/Onboarding, 4) Core Action, 5) Post-Usage.
            For each stage, briefly list:
            - User Actions
            - User Thoughts
            - Potential Frustrations
            """
            
            prompt = PromptTemplate.from_template(prompt_text)
            chain = prompt | llm
            
            # Run the chain and display results
            try:
                response = chain.invoke({
                    "product": product_desc,
                    "age": age_group,
                    "goals": user_goals
                })
                st.success("Artifacts Generated Successfully!")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"An API error occurred: {e}")