==============
gdrivedownload
==============

Simple script that downloads all files from given Google Drive folder.

Requirements
------------

* Python 3.2+

Installation
------------
::

    pip install gdrivedownload


Usage
-----
::

    gdrivedownload client_id client_secret folder_id out_path


* `client_id` - Google Drive OAuth2 client ID
* `client_secret` - Google Drive OAuth2 secret key
* `folder_id` - Google Drive folder ID (usually the last part of the URL, like ``https://drive.google.com/drive/u/0/folders/<folder_id>``)
* `out_path` - output directory to put the files into. Will be created recursively if does not exist

OAuth2 keys can be obtained using `Google Developer Console <https://console.developers.google.com/>`_. Create a project,
then generate OAuth2 credentials for `Other` application type.
