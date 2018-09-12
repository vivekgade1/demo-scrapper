import pandas as pd
import time
import os
import urllib
import io

from selenium import webdriver
from google.cloud import vision
from google.cloud.vision import types
from InstagramScrapper.settings import GOOGLE_CLOUD_CREDENTIALS
import logging

logger = logging.getLogger('__instagram_scrapper__')


class InstagramScrapper(object):
    """
    #    Obtains images and their content- reviews and likes from a given instagram page.
    """

    def __init__(self, **kwrgs):
        default_attributes = dict(page_url='',
                                  # CHROME_PATH = '',
                                  comments_file='insta_comments_whiteshouse.xlsx',
                                  images_file='insta_images_whiteshouse.xlsx',
                                  page_load_time=4,
                                  post_loads=3,
                                  scroll_pause_time=4,
                                  max_posts=15,
                                  comment_loads=1,
                                  comment_load_time=3)

        default_attributes.update(kwrgs)
        for key in default_attributes:
            try:
                self.__dict__[key] = default_attributes.get(key)
            except:
                logger.critical(":::: Key doesnot exist ::::")

        # if self.CHROME_PATH is not None:
        try:
            self.driver = webdriver.PhantomJS()
        except:
            logger.critical(">>>>>> Chrome driver not found. <<<<<<")

        logger.info(":::: instance keys intiation successfull. ::::")
        self.post_links = []
        self.number_posts = 0
        # image user generated content
        self.image_ugc = dict(link_id=[], image_src=[], post_title=[],
                              likes=[], comments=[], user_name=[], user_comment=[])
        # dictionary for google tags
        self.image_tags = dict(post_id=[], labels=[], text=[], entities=[])

    def crawler_init(self):
        number_posts = self._scrape_posts()
        for idx in range(0, number_posts):
            image_source = self._scrape_image_ugc(idx)
            if image_source is not None:
                tagger = googleTags(image_source, GOOGLE_CLOUD_CREDENTIALS)
                tags = tagger._get_tags()
                self.image_tags['post_id'].append(idx)
                self.image_tags['labels'].append(tags[0])
                self.image_tags['text'].append(tags[1])
                self.image_tags['entities'].append(tags[2])
        self.driver.close()
        logger.info(":::: Chrome driving closed. ::::")
        # image_content = pd.DataFrame.from_dict(self.image_ugc).to_excel(self.comments_file, index=False)
        # image_tags = pd.DataFrame.from_dict(self.image_tags).to_excel(self.images_file, index=False)
        return (pd.DataFrame.from_dict(self.image_ugc), pd.DataFrame.from_dict(self.image_tags))

    def _pause(self, pause_time):
        # pause after an action on the webpage
        time.sleep(pause_time)

    def _scroll(self):
        # Get page height and scroll to the bottom of the page
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._pause(self.scroll_pause_time * 2)
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logger.info(":::: Seems like there are not many images in the page ::::")
            return True

    def _get_postlinks(self):
        # obtains href of each post from the active links
        links = self.driver.find_elements_by_xpath("//a[contains(@href, 'taken-by')]")
        for link in links:
            href_link = link.get_attribute("href")
            if href_link not in self.post_links:
                self.post_links.append(href_link)
        self.number_posts = len(self.post_links)

    def _scrape_posts(self):
        # obtain information on the posts- videos and images
        self.driver.get(self.page_url)
        # waiting for the page to load
        self._pause(self.page_load_time)
        self._scroll()
        post_loads = 1
        while True:
            if self._scroll():
                break
            self._get_postlinks()
            logger.info("Number of scrolls: ", post_loads)
            logger.info("Number of posts loaded: ", self.number_posts)
            post_loads += 1
            #             logger.info post_loads, self.post_loads, self.number_posts, self.max_posts
            if (post_loads >= self.post_loads) and (self.number_posts >= self.max_posts):
                break
        self._get_postlinks()
        return self.number_posts

    def _image_post(self):
        # check if the post is an image or a video
        post = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span').text
        return post.split()[1] != 'views'

    def _load_comments(self):
        # loading more comments
        elements = self.driver.find_elements_by_partial_link_text('comments')
        loads = 0
        while len(elements) > 0:
            self.driver.find_element_by_partial_link_text('comments').click()
            self._pause(self.comment_load_time)
            loads += 1
            elements = self.driver.find_elements_by_partial_link_text('comments')
            if loads > self.comment_loads:
                break
        comment_list = self.driver.find_elements_by_tag_name('li')
        return comment_list

    def _get_title(self, comments):
        """
        #   Obtain title or the description of the post.
        #   Assumption - first comment of the post made by the user-posting the picture.
        #   Since we are only looking at the posts of brands it is not a very wild assumption.
        #   There are chances it may go wrong please let me know if you come across such situations.
        """

        post_comment_elem = comments[0].find_elements_by_tag_name('span')
        if len(post_comment_elem) > 0:
            post_title = comments[0].find_element_by_tag_name('span').text
            return post_title
        else:
            return None

    def _get_image_stats(self):
        # retrieve image statistics such as number of likes, number of comments, etc.
        image = self.driver.find_element_by_xpath("//meta[contains(@name, 'description')]")
        content = image.get_attribute('content')
        contents = content.split()
        likes = contents[0]
        comments = contents[2]
        return (likes, comments)

    def _switch_driver_window(self, type=None):
        # switch between windows in python
        if type == 'new':
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
        elif type == 'old':
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            raise ValueError('switching windows without any intent')

    def _scrape_image_ugc(self, post_id):
        # scrape user generated content of an image.
        postlink = self.post_links[post_id]
        self._switch_driver_window('new')
        self.driver.get(postlink)
        time.sleep(self.page_load_time)
        image_src = None
        if self._image_post():
            image_url = self.driver.find_element_by_xpath("//meta[contains(@property, 'image')]")
            image_src = image_url.get_attribute('content')

            # retreiving number of likes and comments
            (likes, comments) = self._get_image_stats()
            comment_list = self._load_comments()

            post_title = self._get_title(comment_list)
            for comment_number in range(2, len(comment_list)):
                user_name_elem = comment_list[comment_number].find_elements_by_tag_name('a')
                user_comment_elem = comment_list[comment_number].find_elements_by_tag_name('span')
                if (len(user_name_elem) > 0) & (len(user_comment_elem) > 0):
                    user_name = comment_list[comment_number].find_element_by_tag_name('a').text
                    user_comment = comment_list[comment_number].find_element_by_tag_name('span').text
                    self.image_ugc['link_id'].append(post_id)
                    self.image_ugc['image_src'].append(image_src)
                    self.image_ugc['post_title'].append(post_title)
                    self.image_ugc['likes'].append(likes)
                    self.image_ugc['comments'].append(comments)
                    self.image_ugc['user_name'].append(user_name)
                    self.image_ugc['user_comment'].append(user_comment)
                else:
                    break
            logger.info(str(len(self.image_ugc['user_comment'])) + " " + str(post_id + 1))
        # switching back to the initial tab
        self._switch_driver_window('old')
        return image_src


