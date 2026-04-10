import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate  # <--- This is the 2026 correct path

# ... (the rest of your code remains the same)

# Configure the Streamlit page
st.set_page_config(page_title="GenAI Persona Builder", page_icon="🧑‍🤝‍🧑")
st.title("🧑‍🤝‍🧑 GenAI UX Persona & Journey Builder")
st.markdown("Instantly generate alignment personas and journey maps using Mistral AI.")

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
                # 1. Initialize the Endpoint directly
                # We use task="text-generation" to match what the free API expects
                llm = HuggingFaceEndpoint(
                    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
                    task="text-generation",
                    huggingfacehub_api_token=hf_api_token,
                    max_new_tokens=1024,
                    temperature=0.7
                )
                
                # 2. Use a standard PromptTemplate (No ChatWrapper needed)
                template = """<s>[INST] You are an Expert UX Researcher. Based on the details below, generate 2 personas and a user journey map.

                Product: {product}
                Target Age: {age}
                Goals: {goals}

                Task 1: Generate 2 distinct fictional UX personas (Name, Age, Occupation, Story, Needs, Pain Points).
                Task 2: Create a simple User Journey Map for Persona #1 (Awareness, Consideration, First Use, Core Action, Post-Usage). [/INST]</s>"""

                prompt = PromptTemplate.from_template(template)
                
                # 3. Simple Chain: Prompt | LLM
                chain = prompt | llm
                
                # 4. Run and Display
                response = chain.invoke({
                    "product": product_desc,
                    "age": age_group,
                    "goals": user_goals
                })
                
                st.success("Artifacts Generated Successfully!")
                st.markdown(response)
                
            except Exception as e:
                st.error(f"An API error occurred: {e}")