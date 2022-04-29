import time
import argparse
import getpass
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

#cli args
parser = argparse.ArgumentParser(description="Scrape linkedin comments")
parser.add_argument("--target", required=True, dest="target", help="The unique user profile name from the URL, linkedin.com/in/<target>/")
parser.add_argument("--headless", dest="headless", action="store_true", help="Use for headless browsing,but limited data")
parser.add_argument("--username", required=True, dest="username", help="linkedin username to log in")
parser.add_argument("--password", dest="password", help="linkedin password to log in, skip this arg to be secure")
parser.set_defaults(headless=False)
args = parser.parse_args()
targetUser = "/in/" + str(args.target) + "/"

#set target URL
recentActivityURL = "https://www.linkedin.com" + targetUser + "detail/recent-activity/"
print(recentActivityURL)

#### Linkedin Creds
linkedinUsername =  str(args.username)
if args.password == None:
    linkedinPassword = getpass.getpass(prompt='LinkedIn Password: ')
else:
    linkedinPassword = str(args.password)

#### Using Selenium Chrome Driver
options = Options()
options.headless = args.headless
chromeService = Service(ChromeDriverManager().install())
options.add_experimental_option('excludeSwitches',['enable-logging'])# resolves some unicode errors
driver = webdriver.Chrome(options=options, service=chromeService)

#add specific user agent here and go to login page
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"})
driver.get("https://www.linkedin.com/login")

#### locate username field by id
enterUsername = driver.find_element(By.ID, "username")
enterUsername.send_keys(linkedinUsername)
print(enterUsername)

##### locate password field by id
enterPassword = driver.find_element(By.ID, "password")
enterPassword.send_keys(linkedinPassword)
print(enterPassword)

##### locate submit button and click
submitCreds = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
submitCreds.click()

#browse to recent activity page of the target
driver.get(recentActivityURL)
time.sleep(3)

# try scrolling down 5 times to pull in more activity (maybe 50 additional 'items'?)
# could add cmd arg to specify
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

#soupify the recent activity page
recentActivityHTML = driver.page_source
recentActivitySoup = BeautifulSoup(recentActivityHTML, 'html.parser')

# write soup to file for testing
# with open("random.html", "w", encoding='utf-8') as file:
#     file.write(str(recentActivitySoup))

# #find the post blocks containing comments
posts = recentActivitySoup.find_all('article', class_="comments-comment-item comments-highlighted-comment-item comments-comment-item--highlighted comments-comments-list__highlighted-comment-item")
replies = recentActivitySoup.find_all('article', class_="comments-comment-item comments-reply-item reply-item")

#find comment authors and comments and compare to targetUser param
for post in posts:
    commentAuthor = post.find('a', class_="comments-post-meta__actor-link")['href']
    comments = post.find('div', class_="feed-shared-text relative", dir="ltr").text.strip()
    if targetUser == commentAuthor and comments != "None":
        print("Comment:" + comments + ' -- ' + commentAuthor)

# find replies made by the targetUser to other comments
for reply in replies:
    replyAuthor = reply.find('a', class_="comments-post-meta__actor-link")['href']
    replyComment = reply.find('div', class_="feed-shared-text relative", dir="ltr").text.strip()
    if targetUser == replyAuthor and replyComment != "None":
        print("Reply:" + replyComment + ' -- ' + replyAuthor)

print("Done!")
time.sleep(2)
