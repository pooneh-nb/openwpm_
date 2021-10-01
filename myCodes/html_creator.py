import os
import shutil
from pathlib import Path
from myCodes import utilities
import re
import multiprocessing
from multiprocessing import Pool as ThreadPool


def find_packed_js(script, packed_html_dir, packed_dir):
    file_name = script.split('/')[-1]
    #print(file_name)
    if os.stat(script).st_size != 0:
        script_text = utilities.read_full_file(script)
        try:
            if '<!DOCTYPE html>\n<html' in script_text or '<!DOCTYPE html><html' in script_text:
                html_files = os.path.join(packed_html_dir, file_name + '.html')
                utilities.write_content(html_files, script_text)
                shutil.move(script, packed_dir)
                return

            if "eval(" in script_text or "Function(" in script_text:
                #print("yep")
            #if re.match("(Function\(\w+)", script_text) or re.match("(eval\(\w+)", script_text):
                shutil.move(script, packed_dir)
                utilities.write_content(os.path.join(packed_html_dir + '/unpacked_js/', file_name + '.js'), script_text)
                #print("done")
                js_file = "http://0.0.0.0:8000/unpacked_js/" + file_name + '.js'
                html_text = """<!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <title>Title</title>
                </head>
                <body>
                <script src='""" + js_file + """'></script>
                </body>
                </html>"""
                html_files = os.path.join(packed_html_dir, file_name + '.html')
                utilities.write_content(html_files, html_text)
        except Exception as ex:
            #print("text", script_text)
            print("Exception", ex)
    else:
        print("text empty")


def main():

    raw_js_dir = "/home/c6/Documents/OpenWPM2/datadir/inline_js"
    raw_js_files = utilities.get_files_in_a_directory(raw_js_dir)
    packed_dir = "/home/c6/Documents/OpenWPM2/datadir/inline_js/packed"
    packed_html_dir = "/home/c6/Documents/OpenWPM2/datadir/inline_js/unpacking/packed_html_files"

    if not os.path.exists(packed_html_dir):
        os.makedirs(packed_html_dir)
    for script in raw_js_files:
        find_packed_js(script, packed_html_dir, packed_dir)



if __name__ == '__main__':
    main()
