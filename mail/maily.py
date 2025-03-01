def create_email(sender, to, subject, message_text):
    """Create a message for an email.
    
    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        
    Returns:
        An object containing a base64url encoded email object.
    """
    import base64
    from email.mime.text import MIMEText
    
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    
    # Convert the message to a string, then to bytes, and finally to base64url encoding
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw_message}


def send_gmail( sender: str, to: str, subject: str, message_text: str ) -> dict:
    """Send an email using Gmail API with authentication handling.
    
    This function handles the entire process of authentication with Gmail API
    and sending an email message to the specified recipient.
    
    Args:
        sender: optional, Email address of the sender. Defaults to "marnewi.ey@gmail.com".
        to: optional, Email address of the receiver. Defaults to "marnewi.amine@gmail.com".
        subject: optional, The subject of the email message. Defaults to "Test Email from Gmail API".
        message_text: optional, The text content of the email message. Defaults to a test message.
        
    Returns:
        A dictionary containing the sent message details or error information returned to the user for confirmation.
    """
    import os.path
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    
    # Define constants

    # If modifying these scopes, delete the file token.json.
    # SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    SCOPES = ["https://mail.google.com/"]
    
    if sender == "":
        sender = "marnewi.ey@gmail.com"
    
    token_path = r"C:\Users\VM764NY\OneDrive - EY\Documents\Python Scripts\alfred\mail\token.json"
    cred_path = r"C:\Users\VM764NY\OneDrive - EY\Documents\Python Scripts\alfred\mail\credentials.json"
    
    # Authentication process
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    try:
        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)
        
        # Create and send email
        message = create_email(sender, to, subject, message_text)
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        
        print(f"Message sent successfully! Message ID: {sent_message['id']}")
        return {"status": "success", "message_id": sent_message['id'], "subject": subject, "message_sent": message_text}
        
    except HttpError as error:
        error_message = f"An error occurred: {str(error)}"
        print(error_message)
        return {"status": "error", "message": error_message}
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}

if __name__ == "__main__":
    send_gmail()