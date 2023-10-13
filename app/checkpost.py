import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def check_linkedin_post(url: str) -> bool:
    '''This function checkLinkedinpost() returns True or False if the post is valid or invalid respectively.'''

    # Send an HTTP GET request to the URL
    try:
        response = requests.get(url, timeout=5)
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

        if '#365DaysofCode' not in post_content:
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

        # Iterate through the list of articles and print their titles
        # for img in post_img:
        #     print(img)

        # Twitter
        # tweet = soup.find_all("span", class_='r-18u37iz')

        # print('Tweet',tweet)

    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)

    return True

# link = 'https://twitter.com/The_LoneArtist/status/1712146803951312913'

# link = 'https://www.linkedin.com/posts/neelmishra07_day166-365daysofcode-scalerdiscord-activity-7118064337751072770-67vS?utm_source=share&utm_medium=member_desktop'
# link2 = 'https://www.linkedin.com/posts/ghanshyam-prajapati_what-do-you-do-if-someone-is-threatening-activity-7094201355233374208-6gor?utm_source=share&utm_medium=member_desktop'
# print('Status: ', check_linkedin_post(link))


def check_twitter_post(url: str) -> bool:
    '''This function checkTwitterpost() returns True or False if the post is valid or invalid respectively.'''

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install())

    # Send an HTTP GET request to the URL
    # response = requests.get(url)

    driver.get(url)

    time.sleep(5)

    # Check if the request was successful

    # Parse the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    print(soup)

    tweet = soup.find("div", class_='css-901oao r-1nao33i r-37j5jr r-1inkyih r-16dba41 r-135wba7 r-bcqeeo r-bnwqim r-qvutc0')

    print(tweet)

    driver.quit()
    return True


TWEET_LINK = 'https://twitter.com/The_LoneArtist/status/1712146803951312913'

check_twitter_post(TWEET_LINK)
