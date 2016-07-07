import requests, os
from urllib2 import urlopen, unquote, URLError, HTTPError
from os.path import abspath, isfile, join
from time import time
from os import remove

def write_to_file(arg_dir, file, f_name):
    """
    opens and writes video to file and displays progress bar during download
    :param arg_dir: dir value
    :param file: URL of file
    :param f_name: filename
    :return:
    """
    # open file for downloading
    # handles any potential errors

    try:
        d_file = urlopen(file)

    # Catch any HTTP Error
    except (requests.HTTPError):
        print("\n\nError: Failed to open the file. \n\n")
        exit(1)

    # Join Dir and file name
    pathname = abspath(join(arg_dir, name))

    # Check for conflicting file names
    if isfile(pathname):
        print ("\n\nError: Conflicting file name: ('{}').\nDownload Aborted.\n\n".format(name))
        exit(1)


    # Grab byte info
    meta = d_file.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_size = 8192

    # open file for writing flv to
    #handle file opening/writing errors

    try:
        with open(pathname, 'wb') as output:
            print("\n\nDownloading:'{0}' (Bytes: {1} | Megabytes: {2:.1f})\n\n".format(name, file_size, file_size/1024/1024))
            start = time()

            # Start loop to display status bar
            while True:
                # Read file's block size into buffer
                buffer = d_file.read(block_size)

                # break if empty buffer
                if not buffer:
                    break

                # Add current length of buffer to files downloaded amount
                file_size_dl += len(buffer)

                # Write buffer/file downloaded amount to file
                output.write(buffer)

                # Set download status for display
                try:
                    status = r'{0:10d} bytes | {1:.1f}MB | Completed: [{2:3.2f}%] Speed: {3:.2f} Mb/s'.format(
                        file_size_dl,
                        file_size/1024/1024.0,
                        file_size_dl * 100.0 / file_size,
                        float(file_size_dl*8/2**20)/(time()-start)
                    )
                # Catch error caused in windows
                except ZeroDivisionError:
                    continue

                # Update Status
                status = status + ' ' + chr(8)*(len(status)+1)

                # print status to screen
                print(status)

    except IOError:
        print("""\n\nError: Failed on: ('{0}').\nCheck that: ('{1}'), is a valid pathname.
            \nOr that ('{2}') is a valid filename.\n\n""".format(arg_dir, pathname[:-len(f_name)], f_name))
        exit(2)
    except BufferError:
        print('\n\nError: Failed on writing buffer.\nFailed to write video to file.\n\n')
        exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupt signal given.\nDeleting incomplete video ('{}').\n\n".format(f_name))
        remove(pathname)
        exit(1)


if __name__ == '__main__':
    dir = raw_input('Paste Path to Save file')
    # dir = 'I:\Movies2'
    url = raw_input('Paste URL')
    # url = 'http://www.funnymasti.com/data/17307.html'
    name = raw_input('Name of the file')
    # name = 'sample3.mp4'
    write_to_file(dir, url, name)


