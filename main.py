import argparse
import os
import sys

import httplib2
from apiclient import errors
from apiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


def create_argparser():
    """Create ArgumentParser with oauth and our arguments.

    :rtype: argparse.ArgumentParser
    """
    description = ('Downloads all files from provided Google Drive folder '
                   'into out_path.')
    parser = argparse.ArgumentParser(parents=[tools.argparser],
                                     description=description)
    parser.add_argument('client_id', help='OAuth2 client ID')
    parser.add_argument('client_secret', help='OAuth2 client secret')
    parser.add_argument('folder_id', help='Google Drive folder ID to get the '
                                          'files from')
    parser.add_argument('out_path', help='Path to the output directory')
    return parser


def create_service(flags, client_id, client_secret):
    """Create Google Drive service using provided Flow flags and OAuth keys

    :param argparse.Namespace flags: flags to be used with run_flow function
    :param str client_id: OAuth2 client id to use
    :param str client_secret: OAuth2 client secret to use
    :return: Google Drive service object
    :rtype: apiclient.discovery.Resource
    """
    flow = OAuth2WebServerFlow(
            client_id=client_id,
            client_secret=client_secret,
            scope='https://www.googleapis.com/auth/drive.readonly',
            redirect_uri='http://localhost')
    storage = Storage('oauth_storage')
    credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(httplib2.Http())
    return build('drive', 'v2', http=http)


def get_file(service, file_id):
    """Get single file metadata

    :param service: Google Drive service object
    :param str file_id: ID of the file to get the metadata of
    :return: file metadata
    """
    return service.files().get(fileId=file_id).execute()


def download_file(service, file_id, file_path):
    """Download file to provided path

    :param service: Google Drive service object
    :param str file_id: ID of the file to download
    :param str file_path: path to download the file to
    """
    request = service.files().get_media(fileId=file_id)
    with open(file_path, mode='wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()


def download_files(service, file_list, out_path):
    """Download all files from provided list

    :param service: Google Drive service object
    :param iterable[str] file_list: list of file IDs to download
    :param str out_path: path to the directory download the files to
    """
    total = len(file_list)
    for i, file_id in enumerate(file_list, 1):
        name = get_file(service, file_id)['title']
        print('Downloading {}... ({}/{}) [{}%]'.format(name, i, total,
                                                       round(i / total * 100)))
        path = os.path.join(out_path, name)
        try:
            download_file(service, file_id, path)
        except errors.HttpError as error:
            os.remove(path)  # Remove broken file
            print('Could not download file: {}'.format(error), file=sys.stderr)


def get_file_list(service, folder_id):
    """Get list of files in given Drive directory

    :param service: Google Drive service object
    :param str folder_id: ID of the folder to get file list of
    :return: list of file IDs
    :rtype: list[str]
    """
    result = []

    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.children().list(
                    folderId=folder_id, **param).execute()

            for child in children.get('items', []):
                result.append(child['id'])
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError as error:
            print('Could not retrieve file list: {}'.format(error))
            break

    return result


if __name__ == '__main__':
    args = create_argparser().parse_args()
    os.makedirs(args.out_path, exist_ok=True)
    service = create_service(args, args.client_id, args.client_secret)

    print('Getting list of files in {}...'.format(args.folder_id))
    file_list = get_file_list(service, args.folder_id)
    print('Retrieved list of {} files'.format(len(file_list)))

    download_files(service, file_list, args.out_path)
