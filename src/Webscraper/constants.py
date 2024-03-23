# This file contains constants, which are useful in other files.


"""
When making a web request, the web client sends a string called 'User-Agent' to the web server to identify himself.

Now, if python makes a web request, the User Agent looks something like this:
'python-requests/2.26.0'

Which can easily be detected and blocked, therefore causing the error 403 Forbidden and hindering the Web Scraping.

By using the following User-Agent, we can bypass the bot-detection:

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
# Note : If this User-Agent becomes invalid, we could use the library 'random_user_agent'


# This is the url the webscraper takes data from
cfsre_url = "https://www.cfsre.org/nps-discovery/monographs"