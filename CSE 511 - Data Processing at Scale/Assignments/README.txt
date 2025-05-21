🐘 How to Start Your PostgreSQL Server on Arch Linux
✅ 1. Start the PostgreSQL service
This will start the server immediately:
sudo systemctl start postgresql.service

✅ 2. Enable PostgreSQL to start on boot
To make sure it starts every time your system boots:
sudo systemctl enable postgresql.service

✅ 3. Check PostgreSQL server status
To confirm it's running correctly:
sudo systemctl status postgresql.service

Look for:
  Active: active (running)

✅ 4. Stop or Restart the Server (if needed)
Stop the server:
sudo systemctl stop postgresql.service

Restart the server:
sudo systemctl restart postgresql.service

🧪 Bonus: Connect to a Database
Connect to your PostgreSQL database (e.g., moviedb) as user shachis:
psql -U shachis -d moviedb

