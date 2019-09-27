#!/usr/bin/env python

import html
import os
import pprint
import requests
import urllib
import json
import youtube_dl

from bs4 import BeautifulSoup
from copy import copy

from ricecooker.chefs import SushiChef
from ricecooker.classes.files import VideoFile
from ricecooker.classes.licenses import get_license
from ricecooker.classes.nodes import ChannelNode, VideoNode

from arvind import ArvindVideo


AVIND_URL = "http://www.arvindguptatoys.com/films.html"

DOWNLOADS_PATH = os.path.join(os.getcwd(), "downloads")
DOWNLOADS_VIDEOS_PATH = os.path.join(DOWNLOADS_PATH, "videos/")

TEMP_HTML_FILE = os.path.join(DOWNLOADS_PATH, "temp/web.html")


def create_language_data(lang_data):
    # Todo clean up this function
    pp = pprint.PrettyPrinter()
    topic_contents = {}
    initial_topics = []

    prev_topic = ""

    counter = 1
    total_loop = len(lang_data)
    for i in lang_data:
        total_loop -= 1
        try:
            title = i.text.rstrip().strip()
            # pp.pprint(title)

            vid_link = ""
            
            try:
                vid_link = i.a.get("href")
                link_details = {}
                link_details['video_link'] = vid_link
                link_details['video_title'] = title
                initial_topics.append(link_details)
                # return
            except:
                # pp.pprint(i.strip())
                pass

            if counter == 1:
                if ":" in title:
                    counter = 0
                    prev_topic = title

            if vid_link == "":
                if ":" in title:
                    topic_contents[prev_topic] = initial_topics
                    prev_topic = title
                    initial_topics = []
                    pp.pprint(title)
            
            pass
        except:
            # pp.pprint(i.strip())
            pass

        if total_loop == 0:
            topic_contents[prev_topic] = initial_topics
    return topic_contents

def scrape_page(url):
    pp = pprint.PrettyPrinter()

    # TODO: check if local html file exist if not create it
    # Online scrape
    response = requests.get(url)
    page = BeautifulSoup(response.text, 'html5lib')

    # if not os.path.exists(TEMP_HTML_FILE):
    #     file = open(TEMP_HTML_FILE, "w") 
    #     file.write(page.prettify())
    #     file.close() 

    # Offline scrape
    # response = urllib.request.urlopen(LOCAL_HTML_PATH)
    # page = BeautifulSoup(response, 'html5lib')

    content_divs = page.body.div

    list_divs = list(content_divs.children)
    language_divs = list(list_divs[5].children)
    # language divs is a list of language just

    # To get the first language append four to the language counter
    language_counter = 7
    get_language = list(language_divs[language_counter])
    # create_language_data(get_language)
    # pp.pprint(list(language_divs)[7])
    lang_name = language_divs[language_counter].get('id')
    data_contents = { lang_name: create_language_data(get_language) }

    # pp.pprint(data_contents)
        

def scrape_video_data(url ,title):

    params = {"format": "json", "url": url}
    url_embed = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url_embed + "?" + query_string
    video_data = {}
    print(url)
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        video_data = json.loads(response_text.decode())

    video_data = []
    pp = pprint.PrettyPrinter()
    try:
        video = ArvindVideo(
                    url=src, 
                    title=title, 
                    description=description, 
                    lang_code=lang_code,
                    filename_prefix=filename_prefix)
        video_data.append(video)

    except Exception as e:
        print('==> Error scraping video URL', url)
        pp.pprint(e)
    return video_data

def download_videos(lang_code):
    """
    Scrape, collect, and download the videos and their thumbnails.
    """
    video_data = []
    vinfo = DATA[lang_code]['video_info']
    try:
        download_path = vinfo['download_path']
        video_data = scrape_video_data(
                            vinfo['video_url'], 
                            lang_code, 
                            vinfo['filename_prefix'])
        print('==> DOWNLOADING', download_path, '====> vinfo', vinfo)
        # Download video and metadata info for all video objects collected.
        for i, video in enumerate(video_data):
            progress = '%d/%d' % (i+1, len(video_data),)
            progress = '==> %s: Downloading video from %s ...' % (progress, video.url,)
            print(progress)
            if video.download(download_dir=download_path, video_data=DATA):
                # TODO(cpauya): Create VideoTopic then add to channel.
                pass
    except Exception as e:
        print('Error downloading videos:')
        pp = pprint.PrettyPrinter()
        pp.pprint(e)
        raise e
    print('==> DONE downloading videos for', vinfo)
    return video_data

def build_english_video_topics(topic):
    """
    """
    video_data = download_videos(LANG_CODE_EN)
    if not video_data:
        print('==> Download of Videos FAILED!')
        return False


    for i, video in enumerate(video_data):
        filepath = video.filepath
        video_node = VideoNode(
                source_id=video.uid, 
                title=video.title, 
                description=video.description,
                aggregator=LE,
                thumbnail=video.thumbnail,
                license=get_license("CC BY-NC-SA", copyright_holder=POINTB),
                files=[
                    VideoFile(
                        path=filepath,
                        language=LANG_CODE_EN
                    )
                ])
        topic.add_child(video_node)

    return topic


class ArvindChef(SushiChef):
    channel_info = {
        "CHANNEL_TITLE": "Arvind Gupta Toys",
        # where you got the content (change me!!)
        "CHANNEL_SOURCE_DOMAIN": "arvindguptatoys.com",
        # channel's unique id (change me!!) # NOTE when you remove test- the channel_id will change; make sure to update notion card
        "CHANNEL_SOURCE_ID": "beta-arvind",
        "CHANNEL_LANGUAGE": "en",  # le_utils language code
        "CHANNEL_THUMBNAIL": 'chefdata/channel_thumbnail.png',
        # (optional)
        "CHANNEL_DESCRIPTION": "",
    }

    def construct_channel(self, **kwargs):

        # English topics
        main_topic = TopicNode(title="English", source_id="arvind_en_main")
        topic_videos_en = TopicNode(title="Videos", source_id="arvind_en_videos")
        main_topic.add_child(topic_videos_en)

        # English videos
        topic = build_english_video_topics(topic_videos_en)


if __name__ == "__main__":
    """
    Run this script on the command line using:
        python sushichef.py -v --reset --token=YOURTOKENHERE9139139f3a23232
    """
    path_maker()
    scrape_page(AVIND_URL)

    # chef.main()
    # url = 'https://www.youtube.com/watch?v=TcppMhWI8-U'
    # scrape_video_data(url)











