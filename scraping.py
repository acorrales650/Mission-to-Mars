#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

   # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_links": hemisphere_image(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
        
    return news_title, news_p


# ### Featured Images
def featured_image(browser):
# Visit URL   
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");',"")
        return f'{PREFIX}_if/{article_background}'
    except:
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML
    return df.to_html()

def hemisphere_image(browser):
    
    # Visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with soup
    html = browser.html
    main_soup = soup(html, 'html.parser')

    # Add try/except
    try:
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

            browser.back()

    except BaseException:
        return None

    # Return the list that holds the dictionary of each image url and title
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



