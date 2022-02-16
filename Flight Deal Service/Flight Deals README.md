# Flight Deals
_Save and run all files and folders in the same level of your directory_

This program helps find deals on flights for destinations of your choice!

The program scans a list of your desired destinations and uses the Tequila API to find outgoing and return flights to and from your destination. 
Next, the program compares these trip totals against your budget, and if something is in your budget it will send you a
text letting you know that prices are low!

You will need a couple technologies to implement this code:

**Google Sheets**

In order to run this code, you will need a google sheet that lists your destination cities, the airport code, and your budget for that destination.
You will also need to input your sheety username, password, and sheet url into the "data_manager" file.
If you choose, there is also a data_manager file and class that can help add phone numbers to this service and allow you to send notifications to multiple people. 
Currently, the code is set up for one person and one number. You would need an additional google sheet to embrace this feature, along with a twilio paid account.

**Twilio**

The notification program sending the SMS messages is twilio. You will need a twilio account. Your Client ID, your Secret ID, your twilio phone number, and your
personal phone number need to be entered into the "notification_manager" file. 

**Tequila**

The search function of this program uses the Tequila API, more specifically their "locations" query.
You will need a Tequila's developer account utilizing their flight tools. From this account, you'll get your API key which you should input into the "flight_search" file.

Note:_The program was designed to search inbound and return flights seperately rather than as a round trip because the Tequila API would sometimes miss opportunities._

