#!/usr/bin/env python

import html
import os
import pprint
import requests
import urllib
import json
import youtube_dl
import uuid
import re

from bs4 import BeautifulSoup
from copy import copy

from ricecooker.chefs import SushiChef
from ricecooker.classes.files import VideoFile
from ricecooker.classes.licenses import get_license
from ricecooker.classes.nodes import ChannelNode, VideoNode, TopicNode

from le_utils.constants.languages import getlang_by_name

from arvind import ArvindVideo


LE = 'Learning Equality'

ARVIND = "Arvind Gupta Toys"

ARVIND_URL = "http://www.arvindguptatoys.com/films.html"

DOWNLOADS_PATH = os.path.join(os.getcwd(), "downloads")
DOWNLOADS_VIDEOS_PATH = os.path.join(DOWNLOADS_PATH, "videos/")

# These are the laguages that has no sub topics on its contents.
SINGLE_TOPIC_LANGUAGES = [
    "bhojpuri", "nepali", "malayalam", "telugu", "bengali", \
    "odiya", "punjabi", "marwari", "assamese", "urdu", \
     "spanish", "chinese", "indonesian", "sci_edu"
    ]

# List of multiple languages on its sub topics
MULTI_LANGUAGE_TOPIC = ["russian", "french",]

# This are the estimate total count of languages
TOTAL_ARVIND_LANG = 23

# List of languages not avialble at the le_utils
UND_LANG = {
            "marwari":{
                "name":"marwari",
                "native_name":"marwari",
                "code": "mwr",
            },
            "bhojpuri":{
                "name":"bhojpuri",
                "native_name":"bhojpuri",
                "code":"bho",
            },
            "odiya":{
                "name":"odiya",
                "native_name":"odiya",
                "code":"or",
            },
    }


SINGLE_TOPIC = "single"
STANDARD_TOPIC = "standard"
MULTI_TOPIC = "multi"


def get_lang_obj(lang_name):
    language_obj = None
    if lang_name:
        lang_name = lang_name.lower()
        language_obj = getlang_by_name(lang_name)
        if not language_obj:
            print("language not in le-utils laguages", lang_name)
    return language_obj


def clean_video_title(title, lang_obj):
    # Remove redundant and misleading words in the video title
    clean_title = title
    try:
        if title != None:
            clean_str = title.replace("-", "").replace("MB", "")
            clean_uplang = clean_str.replace(lang_obj.name.upper(), "")
            clean_lowlang = clean_uplang.replace(lang_obj.name.lower(), "")
            clean_caplang = clean_lowlang.replace(lang_obj.name.capitalize() , "")
            clean_format = clean_caplang.replace(".avi", "").replace(".wmv", "")
            clean_title = re.sub(r'\d+', '', clean_format)
            print("=====> clean title", clean_title)
    except Exception as e:
        print('Error cleaning video title:')
        pp.pprint(e)
    return clean_title


def include_video_topic(topic_node, video_data, lang_obj):
    video = video_data
    create_id = uuid.uuid4().hex[:6].lower()
    video_source_id = create_id + str(video.uid) 
    video_node = VideoNode(
        source_id=video.uid, 
        title=clean_video_title(video.title, lang_obj), 
        description=video.description,
        aggregator=LE,
        thumbnail=video.thumbnail,
        license=get_license("CC BY-NC", copyright_holder=ARVIND),
        files=[
            VideoFile(
                path=video.filepath,
                language=lang_obj.code
            )
        ])
    topic_node.add_child(video_node)


def download_video_topics(data, topic, topic_node, lang_obj):
    """
    Scrape, collect, and download the videos and their thumbnails.
    """
    pp = pprint.PrettyPrinter()

    for vinfo in data[topic]:
        try:
            video = ArvindVideo(
                url=vinfo['video_url'], 
                title=vinfo['video_title'], 
                language='english',
                filename_prefix=vinfo['filename_prefix'])
            print('==> DOWNLOADING', vinfo['video_url'])

            download_path = vinfo['download_path'] + "/" + topic + "/"
            if video.download(download_dir=download_path):
                include_video_topic(topic_node, video, lang_obj)

        except Exception as e:
            print('Error downloading videos:')
            pp.pprint(e)


def generate_child_topics(arvind_contents, main_topic, lang_obj, topic_type):

    pp = pprint.PrettyPrinter()
    data = arvind_contents[lang_obj.name]
    for topic_index in data:
        print("======> Language topic", topic_index)

        if topic_type == STANDARD_TOPIC:
            source_id = topic_index + lang_obj.code
            topic_node = TopicNode(title=topic_index, source_id=source_id)
            download_video_topics(data, topic_index, topic_node, lang_obj)
            main_topic.add_child(topic_node)

        if topic_type == SINGLE_TOPIC:
            download_video_topics(data, topic_index, main_topic, lang_obj)


    return main_topic


