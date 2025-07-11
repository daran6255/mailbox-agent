mailbox_agent/
│
├── venv/
├── agent.py
├── check_storage.py
├── notify.py
├── db.py
├── main.py
├── seed_db.py
├── requirements.txt
└── .env

## Install Python 3 and virtualenv
sudo apt update
sudo apt install python3 python3-venv python3-pip

## Create a virtual environment
python3 -m venv venv
source venv/bin/activate

## Install requirements
pip install --upgrade pip
pip install -r requirements.txt

## Install and configure PostgreSQL
sudo apt install postgresql postgresql-contrib

## Log in as the postgres user:
sudo -u postgres psql

## Create your database and user:
CREATE DATABASE mailagent;
CREATE USER postgres WITH PASSWORD '12345';
GRANT ALL PRIVILEGES ON DATABASE mailagent TO postgres;
\q

## Run database seed
python seed_db.py

**You should see:** 
✅ Database setup complete with all users.

### Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

**Then start the Ollama service:** 
ollama serve

**Make sure it's working:** 
ollama list

### Pull the deepseek-r1:8b model
ollama pull deepseek-r1:8b

## Install Node.js & PM2
sudo apt update
sudo apt install nodejs npm

## Install PM2 globally:
sudo npm install pm2@latest -g

**Verify:**
pm2 --version

## Create a Startup Script
start_agent.sh

## Make it executable:
chmod +x start_agent.sh

## Start with PM2
<!-- pm2 start /home/winvinaya/mailagent/start_agent.sh --name mail-agent --cron "0 9 * * *"

pm2 start /home/winvinaya/mailbox-agent/start_agent.sh --name mail-agent --cron-restart "0 9 * * *" -->

pm2 start /home/winvinaya/mailbox-agent/start_agent.sh --name mail-agent --cron-restart "0 9 * * *"
pm2 save
pm2 startup

pm2 start ecosystem.config.js
pm2 save
pm2 startup

chmod +x /home/winvinaya/mailbox-agent/check_pm2.sh



*/10 * * * * /home/winvinaya/mailbox-agent/check_pm2.sh >> /home/winvinaya/mailbox-agent/check_pm2.log 2>&1


crontab -l

**Check status:**
pm2 list

You should see something like:
┌─────────────┬────┬─────────┬──────┬────────┬───────────┐
│ Name        │ id │ mode    │ ...  │ status │ ...
├─────────────┼────┼─────────┼──────┼────────┼───────────┤
│ mail-agent  │ 0  │ fork    │ ...  │ online │ ...
└─────────────┴────┴─────────┴──────┴────────┴───────────┘

## Save and Auto-start on Boot
pm2 save

## Generate startup script:
pm2 startup

## optional
pm2 restart mail-agent
pm2 stop mail-agent
pm2 logs mail-agent



