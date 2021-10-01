import plyvel
import os
import sqlite3 as lite
from myCodes import utilities
from pathlib import Path
from bs4 import BeautifulSoup as bs
import hashlib

## connect to sqlite DB
# connect to the output database
openwpm_db = '/home/c6/Documents/OpenWPM2/datadir/crawl-data.sqlite'
conn = lite.connect(openwpm_db)
cur = conn.cursor()
# collect hash of each script
hash_list = []
for hash_code in cur.execute("SELECT content_hash FROM http_responses;"):
    if str(hash_code[0]) != 'None':
        hash_list.append(hash_code[0])

base_directory = '/home/c6/Documents/OpenWPM2/datadir'
# Connect to content database
ldb = plyvel.DB(os.path.join(base_directory, 'content.ldb'))

### ldb test
for hash_code in hash_list:
    script_raw_text =ldb.get(str.encode(hash_code))
    script_text = str(script_raw_text, "utf-8")

    if script_text is not None:
        if script_text.startswith("<!DOCTYPE"):
            utilities.write_full_file(os.path.join("/home/c6/Documents/OpenWPM2/datadir/htmls", hash_code + ".html"), script_text)
        else:
            utilities.write_full_file(os.path.join("/home/c6/Documents/OpenWPM2/datadir/inline_js", hash_code +".js"), script_text)

### extract inline scripts
html_files = utilities.get_files_in_a_directory("/home/c6/Documents/OpenWPM2/datadir/htmls")
for html_file in html_files:
    html = utilities.read_full_file(html_file)
    # parse HTML using beautiful soup
    soup = bs(html, "html.parser")

    # get the JavaScript files
    script_urls = []
    inline_scripts = []
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            pass
        else:
            hash_code = hashlib.md5(script.string.encode()).hexdigest()
            utilities.write_full_file(os.path.join("/home/c6/Documents/OpenWPM2/datadir/inline_js", hash_code + ".js"),
                                      script.string)


