import asyncio
from notify import send_warning_mail

import sys

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Unknown error in PM2 check."

    asyncio.run(send_warning_mail(
        to_email="info@winvinaya.com",
        usage_percent=0,
        level="high",
        suggestion=message,
        thinking_data=""
    ))
