# Braintree Transaction Statistics GUI

Hello! As the name suggests, this repository contains a Python file which generates a GUI displaying various statistics on transactions from a Braintree gateway. This is designed to provide a quick and comprehensive snapshot of one's transaction processing without having to go through the hassle of logging into the Braintree gateway and manually gathering the various stats provided in the GUI.

The file can be stored anywhere in your system and run either directly from the file or from a terminal. It has three different launch methods:

1. **Executed with zero arguments**: If no arguments are provided, a default date range of the last 30 days is used.
2. **Executed with a single integer argument**: If only one argument is provided, it must be an int and that int will be used to calculate how many days back the GUI will search. For example, if 10 is passed, the GUI will search for all transactions in the last 10 days.
3. **Executed with two date arguments**: If two arguments are provided, they must be dates in MM/DD/YYYY (or MM/DD/YY) format and those dates will be used as the start and end dates for the search. For example, if 1/1/2023 and 2/15/2023 are provided, the GUI will search for all transactions within that date range.

Whichever method you use, you can then run subsequent new searches without having to close and re-launch the GUI by using the calendar. Click the **Show Calendar** button at the top of the GUI, then select two dates anywhere within the calendar and a new search will automatically run. This can be repeated as much as you like.

## Setup

The app is designed to be encompassed within the single Python file for ease of use so all that needs to be done is to add your Braintree API key credentials to the self.gateway var in the MainWindow class:

```
# Enter your API keys here.
            self.gateway = braintree.BraintreeGateway(
              braintree.Configuration(
                  braintree.Environment.Production,
                  merchant_id="",
                  public_key="",
                  private_key=""
              )
            )
```

Note that the app is set to be used with a production gateway by default. If you plan to use this with a sandbox instead, you'll want to use the sandbox version of the gateway object instead:

```
            self.gateway = braintree.BraintreeGateway(
              braintree.Configuration(
                  braintree.Environment.Sandbox,
                  merchant_id="",
                  public_key="",
                  private_key=""
              )
            )
```

Ensure that only one is included in the try block before running the file.

## Running the app

From there, open a terminal and navigate to the directory where the file is stored, then call the file with any of the above mentioned argument methods:

```
# Default method
python3 BTTransactionStatsGUI.py
```

```
# Days back method
python3 BTTransactionStatsGUI.py 10
```

```
# Search range method
python3 BTTransactionStatsGUI.py 10/15/23 10/15/24
```

Thank you and enjoy!

-- Rickey
