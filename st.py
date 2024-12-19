import streamlit as st
import requests

# Backend URL
backend_url = "https://6ae3-2001-8f8-1d36-9fda-2048-2b33-cc9c-1d02.ngrok-free.app"  # Update with the deployed backend URL

# Add custom CSS for styling
st.markdown(
    """
    <style>
    .chat-history {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        max-height: 300px;
        overflow-y: auto;
        margin-bottom: 20px;
        direction: rtl; /* For Arabic content */
        text-align: right;
        color: #000; /* Default text color */
    }
    .chat-entry {
        margin-bottom: 10px;
    }
    .user {
        color: #007bff; /* Blue for user */
    }
    .model {
        color: #28a745; /* Green for model */
    }
    textarea {
        direction: ltr !important; /* Ensure text box is left-to-right */
        text-align: left !important; /* Ensure text box text alignment */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Arabic Smart Chatbot")

# Sidebar for Reset Chat and Health Check
with st.sidebar:
    st.subheader("Options")
    
    # Reset chat history
    st.subheader("Reset Chat History")
    reset_user_id = st.text_input("Reset User ID", placeholder="Enter the User ID to reset")
    if st.button("Reset Chat", key="reset_button"):
        if reset_user_id:
            try:
                response = requests.post(
                    f"{backend_url}/reset/",
                    data={"user_id": reset_user_id},
                )
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(f"Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please provide a User ID to reset.")

    # Health check
    st.subheader("Health Check")
    if st.button("Check Health"):
        try:
            response = requests.get(f"{backend_url}/health")
            if response.status_code == 200:
                st.success("Server is running and healthy.")
            else:
                st.error("Server is unhealthy.")
        except Exception as e:
            st.error(f"Health check failed: {e}")

# Main chat section
st.subheader("Chat with the AI")

# Step 1: Get User ID
user_id = st.text_input("User ID", placeholder="Enter your user ID")
chat_history = []

if user_id:
    # Chat history container
    st.markdown("### Chat History")
    chat_history_container = st.empty()

    # Step 2: Query input and chat display
    query = st.text_area("Query", placeholder="Type your question here...", height=150)
    if st.button("Send Query"):
        if query:
            try:
                response = requests.post(
                    f"{backend_url}/chat/",
                    data={"user_id": user_id, "query": query},
                )
                if response.status_code == 200:
                    data = response.json()
                    
                    # Update chat history
                    for item in data["history"]:
                        chat_history.append(
                            f"<div class='chat-entry'><span class='user'>{item['role']}</span>: {item['content']}</div>"
                            if item["role"] == "user"
                            else f"<div class='chat-entry'><span class='model'>{item['role']}</span>: {item['content']}</div>"
                        )
                    
                    # Display chat history
                    chat_history_container.markdown(
                        f"<div class='chat-history'>{''.join(chat_history)}</div>",
                        unsafe_allow_html=True,
                    )

                else:
                    st.error(f"Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please provide a query.")
else:
    st.info("Please enter a User ID to start chatting.")
