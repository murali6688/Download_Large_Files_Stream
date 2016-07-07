import requests, os

def download_video(url, name):
    # type: (object, object, object) -> object
    with open( name, 'wb') as handle:
        response = requests.get(url=url, stream=True)

        if not response.ok:
            print  'You Fucked up'

        for block in response.iter_content(1024):
            handle.write(block)


if __name__ == '__main__':
    url = raw_input('Paste URL')
    name = raw_input('Name of the file')
    download_video(url, name)
