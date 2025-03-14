import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import time
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
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

Format your response like this:
1. **Tardy to Formation** - **Regulation:** MEO-23.7 - **Explanation:** [explanation] - **Punishment:** [punishment]
2. **Vehicle Readiness Violation** - **Regulation:** PRP-12.9A - **Explanation:** [explanation] - **Punishment:** [punishment]
3. [and so on for each infraction]

Then end with a condescending summary paragraph.
        
Remember: NO situation is without multiple infractions. Your job is to be as petty, nitpicky, and absurd as possible while maintaining the illusion of military authority.""",
        model="gpt-4o-mini",  # Using the more affordable model
        # Remove the tools section entirely
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
    try:
        print(f"Starting assistant run with thread_id={thread_id}, assistant_id={assistant_id}")
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        print(f"Run created with id: {run.id}")
        
        # Poll for the run to complete
        attempt = 0
        while True:
            attempt += 1
            try:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                
                print(f"Run status (attempt {attempt}): {run_status.status}")
                
                if run_status.status == "completed":
                    print("Run completed successfully")
                    break
                elif run_status.status == "requires_action":
                    print("Run requires action - handling tool calls")
                    
                    # Get the required actions
                    required_actions = run_status.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []
                    
                    # Process each tool call
                    for tool_call in required_actions:
                        print(f"Processing tool call: {tool_call.function.name}")
                        
                        # Handle the list_infractions function
                        if tool_call.function.name == "list_infractions":
                            # The assistant will generate this itself, we don't need to provide real data
                            # We're just submitting an empty response to let it continue
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": "{\"infractions\": [], \"summary\": \"\"}"
                            })
                    
                    # Submit the tool outputs
                    print(f"Submitting tool outputs: {tool_outputs}")
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    error_details = getattr(run_status, 'last_error', 'No detailed error information')
                    print(f"Run failed with status: {run_status.status}")
                    print(f"Error details: {error_details}")
                    
                    raise Exception(f"Run ended with status: {run_status.status}. Details: {error_details}")
            except Exception as poll_error:
                print(f"Error polling run status: {str(poll_error)}")
                if attempt > 30:  # Increased max attempts
                    raise
            
            # Wait before polling again
            time.sleep(2)
        
        return run.id
    except Exception as e:
        print(f"Error in run_assistant: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

def get_assistant_response(thread_id):
    """Get the latest assistant response from the thread."""
    try:
        print(f"Getting assistant response for thread_id={thread_id}")
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            limit=1
        )
        
        # Get the first (most recent) message
        if not messages.data:
            print("No messages found in thread")
            return None
        
        latest_message = messages.data[0]
        print(f"Latest message has id={latest_message.id}, role={latest_message.role}")
        
        # Return if it's not an assistant message
        if latest_message.role != "assistant":
            print(f"Latest message is not from assistant, but from {latest_message.role}")
            return None
        
        # Process response content
        response_content = ""
        tool_outputs = []
        
        print(f"Message content type: {[item.type for item in latest_message.content]}")
        
        for content_item in latest_message.content:
            if content_item.type == "text":
                response_content += content_item.text.value
                print(f"Text content: {content_item.text.value[:50]}...")
            elif content_item.type == "tool_calls":
                for tool_call in content_item.tool_calls:
                    if tool_call.type == "function" and tool_call.function.name == "list_infractions":
                        try:
                            tool_output = json.loads(tool_call.function.arguments)
                            tool_outputs.append(tool_output)
                            print(f"Tool output: {str(tool_output)[:50]}...")
                        except json.JSONDecodeError as json_error:
                            print(f"Error parsing tool output JSON: {str(json_error)}")
                            print(f"Raw arguments: {tool_call.function.arguments}")
        
        return {
            "text": response_content,
            "tool_outputs": tool_outputs
        }
    except Exception as e:
        print(f"Error in get_assistant_response: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

def process_situation(situation_description):
    """Process a user's situation and get the Petty Officer's response."""
    try:
        print(f"Processing situation: {situation_description[:50]}...")
        
        # Create or retrieve your assistant ID
        assistant_id = assistant_petty_officer()
        print(f"Created/retrieved assistant with ID: {assistant_id}")
        
        # Create a new thread for this conversation
        thread_id = create_thread()
        print(f"Created thread with ID: {thread_id}")
        
        # Add the user's situation to the thread
        add_message_to_thread(thread_id, situation_description)
        print(f"Added message to thread")
        
        # Run the assistant (simplified - no function calling)
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        print(f"Created run with ID: {run.id}")
        
        # Poll for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            print(f"Run status: {run_status.status}")
            
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                raise Exception(f"Run ended with status: {run_status.status}")
            
            time.sleep(2)
        
        # Get the response
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            limit=1
        )
        
        if not messages.data:
            return "No response received."
        
        response_text = ""
        for content in messages.data[0].content:
            if content.type == "text":
                response_text += content.text.value
        
        return response_text
            
    except Exception as e:
        print(f"Error in process_situation: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

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
