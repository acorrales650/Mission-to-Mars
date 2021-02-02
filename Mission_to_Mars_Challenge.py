#!/usr/bin/env python
# coding: utf-8

# In[24]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[25]:


from webdriver_manager.chrome import ChromeDriverManager


# In[26]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[27]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[9]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[46]:


# Find and click the full image button
#full_image_elem = browser.find_by_id('full_image')
#full_image_elem.click()


# In[47]:


# Find the more info button and click that
#browser.is_element_present_by_text('more info', wait_time=1)
#more_info_elem = browser.links.find_by_partial_text('more info')
#more_info_elem.click()


# In[10]:


#10.3.4
# Visit Archived JPL URL    
try:
    PREFIX = "https://web.archive.org/web/20181114023740"
    url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    article = browser.find_by_tag('article').first['style']
    article_background = article.split("_/")[1].replace('");',"")
    print (f'{PREFIX}_if/{article_background}')
except:
    print('https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg')


# In[20]:


# Visit Archived JPL URL
#PREFIX = "https://web.archive.org/web/20181114023740"
#url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#browser.visit(url)
#WAIT FOR THE PAGE TO COMPLETELY LOAD!!!🥃


# In[21]:


#article = browser.find_by_tag('article').first['style']
#article_background = article.split("_/")[1].replace('");',"")
#print(f'{PREFIX}_if/{article_background}')


# In[11]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[12]:


df.to_html()


# In[13]:


#browser.quit()


# ### Mars Weather

# In[14]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[15]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[16]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[28]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[31]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with soup
html = browser.html
main_soup = soup(html, 'html.parser')

image_count = len(main_soup.select("div.item"))

# for loop over the link of each sample picture
for i in range(image_count):
    # Create an empty dict to hold the search results
    results = {}
    # Find link to picture and open it
    link_image = main_soup.select("div.description a")[i].get('href')
    browser.visit(f'https://astrogeology.usgs.gov{link_image}')
    
    # Parse the new html page with soup
    html = browser.html
    sample_soup = soup(html, 'html.parser')
    # Get the full image link
    img_url = sample_soup.select_one("div.downloads ul li a").get('href')
    # Get the full image title
    img_title = sample_soup.select_one("h2.title").get_text()
    # Add extracts to the results dict
    results = {
        'img_url': img_url,
        'title': img_title}
    
    # Append results dict to hemisphere image urls list
    hemisphere_image_urls.append(results)
    
    # Return to main page
    browser.back()


# In[32]:


hemisphere_image_urls


# In[33]:


# 5. Quit the browser
browser.quit()


# In[ ]:




