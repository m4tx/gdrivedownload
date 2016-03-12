# gdrivedownload

Simple script that downloads all files from given Google Drive folder.

## Requirements

* Python 3.2+

## Installation

```
pip install -r requirements.txt
```

You can use virtualenv if you want.

## Usage

```
python main.py client_id client_secret folder_id out_path
```

* `client_id` - Google Drive OAuth2 client ID
* `client_secret` - Google Drive OAuth2 secret key
* `folder_id` - Google Drive folder ID (usually the last part of the URL,
    like `https://drive.google.com/drive/u/0/folders/<folder_id>`)
* `out_path` - output directory to put the files into. Will be created recursively if does not exist
