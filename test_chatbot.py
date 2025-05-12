import requests
import json
import uuid
import os

# Configuration
API_URL = "http://localhost:8080/api/chat"  # Update with your actual server URL
USER_ID = str(uuid.uuid4())  # Generate a random user ID or replace with a fixed one for testing
DOCUMENT_TYPE = "seller_disclosure"  # Default document type

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_message(message_text, doc_type=None):
    """Send a message to the chat API and return the response"""
    payload = {
        "messages": [{"role": "user", "content": message_text}],
        "user_id": USER_ID,
        "document_type": doc_type or DOCUMENT_TYPE
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"response": "Error connecting to the server", "pdf_generated": False}

def select_document_type():
    """Let user select document type"""
    print("\nSelect document type:")
    print("1. Seller Disclosure")
    print("2. Lead Based Paint Disclosure")
    print("3. CIS Form")
    print("4. Coming Soon Listing Form")
    
    while True:
        choice = input("Enter choice (1-4): ")
        if choice == '1':
            return "seller_disclosure"
        elif choice == '2':
            return "lead_based_paint_disclosure"
        elif choice == '3':
            return "cis_form"
        elif choice == '4':
            return "coming_soon_listing"
        else:
            print("Invalid choice, please try again.")

def display_chat_interface():
    """Display the chat interface and handle user interactions"""
    clear_screen()
    print("=" * 80)
    print(" PDF Form Chat Bot ".center(80, "="))
    print("=" * 80)
    
    # Let user select document type
    selected_doc_type = select_document_type()
    
    # Update page title based on document type
    if selected_doc_type == "seller_disclosure":
        title = "Seller Disclosure Form Chat Bot"
    else:
        title = "Lead Based Paint Disclosure Chat Bot"
    
    clear_screen()
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)
    print(" Type 'exit' to quit or 'pdf' to generate the PDF ".center(80, "-"))
    print()
    
    chat_history = []
    
    # Send initial message to set document type on server
    init_response = send_message("Hi, I'd like to start filling out a form.", selected_doc_type)
    if "response" in init_response:
        print(f"\nAssistant: {init_response['response']}")
        chat_history.append({"role": "assistant", "content": init_response["response"]})
        print("\n" + "-" * 80)
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            break
            
        # Send the message to the API
        response = send_message(user_input, selected_doc_type)
        
        # Store the conversation
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response["response"]})
        
        # Display the response
        print(f"\nAssistant: {response['response']}")
        
        # Check if PDF was generated
        if response.get("pdf_generated", False):
            print(f"\n[PDF Generated] Available at: {response.get('pdf_url', 'Unknown URL')}")
            
        # Display a separator for readability
        print("\n" + "-" * 80)

if __name__ == "__main__":
    display_chat_interface()