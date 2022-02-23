#!/usr/bin/env python
# coding: utf-8

# In[17]:


from bs4 import BeautifulSoup
import requests
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

import smtplib  # To send the email

# To create the email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime


# In[18]:


now = datetime.datetime.now()


# In[19]:


content = ''


# In[20]:


def extract_website_data(url):
    response = requests.get(url)
    content = response.content
    soup = soup = BeautifulSoup(content, 'html.parser') 
    links = soup.find_all('h2',{'class':'c-entry-box--compact__title'})
    return soup, links


# In[21]:


def get_only_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    title = ' '.join(soup.title.stripped_strings)
    return title, text


# In[51]:


list_of_links = []

def generate_content(links):
    cnt = ''
    for i in list(range(len(links))):
        link = links[i].a.get('href')
        list_of_links.append(link)
        page_content = get_only_text(link)
        summary = summarize(repr(page_content[1]), ratio=0.05)
        cnt += ('<br>' + page_content[0] + link + '\n' + summary + '\n' + '\n' + '<br>')
    return cnt


# In[52]:


soup, links = extract_website_data("https://www.vox.com/")
content = generate_content(links)
content += ('<br>--------------<br>') # Mark the end of the email
content += ('<br><br>End of message')


# In[53]:


print(content)


# In[55]:


# Sending the email...
print('Composing email...')
# First create the parameters required to send an email
SERVER = 'smtp.gmail.com' # Your smtp server
PORT = 587 # For gmail it is 587
FROM = '********' # The senders email address
TO = '*********' # The receivers email
PASS = '*********'

# We create a empty object to create the body of the email using MIMEMultipart()
msg = MIMEMultipart()

# We create a dynamic subject to the email using datetime
msg['Subject'] = 'Top News Stories HN [Automated Email]' + '' + str(now.day) + '_'+ str(now.month) + '_'+ str(now.year)
msg['From'] = FROM
msg['To'] = TO

# To make the email look easthetically more appealing we use the html format
msg.attach(MIMEText(content, 'html'))

# Authenticating the email
print('Initializing the server')

# Assign the server and the port
server = smtplib.SMTP(SERVER, PORT)
# If you want to see if there is any error like failing to connect to the server put "1" in the debug level
server.set_debuglevel(1)
# Initiate the server
server.ehlo()
# start the connection
server.starttls()
# logging using the id and pass
server.login(FROM, PASS)
# Send the mail
server.sendmail(FROM, TO, msg.as_string())
print('Email sent...')
server.quit()


# In[ ]:




