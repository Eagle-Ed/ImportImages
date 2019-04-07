#!/usr/bin/env python
__author__ = 'Edi Layritz'


import os
import sys
from os import walk
import re
import exifread

# ~ in_dir = 'l:\Bilder und Film\_Eusi'
title_start_nr = 400
in_dir = 'd:\Meins\Bilder'

def list_dir_only(in_dir):
    # ~ lists all title dirs (no subdris within a title e.g. CaptureOne, Panxx)
    dirlist = []
    temp_dirlist = []
    for (dirpath, dirnames, filenames) in walk(in_dir):
        if os.path.isdir(dirpath):
            temp_dirlist.append(dirpath)
            print 'dirpath:', dirpath
    for dirs in temp_dirlist:
        found = re.search('(.*20\d{2}-\d{2}-\d{2}(\w|\s|-)+)$',dirs)
        if found:
            additional_dir = found.group(1)
            dirlist.append(additional_dir)
    return dirlist


def find_first_last_pic(file_path):
    filelist = []
    for (dirpath, dirnames, filenames) in walk(file_path):
        for my_file in filenames:
            search_string = '.*\.jpe?g$'
            found_jpg = re.search(search_string, my_file, re.IGNORECASE)
            if found_jpg:
                print 'JPG only: ', my_file
                filelist.append(my_file)
        break  # prevent walk from diving into the 


    n = len(filelist)
    print 'filelist hat ', n, 'Eintraege'
    if n > 0:
        first_picture = filelist[0]
        last_picture = filelist[-1]
    else:
        first_picture = ''
        last_picture = ''
    return first_picture, last_picture

def create_title_list(file_path, title_id):
    # ~ vars
    start_date = 'none'
    end_date = 'none'
    title = 'none'
    
    # ~ search the "Bis" date
    first_pic, last_pic = find_first_last_pic(file_path)
    # ~ start_date = read_picture_date (first_pic)
    if last_pic == '':
        end_date = 'keine Bilder'
    else:
        last_pic = file_path + '\\' + last_pic
        end_date = read_picture_date(last_pic)
    
    # ~ Search the "Von" date and the Title
    found = re.search('.*(20\d{2}-\d{2}-\d{2})\W(.*)', file_path)
    if found:
        start_date = found.group(1)
        title = found.group(2)

    print start_date + ';' + end_date + ';' + title + ';' + file_path + ';' + str(title_id)
    title_ine = start_date + ';' + end_date + ';' + title + ';' + file_path + ';' + str(title_id) + '\n'
    return title_ine
    
def read_picture_date(picture):
    f = open(picture, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)
    picture_date_time = tags.get('Image DateTime')
    picture_date_time = str(picture_date_time)
    picture_date = (picture_date_time.split()[0]).replace(":", "-")
    f.close
    return picture_date
    
    
def main():
    out_file = in_dir + '\\title_list.csv'
    file_main = open(out_file,"w")
    dir_list = list_dir_only(in_dir)
    title_id = title_start_nr
    for file_path in dir_list:
        title_line = create_title_list(file_path, title_id)
        file_main.write(title_line)
        title_id += 1
    file_main.close()


if __name__ == '__main__':
    main()
