import sys
import os
from utilities.openai_tools import process_situation, format_petty_officer_response

def main():
    print("=" * 50)
    print("MILITARY BARRACKS LAWYER - PETTY OFFICER TEST")
    print("=" * 50)
    print("Describe a situation and the Petty Officer will find all infractions.")
    print("Type 'quit' to exit.")
    print("=" * 50)
    
    while True:
        # Get user input
        print("\nDescribe your situation:")
        situation = input("> ")
        
        if situation.lower() in ['quit', 'exit', 'q']:
            print("Exiting. Remember to stay in regulation!")
            break
        
        print("\nProcessing... Stand at attention while I review your case!")
        
        try:
            # Process the situation
            response = process_situation(situation)
            
            # Format the response
            formatted_response = format_petty_officer_response(response)
            
            # Display the results
            print("\n" + "=" * 50)
            print("PETTY OFFICER'S ASSESSMENT:")
            print(formatted_response["message"])
            print("\nINFRACTIONS IDENTIFIED:")
            
            if formatted_response["infractions"]:
                for i, infraction in enumerate(formatted_response["infractions"], 1):
                    print(f"\n{i}. {infraction['title']}")
                    print(f"   Regulation: {infraction['regulation']}")
                    print(f"   Explanation: {infraction['explanation']}")
                    print(f"   Recommended Punishment: {infraction['punishment']}")
            else:
                print("No specific infractions listed, but you're probably still in trouble.")
                
            print("=" * 50)
            
        except Exception as e:
            print(f"Error processing your situation: {str(e)}")
            print("The Petty Officer is currently busy yelling at someone else. Try again later.")

if __name__ == "__main__":
    main() 