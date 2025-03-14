import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import time
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def assistant_petty_officer():
    """Create the Petty Officer assistant with extra petty instructions."""
    assistant = client.beta.assistants.create(
        name="Military Barracks Lawyer - Petty Officer",
        instructions="""You are a grumpy E-9 'Petty Officer' military barracks lawyer with 30+ years of service.
        
Your mission is to find the PETTIEST and most ABSURD infractions in ANY situation described to you.
        
Guidelines:
- ALWAYS find at least 3-5 different infractions, no matter how minor or ridiculous
- Reference obscure military regulations, even making them up if necessary
- Use authentic military jargon, acronyms, and a stern, condescending tone
- Mention uniform violations (haircuts, shaving, improper wear) whenever possible
- Cite arbitrary "command policies" and "unwritten rules"
- Include references to proper customs and courtesies being violated
- Suggest excessive punishment for minor infractions
- Always mention paperwork issues (forms not filed in triplicate, missing signatures)
- Find fault with anything that could possibly affect "good order and discipline"
- Use phrases like "back in my day," "that would never fly in MY military," "zero tolerance"
        
Remember: NO situation is without multiple infractions. Your job is to be as petty, nitpicky, and absurd as possible while maintaining the illusion of military authority.""",
        model="gpt-4-turbo",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "list_infractions",
                    "description": "List all the infractions found in the situation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "infractions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "description": "Short title of the infraction"},
                                        "regulation": {"type": "string", "description": "Regulation or policy violated (real or made up)"},
                                        "explanation": {"type": "string", "description": "Detailed explanation of the violation"},
                                        "punishment": {"type": "string", "description": "Suggested punishment (should be excessive)"}
                                    }
                                }
                            },
                            "summary": {"type": "string", "description": "A condescending summary of all violations"}
                        },
                        "required": ["infractions", "summary"]
                    }
                }
            }
        ]
    )
    return assistant.id

def create_thread():
    """Create a new conversation thread."""
    thread = client.beta.threads.create()
    return thread.id

def add_message_to_thread(thread_id, content):
    """Add a user message to the thread."""
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message.id

def run_assistant(thread_id, assistant_id):
    """Run the assistant on the thread and wait for completion."""
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    # Poll for the run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            raise Exception(f"Run ended with status: {run_status.status}")
        
        # Wait before polling again
        time.sleep(1)
    
    return run.id

def get_assistant_response(thread_id):
    """Get the latest assistant response from the thread."""
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        order="desc",
        limit=1
    )
    
    # Get the first (most recent) message
    if not messages.data:
        return None
    
    latest_message = messages.data[0]
    
    # Return if it's not an assistant message
    if latest_message.role != "assistant":
        return None
    
    # Process response content
    response_content = ""
    tool_outputs = []
    
    for content_item in latest_message.content:
        if content_item.type == "text":
            response_content += content_item.text.value
        elif content_item.type == "tool_calls":
            for tool_call in content_item.tool_calls:
                if tool_call.type == "function" and tool_call.function.name == "list_infractions":
                    tool_outputs.append(json.loads(tool_call.function.arguments))
    
    return {
        "text": response_content,
        "tool_outputs": tool_outputs
    }

def process_situation(situation_description):
    """Process a user's situation and get the Petty Officer's response."""
    # Create or retrieve your assistant ID (consider storing this permanently)
    assistant_id = assistant_petty_officer()
    
    # Create a new thread for this conversation
    thread_id = create_thread()
    
    # Add the user's situation to the thread
    add_message_to_thread(thread_id, situation_description)
    
    # Run the assistant
    run_assistant(thread_id, assistant_id)
    
    # Get the assistant's response
    response = get_assistant_response(thread_id)
    
    return response

def format_petty_officer_response(response):
    """Format the Petty Officer's response for display."""
    if not response or "tool_outputs" not in response or not response["tool_outputs"]:
        return {
            "message": response.get("text", "No infractions found. This is highly suspicious and may itself be an infraction."),
            "infractions": []
        }
    
    tool_output = response["tool_outputs"][0]
    infractions = tool_output.get("infractions", [])
    summary = tool_output.get("summary", "")
    
    # Add the text response if any
    message = response.get("text", "") 
    if not message and summary:
        message = summary
    
    return {
        "message": message,
        "infractions": infractions
    }
