# Braintree Transaction Statistics GUI

Hello!

This is a GUI which displays various statistics on transactions from a Braintree gateway. It's designed to provide a quick and comprehensive snapshot of your Braintree transaction processing without having to go through the hassle of logging into the gateway and manually gathering the various stats provided in the GUI.

## Setup

The app must connect to a Braintree gateway via API keys. Copy the contents of the .env-template file to a new file titled: .env. Inside of .env, fill in your Braintree API keys in the designated fields:

```
MERCHANT_ID = "Merchant ID goes here"
PUBLIC_KEY = "Public key goes here"
PRIVATE_KEY = "Private key goes here"
ENVIRONMENT = "Sandbox or Production goes here"
```

"Sandbox" is loaded in the template by default on the ENVIRONMENT variable, however if you want to run this on a production gateway instead, simply change that to "Production" instead.

## Running the app

Once you've entered your API keys, you're ready to run the app. It's a command line app with a builtin alias/entry point: **runstats**. To run the app, open a terminal and navigate to the root directory, then call the file with any of the below mentioned argument methods:

1. **Executed with zero arguments**: If no arguments are provided, a default date range of the last 30 days is used.
2. **Executed with a single integer argument**: If only one argument is provided, it must be an int and that int will be used to calculate how many days back the GUI will search. For example, if 10 is passed, the GUI will search for all transactions in the last 10 days.
3. **Executed with two date arguments**: If two arguments are provided, they must be dates in MM/DD/YYYY or MM/DD/YY format and those dates will be used as the start and end dates for the search. For example, if 1/1/2023 and 2/15/2023 are provided, the GUI will search for all transactions from January 1st, 2023 to February 15th, 2023.

Whichever method you use, you can then run subsequent new searches without having to close and re-launch the GUI by using the calendar. Click the **Show Calendar** button at the top of the GUI, then select two dates anywhere within the calendar and a new search will automatically run. This can be repeated as much as you like.

### Examples

```
# Default method
runstats
```

```
# Days back method
runstats 10
```

```
# Search range method
runstats 10/15/23 10/15/24
```

Thank you and enjoy!

-- Rickey