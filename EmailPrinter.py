import re
import requests

def emailCrawler(url):
    response = requests.get(url, verify=False)
    content = response.text
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_regex, content)
    for email in emails:
        print(email)
