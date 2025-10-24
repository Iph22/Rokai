# ui_agents.py
import streamlit as st
import requests

st.set_page_config(
    page_title="Arcyn Eye Agents",
    page_icon="👁️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { color: #D4AF37; }
    .agent-card {
        background: #1a1a1a;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 👁️ Arcyn Eye Agent System")
st.markdown("### *Choose Your Intelligence Interface*")
st.markdown("---")

# Agent selector
col1, col2, col3, col4 = st.columns(4)

agents = {
    "eye-1": {"name": "Eye-1", "icon": "👁️", "color": "yellow", "desc": "General Assistant"},
    "eye-1.3": {"name": "Eye-1.3", "icon": "💻", "color": "blue", "desc": "Developer Agent"},
    "eye-2": {"name": "Eye-2", "icon": "📊", "color": "green", "desc": "System Observer"},
    "eye-3": {"name": "Eye-3", "icon": "🎨", "color": "purple", "desc": "Creative Agent"}
}

with col1:
    if st.button("👁️ Eye-1\nGeneral", use_container_width=True):
        st.session_state.agent = "eye-1"
        
with col2:
    if st.button("💻 Eye-1.3\nDeveloper", use_container_width=True):
        st.session_state.agent = "eye-1.3"
        
with col3:
    if st.button("📊 Eye-2\nObserver", use_container_width=True):
        st.session_state.agent = "eye-2"
        
with col4:
    if st.button("🎨 Eye-3\nCreative", use_container_width=True):
        st.session_state.agent = "eye-3"

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = "eye-1"

# Display current agent
current_agent = agents[st.session_state.agent]
st.markdown(f"### Current Agent: {current_agent['icon']} {current_agent['name']} - {current_agent['desc']}")

st.markdown("---")

# Input section
col_name, col_mode = st.columns([2, 1])

with col_name:
    user_name = st.text_input("Your name", value="Dave", label_visibility="collapsed", placeholder="Your name")

with col_mode:
    smart_routing = st.checkbox("Smart Routing", value=False, help="Let Rokai choose the best agent automatically")

# Message input
user_message = st.text_area(
    "Message",
    placeholder=f"Ask {current_agent['name']} anything...",
    height=120,
    label_visibility="collapsed"
)

# Send button
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    send_button = st.button("⚡ SEND", use_container_width=True, type="primary")

# Process message
if send_button:
    if user_message:
        with st.spinner(f"{current_agent['icon']} {current_agent['name']} is thinking..."):
            try:
                # Choose endpoint based on routing mode
                if smart_routing:
                    endpoint = "http://127.0.0.1:8000/ask/smart"
                else:
                    endpoint = f"http://127.0.0.1:8000/agent/{st.session_state.agent}"
                
                # Send request
                response = requests.post(
                    endpoint,
                    json={
                        "user": user_name,
                        "text": user_message
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Show which agent responded
                    st.markdown("---")
                    agent_icon = agents.get(data.get("agent_id", st.session_state.agent), {}).get("icon", "👁️")
                    st.markdown(f"### {agent_icon} {data['agent']} Response")
                    
                    if smart_routing and data.get("routing") == "automatic":
                        st.info(f"🎯 Smart routing selected: {data['agent']}")
                    
                    # Display response
                    st.markdown(f"**{data['response']}**")
                    
                else:
                    st.error("⚠️ Connection error. Ensure backend is running.")
                    
            except requests.exceptions.Timeout:
                st.error("⚠️ Request timeout. Agent is processing complex query.")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
    else:
        st.warning("⚡ Please enter a message")

# Sidebar - Agent info
with st.sidebar:
    st.markdown("## 🧠 Rokai Core")
    st.markdown("### Eye Agent System v0.3")
    
    st.markdown("---")
    
    st.markdown("### Available Agents")
    for agent_id, agent_info in agents.items():
        st.markdown(f"{agent_info['icon']} **{agent_info['name']}**")
        st.caption(agent_info['desc'])
        st.markdown("")
    
    st.markdown("---")
    
    st.markdown("### System Status")
    try:
        status = requests.get("http://127.0.0.1:8000/", timeout=2)
        if status.status_code == 200:
            st.success("✓ Backend Online")
        else:
            st.error("✗ Backend Error")
    except:
        st.error("✗ Backend Offline")
    
    st.markdown("---")
    st.caption("Powered by ARCYN EYE")