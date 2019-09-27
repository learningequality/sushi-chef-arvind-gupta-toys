import pprint
import youtube_dl


class ArvindVideo():

    uid = 0   # value from `id` after `youtube_dl.extract_info()`
    title = ''
    description = ''
    url = ''
    language = ''
    thumbnail = ''  # local path to thumbnail image
    filepath = ''  # local path to video file
    filename_prefix = ''
    download_dir = './'

    def __init__(self, uid=0, url='', title='', description='', language='', 
            filename_prefix=''):
        self.uid = str(uid)
        self.url = url
        self.title = title
        self.description = description
        self.thumbnail = ''
        self.filepath = ''
        self.language = language
        self.filename_prefix = filename_prefix

    def __str__(self):
        return 'ArvindVideo (%s - %s - %s - %s)' % (self.uid, self.url, self.title)

    def get_filename(self, download_dir='./'):
        # TODO(cpauya): How to get the mp4 filename from local path?
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
            value = thumbnail.get('filename', '')
            if value:
                self.thumbnail = value
                break

        return self.filepath

    def download(self, download_dir="./", video_data=None):
        print('====> download()', self.get_filename(download_dir))
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
                vinfo = ydl.extract_info(self.url, download=True)
                # Save the remaining "temporary scraped values" of attributes with actual values
                # from the video metadata.
                self.uid = vinfo.get('id', '')

                self.title = vinfo.get('title', '')                

                # TODO(cpauya): If Burmese, use the translated video description.

                # Set the filepath and thumbnail attributes of the video object.
                self.set_filepath_and_thumbnail(vinfo, download_dir=download_dir)
                # pp.pprint(self)

                # # These are useful when debugging.
                # del vinfo['formats']  # to keep from printing 100+ lines
                # del vinfo['requested_formats']  # to keep from printing 100+ lines
                # print('==> Printing video info:')
                # pp.pprint(vinfo)
                # print('==> NEW', self)
            except (youtube_dl.utils.DownloadError,
                    youtube_dl.utils.ContentTooShortError,
                    youtube_dl.utils.ExtractorError,) as e:
                # print('==> PointBVideo.download(): Error downloading videos')
                # pp.pprint(e)
                raise e
        return True
