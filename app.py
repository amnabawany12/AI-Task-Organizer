
import os
import streamlit as st
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

# Load API key from .env
load_dotenv()

# Page settings
st.set_page_config(
    page_title="AI Task Organizer",
    page_icon="📝",
    layout="centered"
)

# Load custom CSS design
if os.path.exists("style.css"):
    with open("style.css", "r", encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )

# Create the Groq AI model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)


# Information shared between workflow nodes
class TaskState(TypedDict):
    user_input: str
    extracted_tasks: str
    prioritized_tasks: str
    final_result: str


# Node 1: Extract tasks
def extract_tasks(state: TaskState):
    prompt = f"""
    You are a task extraction assistant.
    Extract every individual task from the message.
    Keep deadlines mentioned by the user.
    Do not invent deadlines.
    Return a numbered list.

    User message: {state['user_input']}
    """

    response = llm.invoke(prompt)

    return {"extracted_tasks": response.content}


# Node 2: Assign priorities
def prioritize_tasks(state: TaskState):
    prompt = f"""
    You are a task prioritization assistant.
    Assign each task High, Medium, or Low priority.
    Consider urgency and deadlines.
    Keep the task names and deadlines.
    Do not invent deadlines.
    Briefly explain each priority.

    Tasks:
    {state['extracted_tasks']}
    """

    response = llm.invoke(prompt)

    return {"prioritized_tasks": response.content}


# Node 3: Format results
def format_results(state: TaskState):
    result = "## Your Organized To-Do List\n\n"
    result += state["prioritized_tasks"]

    return {"final_result": result}


# Build the LangGraph workflow
workflow = StateGraph(TaskState)

workflow.add_node("extract", extract_tasks)
workflow.add_node("prioritize", prioritize_tasks)
workflow.add_node("format", format_results)

workflow.set_entry_point("extract")
workflow.add_edge("extract", "prioritize")
workflow.add_edge("prioritize", "format")
workflow.add_edge("format", END)

app = workflow.compile()


# User interface
st.title("📝 AI Task Organizer")

st.write(
    "Turn your everyday messages into an organized "
    "to-do list with AI."
)

st.caption("Powered by Groq AI and LangGraph")

user_input = st.text_area(
    "What do you need to do?",
    placeholder=(
        "Example: Finish my assignment tomorrow, "
        "buy groceries today, and prepare for my "
        "meeting next week."
    ),
    height=130
)

if st.button("✨ Organize My Tasks", use_container_width=True):

    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "API key not found. Please check your .env file."
        )

    elif not user_input.strip():
        st.warning("Please enter your tasks first.")

    else:
        try:
            with st.spinner("AI is organizing your tasks..."):

                result = app.invoke({
                    "user_input": user_input,
                    "extracted_tasks": "",
                    "prioritized_tasks": "",
                    "final_result": ""
                })

            st.success("Your tasks have been organized!")
            st.markdown(result["final_result"])

        except Exception as e:
            st.error(f"Something went wrong: {e}")
