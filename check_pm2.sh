#!/bin/bash

# Check if PM2 process exists
if ! pm2 list | grep -q "mail-agent"; then
    echo "mail-agent not running, attempting restart..."

    pm2 start /home/winvinaya/mailbox-agent/start_agent.sh --name mail-agent

    # Send email alert
    python3 /home/winvinaya/mailbox-agent/send_error_mail.py "mail-agent was not running and was restarted"
fi
