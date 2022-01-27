# Pypypan Wikimedia Commons uploader
This project aims to serve as an alternative to the Pattypan upload tool for Wikimedia Commons.
It uses the same Excel (.xls) files as input.

## Installation
Python packages are published to https://pypi.org/project/pypypan/ and can be installed by running in a terminal (slightly OS dependent):

    pip3 install pypypan

## Authentication
Pypypan uses OAuth to authenticate with Wikimedia. Please consult https://www.mediawiki.org/wiki/Manual:Pywikibot/OAuth for more info, or go directly to https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose to create your OAuth tokens.
Make sure to:

- Check the checkbox 'This consumer is for use only by YourUserName'
- Either pick one applicable project, or use the wildcard
- Select the following for Applicable grants:
    - Edit existing pages
    - Upload new files
    - Upload replace and move files
    - High volume editing

- Copy (and save) the resulting tokens and secrets.
- Fill out ./user-config.py.dist (don't forget your username), and save it as ./user-config.py

## Usage

Usage instructions follow from:

    pypypan --help

Which outputs:

    Usage: pypypan [OPTIONS] COMMAND [ARGS]...

    Options:
    --install-completion [bash|zsh|fish|powershell|pwsh]
                                    Install completion for the specified shell.
    --show-completion [bash|zsh|fish|powershell|pwsh]
                                    Show completion for the specified shell, to
                                    copy it or customize the installation.
    --help                          Show this message and exit.

    Commands:
    generate-excel  Generate an excel file that is filled according to the...
    test-template   Parse a template and use the first file to generate the...
    upload          Upload an excel file that is filled according to the...

Command specific help can be found with e.g.:

    pypypan upload --help

Which outputs:

    Usage: pypypan upload [OPTIONS] EXCEL_FILE

        Upload an excel file that is filled according to the Pattypan format.

        Arguments:
        EXCEL_FILE  [required]

        Options:
        --update-existing / --no-update-existing
                                        [default: no-update-existing]
        --test-one / --no-test-one      [default: no-test-one]
        --use-test-commons / --no-use-test-commons
                                        [default: no-use-test-commons]
        --help                          Show this message and exit.