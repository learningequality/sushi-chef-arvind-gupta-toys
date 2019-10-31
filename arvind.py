import pprint
import youtube_dl

from le_utils.constants.languages import getlang_by_name


# List of languages not avialble at the le_utils
UND_LANG = {
            "marwari":{
                "name":"Marwari",
                "native_name":"marwari",
                "code": "mwr",
            },
            "bhojpuri":{
                "name":"Bhojpuri",
                "native_name":"bhojpuri",
                "code":"bho",
            },
            "odiya":{
                "name":"Odiya",
                "native_name":"odiya",
                "code":"or",
            },
            "sci_edu":{
                "name":"Science/Educational",
                "native_name":"hindi",
                "code":"hi",
            },
    }


class ArvindLanguage():
    name = ''
    code = ''
    native_name = ''

    def __init__(self, name='', code='', native_name=''):
        self.name = name.lower()
        self.code = code
        self.native_name = native_name

    def set_value(self, name, code, native_name):
        self.name = name
        self.code = code
        self.native_name = native_name

    def get_lang_obj(self):

        if self.name != "":
            lang_name = self.name
            language_obj = getlang_by_name(lang_name)

            if not language_obj:
                
                if UND_LANG[self.name]:
                    self.set_value(UND_LANG[self.name]["name"], UND_LANG[self.name]["code"], UND_LANG[self.name]["native_name"])
                    return True
            else:
                self.set_value(language_obj.name, language_obj.code, language_obj.native_name)
                return True
        return False


class ArvindVideo():

    uid = 0   # value from `id` after `youtube_dl.extract_info()`
    title = ''
    description = ''
    url = ''
    language = ''
    thumbnail = ''  # local path to thumbnail image
    filepath = ''  # local path to video file
    filename_prefix = ''
    license = ''
    download_dir = './'
    license_common = False

    def __init__(self, uid=0, url='', title='', description='', language='', 
            filename_prefix=''):
        self.uid = str(uid)
        self.url = url
        self.title = title
        self.description = description
        self.thumbnail = None
        self.filepath = ''
        self.language = language
        self.filename_prefix = filename_prefix

    def __str__(self):
        return 'ArvindVideo (%s - %s - %s)' % (self.uid, self.url, self.title)

    def get_filename(self, download_dir='./'):
        filename = download_dir + self.filename_prefix + '%(id)s.%(ext)s'
        # MUST: make sure to save the `download_dir` for reuse later.
        self.download_dir = download_dir
        return filename

    def set_filepath_and_thumbnail(self, video_info, download_dir='./'):
        # MUST: assign the filename to the `filepath` attribute based on
        # the video_info dict argument.
        # Also traverses the `video_info['thumbnails']` list to get the image filename
        # to be used for the `thumbnail` attribute.
        filename = self.get_filename(download_dir=self.download_dir)
        self.filepath = filename % video_info

        for thumbnail in video_info.get('thumbnails', None):
            value = thumbnail.get('url')

            if value:
                self.thumbnail = value
                break

        return self.filepath

    def download_info(self, download_dir="./", download=False):
        print('====> download_info()', self.get_filename(download_dir))
        ydl_options = {
            'outtmpl': self.get_filename(download_dir),
            'writethumbnail': True,
            'no_warnings': True,
            'continuedl': False,
            'restrictfilenames': True,
            'quiet': False,
            # Note the format specification is important so we get mp4 and not taller than 480
            'format': "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]"
        }
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            pp = pprint.PrettyPrinter()
            try:
                ydl.add_default_info_extractors()
                # vinfo = ydl.extract_info(self.url, download=True)
                vinfo = ydl.extract_info(self.url, download=download)
                # Save the remaining "temporary scraped values" of attributes with actual values
                # from the video metadata.
                self.uid = vinfo['id']  # video must have id because required to set youtube_id later
                self.title = vinfo.get('title', '')
                self.description = vinfo.get('description', '')

                # Set the filepath and thumbnail attributes of the video object.
                self.filepath = self.set_filepath_and_thumbnail(vinfo, download_dir=download_dir)
                
                if not vinfo['license']:
                    self.license = "Licensed not available"
                elif "Creative Commons" in vinfo['license']:
                    self.license_common = True
                else:
                    self.license = vinfo['license']

            except (youtube_dl.utils.DownloadError,
                    youtube_dl.utils.ContentTooShortError,
                    youtube_dl.utils.ExtractorError,) as e:
                    print('==> Error downloading videos', e)
                    # pp.pprint(e)
                    return False
        return True
