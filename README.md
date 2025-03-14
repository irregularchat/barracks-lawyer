# Military Barracks Lawyer

Military Barracks Lawyer is a fun, interactive web app built with Python and Gradio. It helps users search through military regulations and policies while offering advice on whether certain actions are "worth it or not." Additionally, it assists by populating events and suggesting angles to argue that something might be in violation of existing rules.

## Features
### Offensive 
- **Offensive Lawyer "Petty Officer"**: Given a situation, the app will provide find or make up reasons that it is a violation of military regulations, policy, norms, or etiquette.

### Defensive
- **Defensive Lawyer "Chud Advocate"**: Given a situation, the app will provide find or make up reasons that it is not a violation of military regulations, policy, norms, or etiquette.
## Counsel
- **Regulation & Policy Search:** Quickly search and filter through military regulations and policy documents.
- **Worth It or Not Advice:** Get pre-action advice on whether an activity is advisable.


## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/military-barracks-lawyer.git
   cd military-barracks-lawyer

	2.	Create and Activate a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


	3.	Install Dependencies:

pip install -r requirements.txt

Note: Ensure you have Python 3.7 or higher installed.

Usage
	1.	Run the App:

python app.py


	2.	Open in Browser:
The app will launch a local Gradio interface. Open the provided URL in your browser to interact with the Military Barracks Lawyer.
	3.	How It Works:
	•	Search Regulations: Enter keywords to retrieve relevant military regulations and policies.
	•	Pre-Action Advice: Use the “Worth It or Not” function to get immediate feedback on whether an action is advisable.
	•	Incident Analysis: Fill out the details of an incident as prompted, and the app will analyze the situation to find potential policy breaches.

Configuration
	•	Settings: Customize search parameters, advice thresholds, and other options in the config.py file.
	•	Data Sources: The app leverages internal datasets of military regulations. For live updates or changes, refer to the documentation provided in the /docs folder.

Disclaimer

Military Barracks Lawyer is intended for fun and informational purposes only. It is not a substitute for professional legal advice. Always consult a qualified legal professional for any legal matters.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

License

This project is licensed under the MIT License. See the LICENSE file for details.

