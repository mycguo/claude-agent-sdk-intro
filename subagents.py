"""
Subagents are a way to delegate tasks to specialized agents.

Advantages include:
- Context isolation: Subagents have their own context and do not share it with the main agent.
- Tool isolation: Subagents can have their own set of allowed tools, which can be useful for security and manageability.
- Parallelization: Subagents can run in parallel, which can improve performance.

For more details, see: https://docs.claude.com/en/api/agent-sdk/subagents

This is a Streamlit app version of the subagents example.
"""

import streamlit as st
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Kaya - Your Personal Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = None
if "model" not in st.session_state:
    st.session_state.model = "sonnet"


def get_claude_options(model: str):
    """Configure Claude agent options with subagents."""
    return ClaudeAgentOptions(
        model=model,
        permission_mode="acceptEdits",
        setting_sources=["project"],
        allowed_tools=[
            'Read',
            'Write',
            'Edit',
            'MultiEdit',
            'Grep',
            'Glob',
            # Task tool is required to use subagents!
            'Task',
            'TodoWrite',
            'WebSearch',
            'WebFetch',
            'mcp__Playwright__browser_close',
            'mcp__Playwright__browser_resize',
            'mcp__Playwright__browser_console_messages',
            'mcp__Playwright__browser_handle_dialog',
            'mcp__Playwright__browser_evaluate',
            'mcp__Playwright__browser_file_upload',
            'mcp__Playwright__browser_fill_form',
            'mcp__Playwright__browser_install',
            'mcp__Playwright__browser_press_key',
            'mcp__Playwright__browser_type',
            'mcp__Playwright__browser_navigate',
            'mcp__Playwright__browser_navigate_back',
            'mcp__Playwright__browser_network_requests',
            'mcp__Playwright__browser_take_screenshot',
            'mcp__Playwright__browser_snapshot',
            'mcp__Playwright__browser_click',
            'mcp__Playwright__browser_drag',
            'mcp__Playwright__browser_hover',
            'mcp__Playwright__browser_select_option',
            'mcp__Playwright__browser_tabs',
            'mcp__Playwright__browser_wait_for',
        ],
        # We can also specify allowed tools for subagents, by default they inherit all tools including MCP tools.
        agents={
            "youtube-analyst": AgentDefinition(
                description="An expert at analyzing a user's Youtube channel performance. The analyst will produce a markdown report in the /docs directory.",
                prompt="You are an expert at analyzing YouTube data and helping the user understand their performance. You can use the Playwright browser tools to access the user's Youtube Studio. Generate a markdown report in the /docs directory.",
                model="sonnet",
                tools=[
                    'Read',
                    'Write',
                    'Edit',
                    'MultiEdit',
                    'Grep',
                    'Glob',
                    'TodoWrite',
                    'mcp__Playwright__browser_close',
                    'mcp__Playwright__browser_resize',
                    'mcp__Playwright__browser_console_messages',
                    'mcp__Playwright__browser_handle_dialog',
                    'mcp__Playwright__browser_evaluate',
                    'mcp__Playwright__browser_file_upload',
                    'mcp__Playwright__browser_fill_form',
                    'mcp__Playwright__browser_install',
                    'mcp__Playwright__browser_press_key',
                    'mcp__Playwright__browser_type',
                    'mcp__Playwright__browser_navigate',
                    'mcp__Playwright__browser_navigate_back',
                    'mcp__Playwright__browser_network_requests',
                    'mcp__Playwright__browser_take_screenshot',
                    'mcp__Playwright__browser_snapshot',
                    'mcp__Playwright__browser_click',
                    'mcp__Playwright__browser_drag',
                    'mcp__Playwright__browser_hover',
                    'mcp__Playwright__browser_select_option',
                    'mcp__Playwright__browser_tabs',
                    'mcp__Playwright__browser_wait_for',
                ]
            ),
            "researcher": AgentDefinition(
                description="An expert researcher and documentation writer. The agent will perform deep research of a topic and generate a report or documentation in the /docs directory.",
                prompt="You are an expert researcher and report/documentation writer. Use the WebSearch and WebFetch tools to perform research. You can research multiple subtopics/angles to get a holistic understanding of the topic. You can use filesystem tools to track findings and data in the /docs directory. For longer reports, you can break the work into multiple tasks or write sections at a time. But the final output should be a single markdown report. The final report **MUST** include a citations section with links to all sources used. Review the full report, identify any areas for improvement in readability, cohorerence, and relevancy, and make any necessary edits before declaring the task complete. Clean up any extraneous files and only leave the final report in the /docs directory when you are done. You are only permitted to use these specific tools: Read, Write, Edit, MultiEdit, Grep, Glob, TodoWrite, WebSearch, WebFetch. All other tools are prohibited.",
                model="sonnet",
                tools=[
                    'Read',
                    'Write',
                    'Edit',
                    'MultiEdit',
                    'Grep',
                    'Glob',
                    'TodoWrite',
                    'WebSearch',
                    'WebFetch',
                ]
            ),
            "events_agent": AgentDefinition(
                description="You are gathering incoming AI events in bay area. Asking for the input of how many days you want to check, search for sources from https://luma.com/sf, Meetup, eventbrite, startupgrind, Y combinator, 500 startups, Andreessen Horowitz (a16z), Stanford Events, Berkeley Events, LinkedIn Events, Silicon Valley Forum, Galvanize, StrictlyVC, Bay Area Tech Events, cerebralvalley.ai/events , you must include RSVP URL.",
                prompt="You are searching for AI events in the next few days. Ask for how many days in advance. Gather the events, make sure to include short description, location and RSVP URL",
                model="sonnet",
                tools=[
                    'Read',
                    'Write',
                    'Edit',
                    'MultiEdit',
                    'Grep',
                    'Glob',
                    'TodoWrite',
                    'mcp__Playwright__browser_close',
                    'mcp__Playwright__browser_resize',
                    'mcp__Playwright__browser_console_messages',
                    'mcp__Playwright__browser_handle_dialog',
                    'mcp__Playwright__browser_evaluate',
                    'mcp__Playwright__browser_file_upload',
                    'mcp__Playwright__browser_fill_form',
                    'mcp__Playwright__browser_install',
                    'mcp__Playwright__browser_press_key',
                    'mcp__Playwright__browser_type',
                    'mcp__Playwright__browser_navigate',
                    'mcp__Playwright__browser_navigate_back',
                    'mcp__Playwright__browser_network_requests',
                    'mcp__Playwright__browser_take_screenshot',
                    'mcp__Playwright__browser_snapshot',
                    'mcp__Playwright__browser_click',
                    'mcp__Playwright__browser_drag',
                    'mcp__Playwright__browser_hover',
                    'mcp__Playwright__browser_select_option',
                    'mcp__Playwright__browser_tabs',
                    'mcp__Playwright__browser_wait_for',
                ]
            )
        },
        # Note: Playwright requires Node.js and Chrome to be installed!
        mcp_servers={
            "Playwright": {
                "command": "npx",
                "args": [
                    "-y",
                    "@playwright/mcp@latest"
                ]
            }
        }
    )


async def process_message(user_input: str, model: str):
    """Process user message and get response from Claude."""
    options = get_claude_options(model)

    async with ClaudeSDKClient(options=options) as client:
        await client.query(user_input)

        response_text = ""
        async for message in client.receive_response():
            # Extract text content from the message
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_text += content_block.text
                elif hasattr(message.content, 'text'):
                    response_text += message.content.text

        return response_text


# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    # Model selection
    model_option = st.selectbox(
        "Select Model",
        ["sonnet", "opus", "haiku"],
        index=0
    )
    st.session_state.model = model_option

    st.divider()

    st.subheader("📋 Available Subagents")
    st.markdown("""
    - **youtube-analyst**: Analyzes YouTube channel performance
    - **researcher**: Performs deep research and generates reports
    - **documentation-writer**: Creates technical documentation
    - **events_agent**: Gathers upcoming AI events in the Bay Area
    """)

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Claude Agent SDK")


# Main chat interface
st.title("🤖 Kaya - Your Personal Assistant")
st.caption(f"Using model: {st.session_state.model}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What can I help you with today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Get response from Claude
                response = asyncio.run(process_message(prompt, st.session_state.model))

                # Display response
                st.markdown(response)

                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
