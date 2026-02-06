# import asyncio
# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
# from google.genai import types

# from weather_support.agent import root_agent
# import uuid

# import shutup
# shutup.please()

# APP_NAME = "weather_app"
# USER_ID = "default_user"
# SESSION_ID = str(uuid.uuid4())  # Generate a unique session ID for each run
# # Session and Runner
# session_service = InMemorySessionService()
# session = asyncio.run(session_service.create_session(
#     app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
# ))
# runner = Runner(agent=root_agent, app_name=APP_NAME,
#                 session_service=session_service)

# # Agent Interaction (Async)
# async def call_agent_async(query):
#     content = types.Content(role="user", parts=[types.Part(text=query)])
#     print(f"\n--- Running Query: {query} ---")
#     final_response_text = "No final text response captured."
#     try:
#         # Use run_async
#         async for event in runner.run_async(
#             user_id=USER_ID, session_id=SESSION_ID, new_message=content
#         ):
#             print(f"Event ID: {event.id}, Author: {event.author}")

#             # --- Check for specific parts FIRST ---
#             has_specific_part = False
#             if event.content and event.content.parts:
#                 for part in event.content.parts:  # Iterate through all parts
#                     if part.executable_code:
#                         # Access the actual code string via .code
#                         # print(
#                         #     f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```"
#                         # )
#                         has_specific_part = True
#                     elif part.code_execution_result:
#                         # Access outcome and output correctly
#                         # print(
#                         #     f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}"
#                         # )
#                         has_specific_part = True
#                     # Also print any text parts found in any event for debugging
#                     # elif part.text and not part.text.isspace():
#                     #     print(f"  Text: '{part.text.strip()}'")
#                         # Do not set has_specific_part=True here, as we want the final response logic below

#             # --- Check for final response AFTER specific parts ---
#             # Only consider it final if it doesn't have the specific code parts we just handled
#             if not has_specific_part and event.is_final_response():
#                 if (
#                     event.content
#                     and event.content.parts
#                     and event.content.parts[0].text
#                 ):
#                     final_response_text = event.content.parts[0].text.strip()
#                     print(f"==> Final Agent Response: {final_response_text}")
#                 else:
#                     print(
#                         "==> Final Agent Response: [No text content in final event]")

#     except Exception as e:
#         print(f"ERROR during agent run: {e}")
#     print("-" * 30)


# # Main async function to run the examples
# async def main(user_query="What is the current weather in New York?"):
#     await call_agent_async(user_query)


# # Execute the main async function
# while True:
#     try:
#         user_query = input("\nEnter your weather query (or 'exit' to quit): ")
#         if user_query.lower() == "exit":
#             print("Exiting the Weather App. Goodbye!")
#             break
#         asyncio.run(main(user_query))
#     except KeyboardInterrupt:
#         print("\nExiting the Weather App. Goodbye!")
#         break
import asyncio
import uuid
import datetime
import time
import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from weather_support.agent import root_agent

# -----------------------------------------------------------------------------
# Streamlit App Setup
st.set_page_config(page_title="Weather Chatbot", page_icon="☁️")

# -----------------------------------------------------------------------------
# Constants and Initialization
APP_NAME = "weather_app"
USER_ID = "default_user"

# Initialize session state variables
if "SESSION_ID" not in st.session_state:
    st.session_state.SESSION_ID = str(uuid.uuid4())  # Generate a unique session ID
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores the conversation history
if "prev_question_timestamp" not in st.session_state:
    st.session_state.prev_question_timestamp = datetime.datetime.fromtimestamp(0)
if "session" not in st.session_state:
    # Create the session only once and store it in session_state
    session_service = InMemorySessionService()
    st.session_state.session = asyncio.run(session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=st.session_state.SESSION_ID
    ))
    st.session_state.runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    print(f"Session created: {st.session_state.session}")

# -----------------------------------------------------------------------------
# Helper Functions
async def call_agent_async():
    """
    Calls the agent asynchronously with the entire conversation history and returns the final response.
    """
    # Build the conversation history
    conversation = []
    for message in st.session_state.messages:
        conversation.append(
            types.Content(
                role=message["role"],
                parts=[types.Part(text=message["content"])]
            )
        )

    # Use the last user message as the new query
    user_message = conversation[-1]

    print(f"Session ID: {st.session_state.SESSION_ID} - Calling agent with query: '{user_message.parts[0].text}'")

    final_response_text = "No final text response captured."
    try:
        # Use run_async
        async for event in st.session_state.runner.run_async(
            user_id=USER_ID,
            session_id=st.session_state.SESSION_ID,
            new_message=user_message,
        ):
            if event.is_final_response():
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    final_response_text = event.content.parts[0].text.strip()
    except Exception as e:
        final_response_text = f"ERROR: {e}"
    return final_response_text

def reset_chat():
    """
    Resets the chat history and session state.
    """
    st.session_state.messages = []
    st.session_state.prev_question_timestamp = datetime.datetime.fromtimestamp(0)
    st.session_state.SESSION_ID = str(uuid.uuid4())  # Generate a new session ID
    session_service = InMemorySessionService()
    st.session_state.session = asyncio.run(session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=st.session_state.SESSION_ID
    ))
    st.session_state.runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    print(f"Session reset: {st.session_state.session}")

# -----------------------------------------------------------------------------
# Streamlit Chat Interface
# Title and Instructions
st.title("☁️ Weather Chatbot")
st.write("Ask me about the weather in any city or place!")

# Chat Input
user_message = st.chat_input("Ask about the weather...")

# Restart Button
if st.button("Restart Chat"):
    reset_chat()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if user_message:
    # Add user message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Call the agent and display the response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Rate-limit the input if needed
            question_timestamp = datetime.datetime.now()
            time_diff = question_timestamp - st.session_state.prev_question_timestamp
            st.session_state.prev_question_timestamp = question_timestamp

            if time_diff < datetime.timedelta(seconds=3):
                time.sleep(time_diff.seconds + time_diff.microseconds * 0.001)

            # Call the agent with the conversation history
            response = asyncio.run(call_agent_async())

        # Display the assistant's response
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})