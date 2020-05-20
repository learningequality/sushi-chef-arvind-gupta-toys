# Arvind Gupta toys = Toys from trash

Sushi Chef script for importing Arvind Gupta toys content from
[http://www.arvindguptatoys.com/films.html](http://www.arvindguptatoys.com/films.html)


## Installation

1. Install the system prerequisites `ffmpeg` and `imagemagick` by following the
   [prerequisite install instructions](https://ricecooker.readthedocs.io/en/latest/installation.html#software-prerequisites).
2. Install [Python 3](https://www.python.org/downloads/) if you don't have it already.
3. Make sure you also have `pip` installed by running the command `pip --help`
   in a terminal, and if missing [install it](https://pypi.python.org/pypi/pip).
4. Create a Python virtual environment for this project:
   * Install the virtualenv package: `pip install virtualenv`
   * The next steps depends if you're using UNIX or Windows:
      * For UNIX systems (Linux and Mac):
         * Create a virtual env called `venv` in the current directory using the
           following command: `virtualenv -p python3  venv`
         * Activate the virtualenv called `venv` by running: `source venv/bin/activate`.
           Your command prompt should change and show the prefix `(venv)` to
           indicate you're now working inside `venv`.
         * **Checkpoint**: Try running `which python` and confirm the Python in
           is use the one from the virtual env (e.g. `venv/bin/python`) and not
           the system Python. Check also `which pip` is the one from the virtualenv.
         * You may encounter this error `SSL: CERTIFICATE_VERIFY_FAILED`. to fix it, 
           at the terminal run the command `sudo /Applications/Python (your Python version)/Install Certificates.command`
      * For Windows systems:
         * Create a virtual env called `venv` in the current directory using the
           following command: `virtualenv venv`.
         * Activate the virtualenv called `venv` by running `.\venv\Scripts\activate`
         * **Checkpoint**: Try running `python --version` and confirm the Python
           version that is running is the same as the one you downloaded in step 2.


## To run the sushi chef script

      source credentials/proxy_list.env
      nohup ./sushichef.py -v --reset --compress --thumbnails --token=credentials/channeladmin.token &

---



## Instructions and channel rubric

A sushi chef script has been created for you in `sushichef.py` to help you get
started on the import of the content.

1. Start by looking at the [**channel spec**](https://www.notion.so/learningequality/Arvind-Gupta-Toys-21e711bc8d304e1eab704e8c33575d49) that describes the target channel structure,
   licensing information, and tips about content transformations that might be necessary.
2. Add the code necessary to create this channel by modifying the `construct_channel`
   method of the chef class defined in `sushichef.py`.

Use the following rubric as a checklist to know when your sushi chef script is done:

### Main checks

1. Does the channel correspond to the spec provided?
2. Does the content render as expected when viewed in Kolibri?

### Logistic checks

1. Is the channel uploaded to Studio and PUBLISH-ed?
2. Is the channel imported to a demo server where it can be previewed?
3. Is the information about the channel token, the studio URL, and demo server URL
   on notion card up to date? See the [Studio Channels table](https://www.notion.so/761249f8782c48289780d6693431d900).
   If a card for your channel yet doesn't exist yet, you can create one using
   the `[+ New]` button at the bottom of the table.

### Metadata checks

1. Do all nodes have appropriate titles?
2. Do all nodes have appropriate descriptions (when available in the source)?
3. Is the correct [language code](https://github.com/learningequality/le-utils/blob/master/le_utils/resources/languagelookup.json)
   set on all nodes and files?
4. Is the `license` field set to the correct value for all nodes?
5. Is the `source_id` field set consistently for all content nodes?
   Use unique identifiers based on the source website or permanent url paths.

### Code standards

1. Does the section `Usage` in this README contain all the required information
   for another developer to run the script?
   Document and extra credentials, env vars, and options needed to run the script.
2. Is the Python code readable and succinct?
3. Are clarifying comments provided where needed?



## Kolibri content development workflow

See the [ricecooker docs](https://ricecooker.readthedocs.io/en/latest/concepts/developer_workflows.html#developer-workflows) for more info.