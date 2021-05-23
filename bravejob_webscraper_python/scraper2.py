#scraper2.py
#by Corey Warren II

#The Purpose of this program is to practice web scraping.
#This code shall also implement some basic custom data
#cleansing methods.
#For this code, I will take job data from Brave careers
#webpage.

#STEP 1: GET URL FROM GRNHSE_IFRAME (aka get the "src")
#STEP 2: GRAB DATA FROM THE HTML ON THAT NEW URL
#STEP 3: DO BASIC DATA CLEANSING
#STEP 4: PRINT TO CONSOLE
#STEP 5: WRITE TO TXT IN FOLDER

#Resources:
#Scraping iFrame with python
#   https://stackoverflow.com/questions/47068125/scraping-iframe-with-python
#Python String Commands and Manipulation
#   https://www.w3schools.com/python/python_ref_string.asp
#   https://www.w3schools.com/python/ref_string_strip.asp
#   https://gis.stackexchange.com/questions/4748/python-question-how-do-i-extract-a-part-of-a-string
#How To Build A Web Scraper With Python Using Beautiful Soup [2020] #selftaughtdev
#   https://www.youtube.com/watch?v=vIjXuYRLge8
#Python Tutorial: Web Scraping with BeautifulSoup and Requests
#   https://www.youtube.com/watch?v=ng2o98k983k
#Python: Keep changes on a variable made within a function
#   https://stackoverflow.com/questions/53249829/python-keep-changes-on-a-variable-made-within-a-function

from bs4 import BeautifulSoup
import requests
import urllib
from selenium import webdriver

#Get URL
driver = webdriver.Chrome()
driver.get('https://brave.com/careers/?gh_jid=2604828')
html_source = driver.page_source

soup = BeautifulSoup(html_source, "html.parser")

hiddenurl = soup.find('iframe', id="grnhse_iframe")

print("Scraped hidden grnhse iframe container text:")
print(hiddenurl)                                        #hiddenurl consists of all the container parameters of the aforementioned iframe

src_string = str(hiddenurl)                             #hiddenurl is NoneType, so convert it to string

print("src_string = ", src_string)                      #sanity check,
print()                                                 #just verifying that the string was extracted from hiddenurl


mypos = src_string.find("src=")                         #find where "src" is in this long string called mypos
print(".find returns: ", mypos, ".")                    #sanity check

print(src_string[mypos+5:])
src_string = src_string[mypos+5:]

#find where the URL ends
mypos = src_string.find('"')
print("Final URL:")
print(src_string[:mypos])
src_string = src_string[:mypos]

#src_string is now == the URL of the job posting!
#Success!

#Now do another scrape of that more useful URL (it contains the actual job listing text)

driver.get(src_string)
html_source = driver.page_source
driver.quit()

soup = BeautifulSoup(html_source, "html.parser")
job_description = soup.find('div', id="content")

print("\n")
print("Found job_description:")
print(job_description)

#now extract:

#job title      (h1 class="app-title")
#location       (div class="location")
#paragraphs     (span style="font-weight: 400;")

#note: job title and location are singular,
#   however, job description is made up of many elements.
#   These elements must be clearned before printing to console
#   and writing them to an external .txt file.

jobtitle = soup.find('h1', class_='app-title').text

location = soup.find('div', class_='location').text.strip()

paragraphs = soup.find_all('span', style='font-weight: 400;')
    
#Print the Job Info to console
print("\n")
print("Job title:")
print(jobtitle)
print()
print("Location:")
print(location)
print()
print("Description:")


#Print the Description (requires more work, as it is in split parts)
#save changes to the actual description string array

i = 0
for  text in paragraphs:
    
    text = str(text)
    
    #cut the head (left side is cut off from text and discarded)
    mypos = text.find(';">')
    text = text[mypos+3:]
    
    #cut the tail (right side is cut off from text and discarded)
    mypos = text.find('</span>')
    text = text[:mypos]
    
    paragraphs[i] = text
    print(paragraphs[i])
    
    i += 1
    
    
print()
print("Done printing description paragraph array...")


#Write ALL of this cleansed, scraped info to a .TXT file

filename = 'bravejob.txt'       #this is the filename of written file
f = open(filename, 'w')         #write mode

f.write("Job Title: \n" + jobtitle + "\n\n")
f.write("Location: \n" + location + "\n\n")
for text in paragraphs:
    f.write(str(text))
    f.write("\n")


#Close the file, we are done writing.
f.close()


#Friendly Exit Message
print()
print("This information is also available as a .txt file in the same folder as this Python code...")
print("Thank you.")
print()






    

