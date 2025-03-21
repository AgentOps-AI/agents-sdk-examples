import streamlit as st
import asyncio
from real_estate_agent import real_estate_agent, Runner

# Set page configuration
st.set_page_config(
    page_title="Real Estate Assistant",
    page_icon="🔑",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the Real Estate Assistant! I can help you find properties, understand mortgage options, and learn about neighborhoods. How can I help you today?"}
    ]

# Page header
st.title("🏠 Real Estate Assistant")
st.markdown("Find properties, understand mortgages, and explore neighborhoods")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar="🔑"):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar="👤"):
            st.markdown(message["content"])

# Function to process user input
async def process_query(query):
    try:
        result = await Runner.run(real_estate_agent, query)
        return result.final_output
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Chat input
if prompt := st.chat_input("What real estate information are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant", avatar="🔑"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Process the query
        response = asyncio.run(process_query(prompt))
        
        # Update the placeholder with the response
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response}) 