class googleTags(object):
    """
    #    Vision analysis over the images using Google Cloud vision API
    """

    def __init__(self, url, Application_Credentials):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Application_Credentials
        self.image_name = "00000001.jpg"
        self.image_url = url

    def _get_image(self):
        # download the image
        urllib.request.urlretrieve(self.image_url, self.image_name)

    def _read_image(self):
        # read the image 
        with io.open(self.image_name, 'rb') as image_file:
            content = image_file.read()
        return content

    def _get_tags(self):
        # obtain web entities, text, and labels from the image
        self._get_image()
        content = self._read_image()
        client = vision.ImageAnnotatorClient()
        image = types.Image(content=content)
        response_label = client.label_detection(image=image)
        response_web = client.web_detection(image=image)
        response_text = client.text_detection(image=image)
        labels = response_label.label_annotations
        notes = response_web.web_detection
        texts = response_text.text_annotations
        image_labels = [label.description for label in labels]
        image_labels = " ".join(image_labels)
        image_text = [text.description for text in texts]
        image_text = " ".join(image_text)
        web_entities = []
        if notes.web_entities:
            for entity in notes.web_entities:
                if entity.score > 0.1:
                    web_entities.append(entity.description)
        web_entities = " ".join(web_entities)
        return [image_labels, image_text, web_entities]

# if __name__ == '__main__':
#     # dictionary of arguments
#     arguments = dict(page_url = 'https://www.instagram.com/whitehouse/',
#                                   # CHROME_PATH = '/Users/msbde164/Documents/chromedriver',
#                                   comments_file = 'insta_comments_whiteshouse.xlsx',
#                                   images_file ='insta_images_whitehouse.xlsx',
#                                   page_load_time = 4,
#                                   post_loads = 3,
#                                   scroll_pause_time = 4,
#                                   max_posts = 15,
#                                   comment_loads = 1,
#                                   comment_load_time = 3)
#     # instaCrawler = InstagramScrapper(**arguments)
#     # number_posts = instaCrawler._scrape_posts()
#     # # dictionary for google tags
#     # image_tags = dict(post_id=[], labels=[], text=[], entities=[])
#     # # application credentials
#     # for idx in range(0,number_posts):
#     #     image_source = instaCrawler._scrape_image_ugc(idx)
#     #     if image_source is not None:
#     #         tagger = googleTags(image_source, GOOGLE_CLOUD_CREDENTIALS)
#     #         tags = tagger._get_tags()
#     #         image_tags['post_id'].append(idx)
#     #         image_tags['labels'].append(tags[0])
#     #         image_tags['text'].append(tags[1])
#     #         image_tags['entities'].append(tags[2])
#     # instaCrawler.driver.close()
#     reponse = InstagramScrapper(**arguments).crawler_init()
#     image_content = instaCrawler.image_ugc
#     image_content = pd.DataFrame.from_dict(image_content)
#     image_tags = pd.DataFrame.from_dict(image_tags)
#     image_content.to_excel("comments.xlsx", index=False)
#     image_tags.to_excel("tags.xlsx", index=False)
