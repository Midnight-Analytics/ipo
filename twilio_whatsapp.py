import os
import json
import pandas as pd
from twilio.rest import Client
from ipo_calendar import Calendars

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)



data = Calendars().future_ipo()
data2 = json.loads(data)
data3 = pd.json_normalize(data2)
data4 = data3.head()
data5 = data3[['date','company']]
#data5 = data5.reset_index(drop=True)
print(str(data5.set_index('company')))

message = client.messages.create(
                              #body='Hello there!',
                              body=str(data5.set_index('company')),
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+447777777777'
                          )

print(message.sid)