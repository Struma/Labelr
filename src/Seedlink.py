#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 02:58:04 2018
This is the main project script that pulls from other sources to do the work.
@author: julio
"""

import re  
import os
from PIL import Image, ImageDraw, ImageFont
os.chdir("/home/julio/Projects/Seed_ID_program/Seedlink/")
import IPTC
import godfrey


#Settings for the user 
description = "SeedLink project by Daniel Dominguez, Open Source python tools for quick digitizing and authoring of HQ Herbarium seed images."
digitizer = "Daniel Dominguez"
origin = "FSU Godfrey Herbarium"
emailer = "djd10d@my.fsu.edu"
bar_flag = True  #is there a barcode included?
home = "/home/julio/Projects/Seed_images/Test/"

#make sure we are in the right directory
os.chdir(home)
#lets put all the images from this directory into a list (mine were tifs)
images = []
for file in os.listdir(home):
    if file.endswith(".jpg"):     #**** Change this to the extensions of the images
        images.append(file)       # in your folder ****

#iterate through the list
for pic in images:
    
    #My file names were in the format   "fig2a Genus species.tif","Fig2ef Genus species.tif"
    # "fig4 Genus species.tif", "Fig6cd Genus species.tif", ect.....
    # We use the power of regular expressions and regular labeling to extract just the
    # Genus and species.
    pattern = r'(\d*)[abcdefgh]*\S* (.*)(?=.jpg)'  #this will be particular to your img set
    parse = re.compile(pattern)
    name = parse.search(pic)
    name_string = name.group(2)
    full_name = name.group(0)

    #now we need to resize the image to AOFP guidlines (750px Wide)
    im = Image.open(pic)
    bbox = im.getbbox()
    width = 750
    height = int(bbox[3] * (width/bbox[2]))
    im = im.resize((width, height), resample = Image.BICUBIC)
    
    #My images were in figure format, some needed to be split.
    #uncomment and indent the line "split_list.append(im)" four spaces.
    split_list = []
    if im.getbbox()[3] > width:
        height = im.getbbox()[3]
        split = int(height / 2)
        im1 = im.crop(box = (0,0,width, split))
        im2 = im.crop(box = (0, split, width, height))
        split_list.append(im1)
        split_list.append(im2)
    else:
        split_list.append(im)

    #Draw all the elements on the image formatted to AOFP guidlines
    for x in split_list: 
        draw = ImageDraw.Draw(x)
        font = ImageFont.truetype("ariali.ttf", 24) #AOFP says 24
        sub = ImageFont.truetype("ariali.ttf", 14)  #AOFP says 14

        auth = "Photo by Daniel Dominguez"          #**change to the collectors name**
        xtent, ytent = font.getsize(name_string)
        xtent2, ytent2 = sub.getsize(auth)

        small = 4                       #the small indents of both text strings
        
        if (xtent > xtent2):
            draw.rectangle([(0, 0), (xtent + small, ytent)], fill = (15,15,15,225)) #draws the rectangle
            draw.rectangle([(0, ytent), (xtent + small, ytent2 + ytent)], fill = (15,15,15,225)) 
        else :
            draw.rectangle([(0, 0), (xtent2 + small, ytent)], fill = (15,15,15,225)) #draws the rectangle
            draw.rectangle([(0, ytent), (xtent2 + small, ytent2 + ytent)], fill = (15,15,15,225))
        #draws the labels
        draw.text((small, 0), name_string, font=font, fill=(255,255,0,225))
        draw.text((small, ytent), auth, font=sub, fill=(255,255,0,225))

        #clean up 
        del draw
        # write to file
        ind = split_list.index(x) + 1
        #save as JPEG
        jpgname = name_string + "_" + str(ind) + ".jpg"
        jpgpath = home + "OUTPUT/" + jpgname
        x.save(jpgpath , "JPEG") 
        parsed_name = name_parser(full_name, bar_flag)
        print(parsed_name)
        if (parsed_name[2] != ("sp." or "sp")):
            print("full_on_name")
            a = Godfrey(parsed_name[1], parsed_name[2])
            os.chdir("OUTPUT")   #jump to that folder
            IPTC_Writer(jpgname,  #Write the metadata
                description,
                digitizer,
                origin, 
                parsed_name[1],
                emailer,
                parsed_name[0],
                parsed_name[2],
                a.genspec_url,     #This needs to be a barcode url if it exist
                "NA"
                )
            os.chdir(home) #Jump back to the image folder
        else: 
            a = Godfrey(parsed_name[1])
            print("half_name")
        
            os.chdir("OUTPUT")   #jump to that folder
            IPTC_Writer(jpgname,  #Write the metadata
                    description,
                    digitizer,
                    origin, 
                    parsed_name[1],
                    emailer,
                    "N/a",
                    parsed_name[2],
                    a.gen_url,
                    "NA"
                    )
            os.chdir(home) #Jump back to the image folder
        





