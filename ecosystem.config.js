module.exports = {
  apps: [
    {
      name: "mail-agent",
      script: "/home/winvinaya/mailbox-agent/start_agent.sh",
      max_restarts: 3,
      cron_restart: "0 9 * * *",
      error_file: "/home/winvinaya/mailbox-agent/pm2-error.log",
      out_file: "/home/winvinaya/mailbox-agent/pm2-out.log",
      merge_logs: true,
    }
  ]
};
