import streamlit as st
from langchain_openai import OpenAI  

st.set_page_config(page_title="My ChatGPT", page_icon="🤖")
st.title("... My ChatGPT ...")

# Sidebar for API key
openai_api_key = st.sidebar.text_input("🔑 Add Your OpenAI API Key", type="password")

# Store chat history in session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize LLM
llm = None
if openai_api_key.startswith("sk-"):
    try:
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    except Exception as e:
        st.error(f" Failed to connect: {e}")


def generate_response(user_input):
    """Generate response from OpenAI LLM."""
    try:
        return llm(user_input)
    except Exception as e:
        return f"Error: {str(e)}"


# Input form
with st.form("chat_form"):
    text = st.text_area(" Enter your message:", placeholder="Ask me anything...")
    submitted = st.form_submit_button("Send")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter a valid OpenAI API key!")

    if submitted and llm:
        response = generate_response(text)
        # Save chat history
        st.session_state["messages"].append(("You", text))
        st.session_state["messages"].append(("AI", response))


# Show chat history
for sender, msg in st.session_state["messages"]:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")