def create_language_data(lang_data, lang_obj, ):
    # Todo clean up this function
    pp = pprint.PrettyPrinter()
    topic_contents = {}
    initial_topics = []
    prev_topic = ""
    counter = 1
    topic_limit = 0
    parent_topic = 0
    total_loop = len(lang_data)
    # pp.pprint(lang_data)
    for item in lang_data:
        total_loop -= 1
        try:
            title = item.text.rstrip().strip()
            # pp.pprint(title)
            video_link = ""
            download_path = DOWNLOADS_VIDEOS_PATH + lang_obj.name
            try:
                video_link = item.a.get("href")
                topic_details = {}
                ytd_domain = "youtube.com"
                if ytd_domain in video_link:
                    topic_details['video_url'] = video_link
                    topic_details['video_title'] = title
                    topic_details['filename_prefix'] = 'arvind-video-'
                    topic_details['download_path'] = download_path
                    # uncomment this to limit topic
                    # if topic_limit != 1:
                    #     topic_limit += 1
                    initial_topics.append(topic_details)
            except:
                pass
            if counter == 1:
                if ":" in title:
                    counter = 0
                    prev_topic = title.replace(":", "").strip()

            if video_link == "":
                if ":" in title:
                    topic_contents[prev_topic] = initial_topics
                    prev_topic = title.replace(":", "").strip()
                    initial_topics = []
                    topic_limit = 0
                    # uncomment this to limit topic
                    # if parent_topic == 2:
                    #     break
                    parent_topic += 1
                    # pp.pprint(title)
        except:
            pass

        if total_loop == 0:
            topic_contents[prev_topic] = initial_topics
    return topic_contents


def scrape_arvind_page():
    url = ARVIND_URL
    pp = pprint.PrettyPrinter()

    response = requests.get(url)
    page = BeautifulSoup(response.text, 'html5lib')
    content_divs = page.body.div
    list_divs = list(content_divs.children)
    laguages_div_start = 5
    languages_list = list(list_divs[laguages_div_start].children)

    return languages_list


def create_languages_topic():
    arvind_languages = scrape_arvind_page()
    pp = pprint.PrettyPrinter()
    main_topic_list = []

    loop_max = TOTAL_ARVIND_LANG
    language_next_counter = 7
    lang_limit = 0
    loop_couter = 0
    # for i in range(loop_count):
    while (loop_couter != loop_max):
        try:
            lang_name = arvind_languages[language_next_counter].get('id')
            # Increase the language_next_counter to get the next language contents
            lang_obj = get_lang_obj(lang_name)
            if lang_obj != None:

                language_source_id = "arvind_main_" + lang_obj.code
                lang_name = lang_obj.name
                print("=====> Creating Language topic for ", lang_name)
                lang_name_lower = lang_name.lower()

                get_language_data = list(arvind_languages[language_next_counter])
                data_contents = { lang_name: create_language_data(get_language_data, lang_obj) }
                language_topic = TopicNode(title=lang_name.capitalize(), source_id=language_source_id)

                # Filter languages that only has a language topics contents format
                if lang_name_lower not in SINGLE_TOPIC_LANGUAGES and lang_name_lower not in MULTI_LANGUAGE_TOPIC:
                    # uncomment this to limit language
                    # if lang_limit == 8:
                    #     break
                    # lang_limit += 1

                    print("=======> This Language in standard format", lang_name)
                    print("=====>")

                    topic_type = STANDARD_TOPIC
                    generate_child_topics(data_contents, language_topic, lang_obj, topic_type)
                    main_topic_list.append(language_topic)

                    print("=====>finished", lang_name)

                if lang_name_lower in SINGLE_TOPIC_LANGUAGES:
                    # Handle the single topic languages
                    print("=====> This Language in single topic format ", lang_name)
                    print("=====>")
                     # uncomment this to limit language
                    # if lang_limit == 2:
                    #     break
                    # lang_limit += 1

                    topic_type = SINGLE_TOPIC
                    generate_child_topics(data_contents, language_topic, lang_obj, topic_type)
                    main_topic_list.append(language_topic)
                    print("=====>finished", lang_name)


                if lang_name_lower in MULTI_LANGUAGE_TOPIC:
                    # Handle the multi topic languages
                    print("=====> This Language in multiple langauage topic format ", lang_name)
                    print("=====>")
                    print("=====>finished", lang_name)
                    pass

        except Exception as e:
            pp.pprint(e)
            break
        language_next_counter += 4
        loop_couter += 1

    # pp.pprint(data_contents)
    return main_topic_list


class ArvindChef(SushiChef):
    channel_info = {
        "CHANNEL_TITLE": "Arvind Gupta Toys",
        # where you got the content (change me!!)
        "CHANNEL_SOURCE_DOMAIN": "arvindguptatoys.com",
        # channel's unique id (change me!!) # NOTE when you remove test- the channel_id will change; make sure to update notion card
        "CHANNEL_SOURCE_ID": "arvind-gupta-toys-beta-test",
        "CHANNEL_LANGUAGE": "mul",  # le_utils language code
        "CHANNEL_THUMBNAIL": 'chefdata/arvind_gupta_thumbnail.png',
        # (optional)
        "CHANNEL_DESCRIPTION": "Math and Science activities through low-cost " \
                "materials all in the form of videos to provide various pathways for children to explore" \
                " and deepen their understanding of concepts in low-resource contexts around the world." \
                " Valuable resource library for teachers to incorporate in their lessons, for parents to" \
                " work with children at home using readily available, simple, and low-cost materials.",
    }

    def construct_channel(self, **kwargs):

        channel = self.get_channel(**kwargs)

        languages_topic = create_languages_topic()
        for lang_topic in languages_topic:
            channel.add_child(lang_topic)
        return channel


if __name__ == "__main__":
    """
    Run this script on the command line using:
        python sushichef.py -v --reset --token=YOURTOKENHERE9139139f3a23232
    """

    chef = ArvindChef()
    chef.main()
    # create_languages_topic()