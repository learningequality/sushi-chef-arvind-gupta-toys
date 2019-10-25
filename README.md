# Arvind Gupta toys = Toys from trash

Sushi Chef script for importing Arvind Gupta toys content from [http://www.arvindguptatoys.com/films.html](http://www.arvindguptatoys.com/films.html)

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
5. Run `pip install -r requirements-dev.txt` to install the development python libraries.

### To run the sushi chef script

      python sushichef.py -v --reset --token=<Kolibri Studio token>

---

## About

A sushi chef script is responsible for importing content into Kolibri Studio.
The [ricecooker](https://github.com/learningequality/ricecooker) library provides
all helper methods necessary for uploading the content to Kolibri Studio.
The ricecooker docs can be found [here](https://ricecooker.readthedocs.io/en/latest/).

This repo includes two sample chef scripts in `examples/openstax_sushichef.py` (json)
and `examples/wikipedia_sushichef.py` (html). To find more code examples, search
for [`sushi-chef-*` on github](https://github.com/search?q=org%3Alearningequality+sushi-chef-%2A)
to see all the sushi chef scripts. They are all example of how to extract,
transform, and upload content from various sources of openly licensed content.

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

Running the sushichef script is only one of the steps in the Kolibri content
development workflow:

             ricecooker     studio       kolibri demo server
    SPEC-->--CHEF----->-----PUBLISH--->--IMPORT using token and REVIEW
    (1)      (2)            (3)          (4)                    (5)
      \______/                                                 /
       \______________________________________________________/

It is your responsibility as the chef author to take this channel all the way
through this workflow and make sure that the final channel works in Kolibri.

Notes on specific steps:

* `(1)`: the spec for the channel describes how the channel should be organized
* `(2)`: your main task as a chef author is to implement all the extraction
    and content transformation described in the spec. If you run into any kind
    of difficulties with this step post a question in the LE slack channel
    `#sushi-chefs` and someone from the content team will be able assist you.
    For example, "Hello @here I'm having trouble with the arvind-gupta-toys chef
    because X and Y cannot be organized according to the spec because Z."
    For complicated or very large channels the spec may go through multiple iterations.
* `(3)`: once the channel is on Studio you can preview the structure there
    and create or update a notion card with the channel information.
    The next step is to export the channel in the format necessary for use in
    Kolibri using the `PUBLISH` button on Studio. The PUBLISH action exports
    all the channel metadata to a sqlite3 DB file
    `https://studio.learningequality.org/content/databases/{channel_id}.sqlite3`
    the first time a channel is PUBLISH-ed a secret token is generated that can
    be used to import the channel in Kolibri. Note down the channel's token.
* `(4)`: the next step is to import your channel into a Kolibri instance. You
    can use Kolibri installed on your local machine or an online demo server.
    Admin (`devowner`) credentials for the demo server will be provided for you
    so that you can import and update the channel every time you push a new version.
    Follow these steps to import your channel `Device` > `IMPORT` > `ONLINE` >
    `Try adding a token`, add the channel token, select all nodes > `IMPORT`.
* `(5)`: You can now go to the Kolibri Learn tab and preview your channel to
    see it the way learners will see it. Take the time to click around and browse
    the content to make sure everything works as expected. Update the notion card
    and leave a comment. For example "First draft of channel uploaded to demo server."
    This would be a good time to ask a member of the LE content team to review
    the channel. You can do this using the `@Person Name` in your notion comment.
    Consult the content source notion card to know who the relevant people to tag.
    For example, you can @-comment the `Library` person on the card to ask them
    to review the channel—be sure to specify the channel's "level of readiness"
    in your comment, e.g., if it's a draft version for initial feedback, or
    the near-final, spec-compliant version ready for detailed review and QA.
    For async technical questions tag the `SushOps` person on the card or post
    your question in the `#sushi-chefs` channel. For example, "I downloaded this
    html and js content, but it doesn't render right in Kolibri because of the
    iframe sandboxing." or "Does anyone have sample code for extracting content
    X from a shared drive link Y of type Z?".
