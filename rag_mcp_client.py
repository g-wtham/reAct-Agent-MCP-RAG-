import streamlit as st
import asyncio
from fastmcp import Client

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp" 
TOOL_NAME = "retrieve_answer"

st.set_page_config(page_title="reAct RAG Agent + MCP", page_icon="💬")
st.title("reAct RAG Agent + MCP")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

import json

async def call_mcp_tool(prompt_text: str) -> str:
    client = Client(MCP_SERVER_URL)
    try:
        async with client:
            result = await client.call_tool(TOOL_NAME, {"prompt": prompt_text})
            # Extract the raw JSON string from content
            if result and hasattr(result, "content") and len(result.content) > 0:
                raw_json_str = result.content[0].text
                # Parse JSON string to Python dict
                parsed = json.loads(raw_json_str)
                # Extract the 'result' field which has the answer text
                answer_text = parsed.get("result", "No answer found in result.")
                return answer_text
            return "Server returned a response but no readable content."
    except Exception as e:
        return f"Error connecting to MCP Server or calling tool: {e}"


with st.form(key='query_form', clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    query = col1.text_input(
        "Ask a question about your documents:", 
        key="user_input", 
        label_visibility="collapsed"
    )
    submitted = col2.form_submit_button("Send")

if submitted and query:
    # Add user query to history
    st.session_state.chat_history.append({"role": "user", "content": query})

    with st.spinner("Connecting to MCP Server and retrieving answer..."):
        try:
            agent_answer = asyncio.run(call_mcp_tool(query))
        except RuntimeError as e:
            # Handle event loop already running scenario
            st.error(f"Error executing asynchronous code: {e}")
            agent_answer = "Execution error. Please ensure the MCP server is running correctly."

    st.session_state.chat_history.append({"role": "bot", "content": agent_answer})

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")
