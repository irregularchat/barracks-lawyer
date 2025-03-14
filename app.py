import gradio as gr
import os
from utilities.openai_tools import process_situation, format_petty_officer_response, assistant_petty_officer
from dotenv import load_dotenv

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
        # Process the situation
        print(f"Processing situation: {situation[:50]}...")
        response = process_situation(situation)
        
        # Format the response
        print("Formatting response...")
        formatted_response = format_petty_officer_response(response)
        
        # Create a formatted output for Gradio
        message = formatted_response["message"]
        infractions = formatted_response["infractions"]
        print(f"Found {len(infractions)} infractions")
        
        output = f"<h3>PETTY OFFICER'S ASSESSMENT:</h3>\n<p>{message}</p>\n\n<h3>INFRACTIONS IDENTIFIED:</h3>\n"
        
        if infractions:
            for i, infraction in enumerate(infractions, 1):
                output += f"<div style='margin-bottom: 20px; padding: 10px; border: 1px solid #d00; background-color: #fff0f0;'>"
                output += f"<h4>{i}. {infraction['title']}</h4>"
                output += f"<p><strong>Regulation:</strong> {infraction['regulation']}</p>"
                output += f"<p><strong>Explanation:</strong> {infraction['explanation']}</p>"
                output += f"<p><strong>Recommended Punishment:</strong> {infraction['punishment']}</p>"
                output += "</div>"
        else:
            output += "<p>No specific infractions listed, but you're probably still in trouble.</p>"
            
        return output
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in petty_officer_analysis: {str(e)}")
        print(f"Traceback: {error_trace}")
        return f"""<div style='color: red; padding: 10px; border: 1px solid red;'>
            <h3>ERROR: The Petty Officer is currently busy yelling at someone else.</h3>
            <p>Technical details: {str(e)}</p>
            <pre style='background-color: #f8f8f8; padding: 10px; font-size: 12px; overflow: auto;'>{error_trace}</pre>
            </div>"""

# Create the Gradio interface
with gr.Blocks(title="Military Barracks Lawyer", theme=gr.themes.Default(), 
               css="#logo {padding: 10px; background-color: #f0f0f0; border-radius: 10px;}") as app:
    with gr.Row(elem_id="header"):
        with gr.Column(scale=1):
            gr.Image("static/logo.jpeg", elem_id="logo", show_label=False, 
                    container=False, height=100)
        with gr.Column(scale=3):
            gr.Markdown(
                """
                # 🎖️ Military Barracks Lawyer - Petty Officer 🎖️
                
                *Tell me about your situation, and I'll find ALL the regulations you're violating.*
                
                This grumpy E-9 has 30+ years of service and can find an infraction in ANYTHING.
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
            ["I forgot to salute an officer while I was carrying boxes to my barracks."],
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