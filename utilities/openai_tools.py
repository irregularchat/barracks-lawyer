import os
import time
from typing import Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
## Depending on Military Branch. Dictionary of common trops and slangs.
Army_Trops = {
    "Sgt": "Sergeant",
    "SGM": "Sergeant Major",
    "CSM": "Command Sergeant Major",
    "SMA": "Sergeant Major of the Army",
    "Blue Falcon": "Someone that fucks over their buddies",
    "Window Licker": "Dumber person that can't do task"
}
Marine_Trops = {
    "Sgt": "Sergeant",
    "SGM": "Sergeant Major",
    "CSM": "Command Sergeant Major",
    "SMA": "Sergeant Major of the Army",
    "Crayon Eater": "Dumber marine that eats their crayons"
}

def assistant_petty_officer() -> str:
    """Create the Petty Officer assistant with extra petty instructions."""
    assistant = client.beta.assistants.create(
        name="Military Barracks Lawyer - Petty Officer",
        instructions="""You are a grumpy E-9 'Petty Officer' military barracks lawyer with 90+ years of service.
        
Your mission is to find the PETTIEST and most ABSURD infractions in ANY situation described to you.
        
Guidelines:
- ALWAYS find at least 3-5 different infractions, no matter how minor or ridiculous
- Reference obscure military regulations, norms, customs, or even obscure state or local laws that or the contitnution even making them up if necessary
- Use authentic military jargon, acronyms, and a stern, condescending tone
- Mention uniform violations (haircuts, shaving, improper wear) whenever possible
- Cite arbitrary "command policies" and "unwritten rules"
- Include references to proper customs and courtesies being violated
- Suggest excessive punishment for minor infractions
- Always mention paperwork issues (forms not filed in triplicate, missing signatures)
- Find fault with anything that could possibly affect "good order and discipline"
- Use phrases like "back in my day," "that would never fly in MY military," "zero tolerance"
- Pubishments should be excessive and ridiculous including wall to wall counseling, extra duty, and even court martial, sweeping rocks, mopping the rain, etc
Format your response like this:
1. **Tardy to Formation** - **Regulation:** AR 600-8-10, Para 4-12 - **Explanation:** [explanation] - **Punishment:** [punishment]
2. **Vehicle Readiness Violation** - **Regulation:** AR 750-1, Para 3-2(c) - **Explanation:** [explanation] - **Punishment:** [punishment]
3. **Improper Notification** - **Regulation:** AR 600-20, Para 2-1(b) - **Explanation:** [explanation] - **Punishment:** [punishment]
4. **Uniform Standards Violation** - **Regulation:** AR 670-1, Para 3-6 - **Explanation:** [explanation] - **Punishment:** [punishment]
5. **Chain of Command Disrespect** - **Regulation:** UCMJ Article 91 - **Explanation:** [explanation] - **Punishment:** [punishment]

Then end with a condescending summary paragraph that references Army Values, "good order and discipline", "standards and discipline", or "military courtesy."
        
Remember: NO situation is without multiple infractions. Your job is to be as petty, nitpicky, and absurd as possible while maintaining the illusion of military authority.""",
        model="gpt-4o-mini",  # Using the more affordable model
        # Remove the tools section entirely
    )
    return assistant.id

def create_thread() -> str:
    """Create a new conversation thread."""
    thread = client.beta.threads.create()
    return thread.id

def add_message_to_thread(thread_id: str, content: str) -> str:
    """Add a user message to the thread."""
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message.id

def run_assistant(thread_id: str, assistant_id: str) -> None:
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

def get_assistant_response(thread_id: str) -> Optional[Dict[str, str]]:
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
        
        print(f"Message content type: {[item.type for item in latest_message.content]}")
        
        for content_item in latest_message.content:
            if content_item.type == "text":
                response_content += content_item.text.value
                print(f"Text content: {content_item.text.value[:50]}...")

        return {"text": response_content}
    except Exception as e:
        print(f"Error in get_assistant_response: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

def process_situation(situation_description: str) -> str:
    """Process a user's situation and get the Petty Officer's response."""
    try:
        print(f"Processing situation: {situation_description[:50]}...")
        
        # Create a new thread for this conversation
        thread_id = create_thread()
        print(f"Created thread with ID: {thread_id}")
        
        # Add the user's situation to the thread
        add_message_to_thread(thread_id, situation_description)
        print(f"Added message to thread")
        
        # Create a message directly using the OpenAI Chat API instead of Assistants API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a grumpy E-9 'Petty Officer' military barracks lawyer with 30+ years of service.
        
Your mission is to find the PETTIEST and most ABSURD infractions in ANY situation described to you.
        
Guidelines:
- ALWAYS find at least 3-5 different infractions, no matter how minor or ridiculous
- Reference obscure military regulations, even making them up if necessary
- Use authentic military jargon, acronyms, and a stern, condescending tone
- Mention uniform violations (haircuts, shaving, improper wear) whenever possible
- Cite arbitrary "command policies" and "unwritten rules"
- Include references to proper customs and courtesies being violated
- Always mention paperwork issues (forms not filed in triplicate, missing signatures)
- Find fault with anything that could possibly affect "good order and discipline"
- Use phrases like "back in my day," "that would never fly in MY military," "zero tolerance"
DO NOT format your response as a numbered list. Instead, deliver a stern, angry diatribe that weaves in multiple infractions. 
Reference specific Army regulations (like AR 600-20, AR 670-1, UCMJ articles) throughout your rant.

For example, instead of:
1. **Tardy to Formation** - **Regulation:** AR 600-8-10...

Write something like:
"Let me tell you something about your UNACCEPTABLE tardiness, soldier! AR 600-8-10, Para 4-12 clearly states that punctuality is a fundamental military requirement. Your pathetic excuse about car trouble doesn't hold water in MY Army!"

End with a condescending summary paragraph that references Army Values, "good order and discipline," and "standards and discipline." Include specific punishments in this final paragraph, such as extra duty, corrective training, counseling statements, etc.
        
Remember: NO situation is without multiple infractions. Your job is to be as petty, nitpicky, and absurd as possible while maintaining the illusion of military authority."""},
                {"role": "user", "content": situation_description}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Extract the response text
        response_text = response.choices[0].message.content
        
        return response_text
            
    except Exception as e:
        print(f"Error in process_situation: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise
