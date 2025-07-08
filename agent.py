import ollama
from agno.agent import Agent
from check_storage import get_mailbox_storage_percent, get_email_metadata
from notify import send_warning_mail
from db import get_user_credentials
import asyncio

model = "deepseek-r1:8b"  # Replace if using a different Ollama model

class MailboxMonitorAgent(Agent):
    def __init__(self):
        super().__init__(name="MailboxMonitor")

    def run(self):
        users = get_user_credentials()

        for email, password in users:
            try:
                percent = get_mailbox_storage_percent(email, password)
                print(f"{email} is at {percent:.2f}%")

                if percent >= 82:
                    # Generate AI suggestion
                    suggestion, thinking_data = self.generate_ai_suggestion(email, percent, password)

                    # Send high alert mail with AI suggestion and thinking data
                    asyncio.run(send_warning_mail(email, percent, level="high", suggestion=suggestion, thinking_data=thinking_data))
                    print(f"📧 High alert sent to {email} with AI suggestion.")

                elif percent >= 70:
                    # Send caution mail without AI
                    asyncio.run(send_warning_mail(email, percent, level="caution"))
                    print(f"📧 Caution alert sent to {email}.")

                else:
                    print(f"✅ {email} is under threshold. No alert sent.")

            except Exception as e:
                print(f"❌ Error checking {email}: {e}")

    def generate_ai_suggestion(self, email, percent, password):
        try:
            # Ensure percent is a string before passing it into AI prompt (to avoid float issue)
            percent_str = str(percent)  # Convert percent to string to avoid float-related issues

            metadata = get_email_metadata(email, password)  # Ideally pass securely

            folder_summary = ""
            for folder, items in metadata.items():
                folder_summary += f"\n📂 {folder}:\n"
                for item in items:
                    folder_summary += f"- From: {item['from']} | Subject: {item['subject']}\n"

            prompt = (
                f"The mailbox {email} is using {percent_str}% of 500MB storage.\n"
                f"Below is a list of recent emails from all folders:\n{folder_summary}\n\n"
                "Based on this metadata, identify which email addresses are sending promotional, subscription, or unnecessary emails that can be deleted.\n"
                "Respond with a plain list of email addresses and types of emails to delete. No XML, no tags. Example:\n"
                "- news@shopping.com – Promotional\n- updates@social.com – Social Notifications\n"
            )

            response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

            # Capture the thinking data
            thinking_data = response.get('message', {}).get('content', '').split('<think>')[-1] if '<think>' in response.get('message', {}).get('content', '') else ''
            suggestion = str(response['message']['content']).strip()  # Convert to string to prevent float-related errors

            # Add additional handling for floating-point values if needed
            # Ensure everything is properly formatted and strings are clean
            suggestion = suggestion.replace("\n", "<br>")  # Example replace to ensure formatting in email
            thinking_data = thinking_data.replace("\n", "<br>")  # Format thinking data too

            return suggestion, thinking_data

        except Exception as e:
            print(f"❌ AI suggestion failed for {email}: {e}")
            return None, None
