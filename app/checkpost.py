import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium import webdriver


def check_linkedin_post(url: str, event: str) -> bool:
    '''This function checkLinkedinpost() returns True or False if the post is valid or invalid respectively.'''

    # Send an HTTP GET request to the URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title").text

        article = soup.find_all(
            'article', class_='relative pt-1.5 px-2 pb-0 bg-color-background-container container-lined main-feed-activity-card main-feed-activity-card-with-comments')[0]

        # Find the content of post by inspecting the HTML structure
        post_content = article.find(
            'p', class_='attributed-text-segment-list__content text-color-text !text-sm whitespace-pre-wrap break-words').text

        image_list_items = article.find_all(
            'li', class_='bg-color-background-container-tint col-span-full row-span-full')

        print('Title -> ', title)
        print(post_content)
        print(image_list_items)

        if event not in post_content:
            return False

        # Extract the src attributes of each image
        if len(image_list_items) > 0:
            for item in image_list_items:
                img_element = item.find('img')
                if img_element:
                    src = img_element.get('data-delayed-url')
                    print(src)
                else:
                    print("Image element not found.")
        else:
            print("Image element not found.")
            return False
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)

    return True


def check_twitter_post(url: str, event: str) -> bool:
    '''This function checkTwitterpost() returns True or False if the post is valid or invalid respectively.'''
    
    # Specify the path to the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the URL in the browser
        driver.get(url)

        # Wait for some time to ensure the content is loaded (adjust this time as needed)
        time.sleep(5)


        # Parse the HTML content of the page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        tweet = soup.find("div", class_='css-901oao r-18jsvk2 r-37j5jr r-1inkyih r-16dba41 r-135wba7 r-bcqeeo r-bnwqim r-qvutc0').text
        print(tweet)


        if event not in tweet:
            driver.quit()
            return False

        tweet_img_element = soup.find_all('div', class_='css-1dbjc4n r-1p0dtai r-1mlwlqe r-1d2f490 r-11wrixw r-61z16t r-1udh08x r-u8s1d r-zchlnj r-ipm5af r-417010')
        # print(tweet_img_element)

        if len(tweet_img_element) <= 0:
            driver.quit()
            return False
        
        img_element = tweet_img_element[0].find('img')
        # src = img_element.get('data-delayed-url')
        print(img_element)

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        # Quit the driver
        driver.quit()

    return True

