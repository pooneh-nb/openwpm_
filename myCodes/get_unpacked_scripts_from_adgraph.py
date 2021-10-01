import errno
import os
from os import listdir
from os.path import isfile, join
import sys
import shutil
import json
from myCodes import utilities


def read_json(file_addr):
    try:
        with open(file_addr) as json_data:
            d = json.load(json_data)
        return d
    except Exception as ex:
        print('Invalid Json', file_addr)
        return {}



def write_content(file_addr, list_content):
    with open(file_addr, 'wb') as out_file:
        for item in list_content:
            out_file.write(item.encode('utf-8') + b'\n')


def get_files_in_a_directory(directory_path):
    file_list = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    file_list_path = [os.path.join(directory_path, f) for f in file_list]
    return file_list_path



def process_file(f_addr, directory_to_write):
    json_obj = read_json(f_addr)
    if not json_obj:
        return

    url = json_obj['url']
    timeline = json_obj['timeline']


    script_text = []
    for item in timeline:
        if item['event_type'] == 'ScriptCompilation' or item['event_type'] == 'ScriptEval':
            script_text.append(item['script_text'])

    #file_name = url.strip().split('/')[-1].split('.com')[0]
    file_name = url.split('/')[-1]
    file_name = file_name.replace('%7C', '|').split('.')[0]
    #id = file_name.split('_')[0]
    write_content(directory_to_write + '/' + file_name, script_text)
    """if id.isdigit():
        write_content(directory_to_write + '/' + file_name, script_text)
    else:
        print('Invalid file name: ', file_name)
    return"""

def copy_files(src, dst):
    try:
        # if path already exists, remove it before copying with copytree()
        if os.path.exists(dst):
            shutil.rmtree(dst)
            shutil.copytree(src, dst)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            print('Directory not copied. Error: %s' % e)


def copy_to_all_plus_unpacked(unpacked_scripts, outdir):
    unpacked_scripts  = utilities.get_files_in_a_directory(unpacked_scripts)
    for js in unpacked_scripts:
        script_context = utilities.read_file_splitlines(js)
        script_name = js.split('/')[-1]
        utilities.write_dill_compressed(os.path.join(outdir, script_name), script_context)


def main():
    adgraph_processed_files_fir = "/home/c6/Documents//0.0.0.0"
    read_directory_path = '/home/c6/Documents/OpenWPM2/datadir/inline_js/unpacking/adgraph_processed'
    write_directory_path = '/home/c6/Documents/OpenWPM2/datadir/inline_js/unpacking/unpacked'

    # copy files from the adgraph' output in home/rendering_stream
    ##copy_files(adgraph_processed_files_fir, read_directory_path)

    if not os.path.exists(write_directory_path):
        os.makedirs(write_directory_path)

    all_files = get_files_in_a_directory(read_directory_path)
    count = 0
    for item in all_files:
        process_file(item, write_directory_path)
        count += 1
        if count % 1000 == 0:
            print('Processed: ', count)

    # merge the unpacked files with the main files
    #destination_unpacked_folder = "/home/c6/Desktop/OpenWPM/jsons/CDX_api/gathered_downloaded_files/fp_date_organized/2018/unpacked"
    #copy_to_all_plus_unpacked(write_directory_path, destination_unpacked_folder)
    ##copy_files(write_directory_path, destination_unpacked_folder)


if __name__ == '__main__':
    main()