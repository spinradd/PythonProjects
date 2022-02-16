# Find Apartment Leases

This program scours apartments.com for a selection of leases of your choice!

This code will first search apartments.com using a search url you provided, and go through all the result pages.
While mining, it will store the address, the rent-range of the property, and the url of the opportunity.

After that, it will automatically travel to a google form of your creation where it will continuously fill out the google form until all the entries have been entered.

To do this, you will need to create a google form that uses three short answer inputs. Place the google sheet url into the "main" file.

This program was developed to work on using the selenium technology, but a more effective way to use this program would be to transfer the data using google sheets API.
