import imaplib
import email
from email.header import decode_header
import os

# Your email credentials
EMAIL = "bm9711111111@gmail.com"
PASSWORD = "mekueihigncngwqt"  # Use the app password if 2-step verification is enabled
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Connect to the Gmail server using IMAP
def connect_to_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    return mail

# Download emails and save them as .eml files
def download_emails():
    mail = connect_to_gmail()
    mail.select("inbox")  # Select the mailbox you want to download from

    # Search for all emails in the inbox
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("Failed to fetch email IDs.")
        return

    # Convert the result to a list of email IDs
    email_ids = messages[0].split()

    # Create a directory to save emails
    if not os.path.exists("emails"):
        os.makedirs("emails")

    # Loop through each email ID and fetch its content
    for i, email_id in enumerate(email_ids):
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            print(f"Failed to fetch email with ID: {email_id}")
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                # Decode sender's email
                from_ = msg.get("From")
                if isinstance(from_, bytes):
                    from_ = from_.decode(encoding or "utf-8")

                # Print email info
                print(f"Downloading email {i + 1}: {subject} from {from_}")

                # Save email as .eml file
                filename = f"emails/email_{i + 1}.eml"
                with open(filename, "wb") as f:
                    f.write(response_part[1])

    # Logout
    mail.logout()

# Run the script to download emails
if __name__ == "__main__":
    download_emails()
