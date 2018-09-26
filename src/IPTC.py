#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 16:57:18 2018
This program is part of the Seedy Project by Daniel Dominguez

These functions allow for the rapid writing of IPTC tags for the seedy main file
Assumes that the user is calling in the working directory of the images

@author: julio
"""

import pyexiv2
import datetime


def IPTC_Writer(image_flname,
                descrip,
                digitizer,
                origin, 
                gen,
                email = "NA",
                barcode = "NA",
                spec = "NA",
                herb_url = "NA",
                AOFP_url = "NA"):
    
    
    j = pyexiv2.ImageMetadata(image_flname)
    j.read()
    j['Iptc.Application2.Subject'] = ["Description: " + descrip, "Origin: " + origin, "Genus: " + gen,
     "Species: " + spec, "Barcode: " + barcode , herb_url, "AOFP: " + AOFP_url]
    j['Iptc.Application2.DigitizationDate'] = [datetime.date.today()]
    j['Iptc.Application2.Byline'] = [digitizer]
    j['Iptc.Application2.Headline'] = ["FSU Herbarium Specimen: Plant Seeds- Genus: " + gen + " Spec: " + spec]
    j['Iptc.Application2.Contact'] = [email]
    j.write()


def read_meta(file_name):  #this function takes a list or a string name and prints the metadata
    
    if (type(file_name) == list):
        return_list = []
        for c in file_name:
            J = pyexiv2.ImageMetadata(c)
            J.read()
            sub_list = []
            for x in J.exif_keys:
                print(J[x].value)
                sub_list.append(J[x].value)
            for x in J.iptc_keys:
                print(J[x].value)
                sub_list.append(J[x].value)
            return_list.append(sub_list)
            
    elif (type(file_name) == str):
        return_list = []
        J = pyexiv2.ImageMetadata(file_name)
        J.read()
        sub_list = []
        for x in J.exif_keys:
            print(J[x].value)
            sub_list.append(J[x].value)
        for x in J.iptc_keys:
            print(J[x].value)
            sub_list.append(J[x].value)
        return_list.append(sub_list)
    return return_list
        
        


def img_list():
    images = []
    for file in os.listdir():
        if file.endswith(".jpg"):     #**** Change this to the extensions of the images
            images.append(file)       # in your folder ****
    return(images)



'''
program_description = "Project; SEEDY project by Daniel Dominguez, Open Source python tools for quick digitizing and authoring of HQ Herbarium seed images."
digitiz ="Digitizer: Daniel Dominguez"

herbarium_origin = "Godfrey Herbarium FSU"
herbarium_barcode = "barcode: " + str(12381237123)
genus_species = "genus_species: "
genus = "genus: "
species = "species "
Herbarium_Link = "url"
AOFP_link = "other url"
Contact = "contacnt@email.com"
img_title = 'Agalinis tenuifolia_1.jpg'

IPTC_Writer(program_description, digitizer, date_digitized, herbarium_origin, genus, herbarium_barcode, species, Herbarium_Link, AOFP_link)


	Iptc.Application2.Subject 	String 	No 	Yes 	13 	236   Will hold the info
      	Iptc.Application2.ReleaseDate Date                8
           	Iptc.Application2.DateCreated 	Date 	No 	No 	8 	8
                	Iptc.Application2.DigitizationDate 	Date 	No 	No 	8 	8
                     	Iptc.Application2.Byline 	String 	No 	Yes 	0 	32
                         Iptc.Application2.Headline 	String 	No 	No 	0 	256 synopsis of content
                          	Iptc.Application2.Contact   string                     128
                               	Iptc.Application2.Caption 	String 	No 	No 	0 	2000
                                   
'''