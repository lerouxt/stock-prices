stock-prices
============

Python script that will get latest close prices for a set of stocks in OFX format.

If you are one of the few people who still use the sunsetted version of
Microsoft Money, then you can use this script to get the latest stock prices
from www.aphavantage.co.  You will need to get an API key from them, but it's
free and the product coverage is decent.

    $ ./prices_alpha.py --apikey=<file-with-apikey> --stockfile=<file-with-stocks> > ofx.ofx

Then you can use 'File, Import, Import Statement' within MS Money to process
the OFX file.

Note that Money requires you to differentiate stocks and mutual funds, so the
format of the stock file is a bit nutty.  Just prefix your symbol with MF: for
mutual funds, and S: for stocks, like this:


    MS:TIPS
    S:MSFT

Enjoy.
