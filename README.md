Collect information from the American SEC about investments in nuclear weapons held by Swiss companies. This is easy to adapt to other countries, or other lists of problematic companies.

Take the results with a large grain of salt. The SEC data also has errors sometimes, like a comma that's accidentally shifted three places to the left.

Download data with fetch.py and analyse it with analyse.py.

Notes about fetch.py:

* Please change the HTTP headers before using - the SEC insists on you supplying your name and contact information in this way.
* This downloads about 2GB of data in the default configuration. The SEC servers are fairly fast, it shouldn't take longer than an hour.
* This uses around 10GB of disk space in the default configuration and can easily use 25GB if you download a larger subset of the files the SEC offers.

Notes about analyse.py

* Right now this only creates a .csv file with the holding information - calculating sums and drawing graphs is not implemented yet.
* It takes a long time to run, maybe 30 minutes. I'm not sure why, most likely parsing a few thousand malformed xml files using Beautiful Soup is slow.
* It skips a lot of files which are maybe malformed, maybe a different report. I haven't checked.
