# ui.py
import streamlit as st
import requests

# Page config with Arcyn branding
st.set_page_config(
    page_title="Rokai Core Intelligence",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for black & gold theme
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #1a1a1a;
        color: #D4AF37;
        border: 1px solid #D4AF37;
    }
    .stButton button {
        background-color: #D4AF37;
        color: #000000;
        font-weight: bold;
        border: none;
    }
    .stButton button:hover {
        background-color: #FFD700;
    }
    h1 {
        color: #D4AF37;
        font-family: 'Space Grotesk', sans-serif;
    }
    p, label {
        color: #FFFFFF;
    }
    .success-box {
        background-color: #1a1a1a;
        border-left: 4px solid #D4AF37;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🧠 Rokai Core Intelligence")
st.markdown("### *Arcyn Intelligence Protocols Active*")
st.markdown("---")

# User input
col1, col2 = st.columns([1, 3])
with col1:
    user_name = st.text_input("Name", value="Dave", label_visibility="collapsed", placeholder="Your name")
with col2:
    st.empty()

# Message input
user_message = st.text_area(
    "Message", 
    placeholder="Ask Rokai anything about AI, systems, or Arcyn's future...",
    height=100,
    label_visibility="collapsed"
)

# Send button
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    send_button = st.button("⚡ SEND", use_container_width=True, type="primary")

# Process message
if send_button:
    if user_message:
        with st.spinner("🧠 Rokai is thinking..."):
            try:
                # Send to backend
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "user": user_name,
                        "text": user_message
                    },
                    timeout=30
                )
                
                # Display response
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("---")
                    st.markdown("### 🔱 Rokai Response")
                    st.markdown(f'<div class="success-box">{data["response"]}</div>', unsafe_allow_html=True)
                else:
                    st.error("⚠️ Connection error. Ensure backend is running.")
                    
            except requests.exceptions.Timeout:
                st.error("⚠️ Request timeout. Rokai is processing a complex query.")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
    else:
        st.warning("⚡ Please enter a message")

# Divider
st.markdown("---")

# History section
with st.expander("📚 View Conversation History"):
    if st.button("Load History"):
        try:
            history_response = requests.get("http://127.0.0.1:8000/history?limit=20")
            if history_response.status_code == 200:
                history = history_response.json()["messages"]
                st.markdown("### Recent Interactions")
                for msg in history:
                    role_icon = "👤" if msg["role"] == "user" else "🧠"
                    role_color = "#FFFFFF" if msg["role"] == "user" else "#D4AF37"
                    st.markdown(f'<p style="color: {role_color};">{role_icon} {msg["content"]}</p>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading history: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666666; font-size: 0.8rem;">Powered by Claude Sonnet 4 | Arcyn Intelligence v0.1</p>',
    unsafe_allow_html=True
)