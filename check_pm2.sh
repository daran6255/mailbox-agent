#!/bin/bash
echo "[DEBUG] Running PM2 check..." >> /home/winvinaya/mailbox-agent/check_pm2.log
date >> /home/winvinaya/mailbox-agent/check_pm2.log

if ! pm2 list | grep -q "mail-agent"; then
    echo "[DEBUG] mail-agent not running, restarting..." >> /home/winvinaya/mailbox-agent/check_pm2.log
    pm2 start /home/winvinaya/mailbox-agent/start_agent.sh --name mail-agent
    echo "[DEBUG] Sending alert email..." >> /home/winvinaya/mailbox-agent/check_pm2.log

    python3 /home/winvinaya/mailbox-agent/send_error_mail.py "mail-agent was not running and was restarted"
else
    echo "[DEBUG] mail-agent is running." >> /home/winvinaya/mailbox-agent/check_pm2.log
fi
