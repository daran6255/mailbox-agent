from agent import MailboxMonitorAgent
from notify import send_warning_mail
import traceback
import asyncio

if __name__ == "__main__":
    try:
        agent = MailboxMonitorAgent()
        agent.run()
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        # Send email alert
        asyncio.run(send_warning_mail(
            to_email="info@winvinaya.com",
            usage_percent=0,
            level="high",
            suggestion=f"Critical error:\n{error_message}",
            thinking_data=""
        ))
        exit(1)
