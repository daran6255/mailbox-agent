#!/bin/bash

LOG_FILE="/home/winvinaya/mailbox-agent/pm2-error.log"

# Check PM2 process
if ! pm2 list | grep -q "mail-agent.*online"; then
    echo "mail-agent is NOT running!" | mail -s "PM2 ALERT: mail-agent DOWN" info@winvinaya.com
fi

# Check PM2 logs for new errors
if grep -qi "Traceback" "$LOG_FILE"; then
    echo "Error found in PM2 error log" | mail -s "PM2 ERROR in mail-agent" info@winvinaya.com
fi
