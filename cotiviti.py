import sqlite3

# Connect to SQLite database (creates file if it does not exist)
conn = sqlite3.connect('contracts_demo.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Contracts (
    contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payer_name TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Insert sample data
cursor.executemany('''
INSERT INTO Contracts (payer_name, provider_name, start_date, end_date, email)
VALUES (?, ?, ?, ?, ?)
''', [
    ('HealthCorp', 'DocSmith', '2023-01-01', '2024-01-01', 'docsmith@example.com'),
    ('Siddu', 'Telu', '2022-06-01', '2023-12-01', 'wildsid20@gmail.com'),
    ('WellnessInc', 'DrBrown', '2023-03-01', '2024-03-01', 'drbrown@example.com')
])

# Commit changes and close connection
conn.commit()
conn.close()

import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('contracts_demo.db')

# Query for contracts expiring soon
expiring_query = '''
SELECT * FROM Contracts
WHERE end_date < date('now', '+30 days')
'''

# Load data into a DataFrame
expiring_df = pd.read_sql(expiring_query, conn)

# Email setup
sender = 'your_email@example.com'
smtp_server = 'smtp.example.com'
smtp_port = 587
username = 'your_email@example.com'
password = 'your_password'

for index, row in expiring_df.iterrows():
    recipient = row['email']
    subject = f'Contract Expiration Reminder for {row["provider_name"]}'
    body = f'''
    Dear {row["provider_name"]},

    This is a reminder that your contract with {row["payer_name"]} is set to expire on {row["end_date"]}.
    Please review the contract terms and initiate renewal discussions if necessary.

    Best regards,
    Contract Management Team
    '''

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, recipient, msg.as_string())

# Close connection
conn.close()

