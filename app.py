import gradio as gr
import os
from utilities.openai_tools import process_situation
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")

def petty_officer_analysis(situation):
    """Process the user's situation through the Petty Officer assistant."""
    if not situation.strip():
        return "You can't fool me with blank reports, soldier! DESCRIBE YOUR SITUATION!"
    
    try:
        # Process the situation - now returns plain text
        response_text = process_situation(situation)
        
        # Format the HTML output - ONLY include the assessment section
        output = f"""
        <div style="font-family: Arial, sans-serif;">
            <h3 style="color: #8B0000; border-bottom: 1px solid #ccc; padding-bottom: 8px;">PETTY OFFICER'S ASSESSMENT:</h3>
            <div style="white-space: pre-wrap; padding: 15px; border: 1px solid #d00; background-color: #fff0f0; border-radius: 5px;">
                {response_text}
            </div>
        </div>
        """
        
        return output
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in petty_officer_analysis: {str(e)}")
        print(f"Traceback: {error_trace}")
        return f"""<div style='color: red; padding: 10px; border: 1px solid red;'>
            <h3>ERROR: The Petty Officer is currently busy yelling at someone else.</h3>
            <p>Technical details: {str(e)}</p>
            </div>"""

# Create the Gradio interface
with gr.Blocks(title="Military Barracks Lawyer", theme=gr.themes.Default(), css="""
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
        background-color: #f5f5f5;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .logo-image {
        max-height: 120px;
        object-fit: contain;
        border-radius: 5px;
    }
""") as app:
    with gr.Row():
        with gr.Column(scale=1):
            # Use gr.Image with proper parameters
            gr.Image(
                value="static/logo.png",  # Path to your logo
                show_label=False,         # Hide the label
                container=False,          # Remove container styling
                height=120,               # Set fixed height
                width=120,                # Set fixed width
                interactive=False         # Make it non-interactive (display only)
            )
        
        with gr.Column(scale=3):
            gr.Markdown(
                """
                # 🎖️ Military Barracks Lawyer - Petty Officer 🎖️
                
                *Tell me about your situation, and I'll find ALL the regulations you're violating.*
                
                This grumpy E-9 has 90+ years of service and can find an infraction in ANYTHING.
                """
            )
    
    with gr.Row():
        with gr.Column():
            situation_input = gr.Textbox(
                label="Describe Your Situation",
                placeholder="I was 5 minutes late to formation because my car wouldn't start...",
                lines=5
            )
            submit_button = gr.Button("Submit For Inspection", variant="primary")
        
        with gr.Column():
            output_html = gr.HTML(label="Petty Officer's Response")
    
    # Example situations to try
    gr.Examples(
        [
            ["I was 5 minutes late to formation because my car wouldn't start."],
            ["I finished all work assigned early, so I went to the gym."],
            ["I wore white socks instead of black socks with my uniform today."],
            ["I took a 35-minute lunch break instead of the allowed 30 minutes."],
            ["My roommate played music after lights out."]
        ],
        inputs=situation_input,
        outputs=output_html,
        fn=petty_officer_analysis,
        cache_examples=False
    )
    
    # Set up the event handlers
    submit_button.click(
        fn=petty_officer_analysis,
        inputs=situation_input,
        outputs=output_html
    )
    
    gr.Markdown(
        """
        ### Disclaimer:
        
        This app is for entertainment purposes only. All regulations cited may be completely made up. 
        No actual military advice is being provided. Use at your own risk, private!
        """
    )

# Launch the app
if __name__ == "__main__":
    app.launch() 