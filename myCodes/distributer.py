from myCodes import utilities
import os



def distributer():
    all_urls = utilities.read_json("/home/c6/Documents/OpenWPM2/datadir/callable_urls.json")
    out_dir = "/home/c6/Documents/OpenWPM2/datadir/distributed_dataset"
    counter = 0
    counter_name = 1
    splitter = 15000

    while counter != 675000:
        new_list_name = "list" + str(counter_name)
        new_list = all_urls[counter:splitter]
        counter = splitter
        splitter = splitter + 15000
        counter_name += 1
        utilities.write_json(os.path.join(out_dir, new_list_name+".json"), new_list)

    new_list_name = "list" + str(counter_name)
    new_list = all_urls[counter:]
    utilities.write_json(os.path.join(out_dir, new_list_name+".json"), new_list)

    all_sublists = utilities.get_files_in_a_directory(out_dir)
    for file in all_sublists:
        file = utilities.read_json(file)
        print(len(file))


def sanitiser():
    all_urls = utilities.read_json("/home/c6/Documents/OpenWPM2/datadir/callable_urls.json")
    setify = set()
    sub_lists = utilities.get_files_in_a_directory("/home/c6/Documents/OpenWPM2/datadir/distributed_dataset")
    for sublist in sub_lists:
        sublist_content = utilities.read_json(sublist)
        for url in sublist_content:
            setify.add(url)
    print(len(setify))
    print(len(all_urls))


sanitiser()