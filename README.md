
# AI Task Organizer

## Project Overview
The AI Task Organizer converts everyday messages into an organized to-do list. It uses Groq AI to extract tasks and assign priorities, while LangGraph manages the workflow.

## Features
- Extracts individual tasks from natural-language messages.
- Identifies deadlines mentioned by the user.
- Assigns High, Medium, or Low priorities.
- Displays an organized task list.
- Provides a simple Streamlit user interface.

## Technologies Used
- Python
- Streamlit
- LangGraph
- Groq API
- LangChain Groq
- Python-dotenv

## Workflow
1. User enters a message containing tasks.
2. Task Extraction identifies individual tasks.
3. Task Prioritization assigns priority levels.
4. Format Results creates the final to-do list.

## Installation and Setup

1. Install Python.
2. Clone or download this repository.
3. Install the required libraries:

   pip install -r requirements.txt

4. Create a `.env` file in the project folder.
5. Add your Groq API key:

   GROQ_API_KEY=your_groq_api_key_here

6. Start the application:

   streamlit run app.py

## Note
Keep your API key private. Do not upload your `.env` file to GitHub.
