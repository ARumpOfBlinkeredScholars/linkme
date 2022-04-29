# linkme
### Scrape LinkedIn Comments
Created as a reason to play with Python more. I noticed some of the higher-visibility LinkedIn posts get absolutely filthy with insults and political vomit. It seems some people are just as comfortable being an asshole on LinkedIn as they are on their own Facebook/Instagram/Parler/4chan accounts. I thought, "Damn, wouldn't it suck to end up working on a team with someone who is so comfortable being a prick that they would do it with their company logo attached?"

I wanted to see if I could put something together that would make it easier to see this type of social media behavior. Nothing fancy, uses Selenium to log in to LinkedIn, browse to the activity page of your target user, and filter out some comments and replies they've made.


```
usage: linkme.py [-h] --target TARGET [--headless] --username USERNAME [--password PASSWORD]

Scrape linkedin comments

options:
  -h, --help           show this help message and exit
  --target TARGET      The unique user profile name from the URL, linkedin.com/in/<target>/
  --headless           Use for headless browsing,but limited data
  --username USERNAME  linkedin username to log in
  --password PASSWORD  linkedin password to log in, skip this arg to be secure
  ```
