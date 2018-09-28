#!/usr/bin/env python3

"""labelr by Julio Dominguez
is a script utility for authoring scientific images. Labelr is based off
the image guidlines set by the Atlas Of Florida Plants online database.

This script aims to be both a batch processor and an interactive utility for
use outside of biological systematics.
"""

from optparse import OptionParser
import os
from PIL import Image, ImageDraw, ImageFont
import re
import pyexiv2
import datetime




def main():
    """Handles the parser and calls module functions"""
    imgs = [] # The inital image path list

    # Option Parser 
    #
    usage = "usage: %prog [options] <input> <output_dir>"

    parser = OptionParser(usage=usage)


    parser.add_option("-f", "--file", action="store",type="string", dest="filename",
            help="write report to FILE", metavar="FILENAME")


    parser.add_option("-q", "--quiet",
            action="store_false", dest="verbose",
            default=True,
            help="don't print status messages to stdout")


    parser.add_option("-A", "--author",        # AUTHOR input
            action="store_true", dest="auth",
            default=False,
            help="Prompt the user for author name")



    parser.add_option("-d", "--details", action="store",type="string",
            dest="details_file",
            help="Details for labeling", metavar="detail_file")


    (options, args) = parser.parse_args()


    # make sure that the OUTPUT exist, create folder if not
    #
    try:
        if args[1] is None:
            pass
        elif (os.path.exists(args[1]) == False):
            os.mkdir(args[1])
    except IndexError:
        raise RuntimeError("No output directory specified (check arg2)")


    # make sure images actually exist in INPUT folder
    #
    try:
        imgs = get_imgs(args[0])
    except IndexError:
        raise RuntimeError("No source image or source directory specified:\
Labelr.py --help for help")

    # Start going through the options
    #
    if options.auth:
        AUTHOR = prompt_auth() #Author will be treated as a constant once set.

    # save resized images into new folder
    #
    for img in imgs:
        image_file = size_img(img)

        if options.auth:
            # draw subtitle
            image_file = draw_title(image_file,
                                    os.path.basename(img).split('.')[0],
                                    AUTHOR)
        else:
            image_file = draw_title(image_file, os.path.basename(img).split('.')[0])
        image_file.show()


def prompt_auth():
    author = input("Name of Systematician\n--> ")
    return author

def IPTC_parse(IPTC_path):
    # some file with the proper fields
    IPTC_file = open(IPTC_path, "r")
    IPTC_list = IPTC_file.readlines()
    IPTC_tuple = ("description", "digitizer", "origin", "genus", "email",
                      "barcode", "species", "herb_url", "AOFP_url")
    IPTC_dictionary = { IPTC_tuple[x]:IPTC_list[x] for x in
                      range(len(IPTC_tuple)) }
    return IPTC_dictionary

def IPTC_Writer(image_flname,
                descrip = "NA",
                digitizer = "NA",
                origin = "NA",
                gen = "NA",
                email = "NA",
                barcode = "NA",
                spec = "NA",
                herb_url = "NA",
                AOFP_url = "NA"):

    j = pyexiv2.ImageMetadata(image_flname)
    j.read()
    j['Iptc.Application2.Subject'] = ["Description: " + descrip, "Origin: " + origin, "Genus: " + gen,
     "Species: " + spec, "Barcode: " + barcode , herb_url, "AOFP: " + AOFP_url]
    j['Iptc.Application2.DateCreated'] = [datetime.date.today()]
    j['Iptc.Application2.Byline'] = [digitizer]
    j['Iptc.Application2.Headline'] = ["FSU Herbarium Specimen: Plant Seeds- Genus: " + gen + " Spec: " + spec]
    j['Iptc.Application2.Contact'] = [email]
    j.write()
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


	Iptc.Application2.Subject String No Yes  13  236   Will hold the info
    Iptc.Application2.ReleaseDate Date                8
    Iptc.Application2.DateCreated Date No No 8 8
    Iptc.Application2.DigitizationDate Date  No  No  8 8
    Iptc.Application2.Byline String  No  Yes 0 32
    Iptc.Application2.Headline  String  No  No  0 256 synopsis of content
    Iptc.Application2.Contact   string  128
    Iptc.Application2.Caption String No  No  0 2000

'''


def barcode_parse( s_string, code_pattern = "", regex= None):
    # take a regex as input and ouput the groups
    # can be used to clean and split file name
    DEFAULT_REGEX = r""

    if regex == None:
        pattern = re.compile(DEFAULT_REGEX)
        barcode, filename = pattern.match(s_string)
    else:
        pattern = re.compile(code_pattern)
        barcode, filename = pattern.match(s_string)

    return barcode, filename


def size_img(imPath, ar = "AUTO"):
    """ Returns a resized image based on Aspect Ratio"""

    aspec_ratios = {"square":(650, 550, 1.18), "landscape":(650, 750, .86),
    "portrait":(550, 450, 1.22), "slender":(550, 400, 1.3)}

    def square(imgpath):
        im = Image.open(imgpath)
        width2, height2 = im.size
        width, height = aspec_ratios.get("square")[0:2]
        width_ratio = width / width2
        new_height =int( width_ratio * height2 )
        return im.resize((width, new_height), resample = Image.LANCZOS)
    def landscape(imgpath):
        im = Image.open(imgpath)
        width2, height2 = im.size
        width, height = aspec_ratios.get("landscape")[0:2]
        width_ratio = width / width2
        new_height =int( width_ratio * height2 )
        return im.resize((width, new_height), resample = Image.LANCZOS)
    def slender(imgpath):
        im = Image.open(imgpath)
        width2, height2 = im.size
        width, height = aspec_ratios.get("slender")[0:2]
        width_ratio = width / width2
        new_height =int( width_ratio * height2 )
        return im.resize((width, new_height), resample = Image.LANCZOS)
    def portrait(imgpath):
        im = Image.open(imgpath)
        width2, height2 = im.size
        width, height = aspec_ratios.get("portrait")[0:2]
        width_ratio = width / width2
        new_height =int( width_ratio * height2 )
        return im.resize((width, new_height), resample = Image.LANCZOS)

    def aspect_detect(img_path):
        width, height = Image.open(img_path).size
        aspect_ratio = height / width
        if (aspect_ratio <= 1):
            return landscape(imPath)
        elif (1 < aspect_ratio <= 1.05):
            return square(imPath)
        elif (1.05 < aspect_ratio <= 1.29):
            return portrait(imPath)
        elif (aspect_ratio > 1.29):
            return slender(imPath)

    if ar == "AUTO" :
        return aspect_detect(imPath)
    elif ar == "square":
        return square(imPath)
    elif ar == "landscape":
        return landscape(imPath)
    elif ar == "slender":
        return slender(imPath)
    elif ar == "portrait":
        return portrait(imPath)

def get_imgs(path):
    """ returns list of file paths to images that match the following formats
    or raises an error """
    fmats = ['JPEG', 'BMP', 'PNG', 'TIFF', 'GIF', 'JPEG 2000']
    files_list = []

    # Returns list of path(s)
    #
    if os.path.isdir(path):
        files = os.listdir(path)
        for img_file in files:
            try:
                if Image.open(os.path.join(path, img_file)).format in fmats:
                    files_list.append(os.path.join(path,img_file))
            except OSError:
               pass
        if len(files_list) == 0:
            raise RuntimeError("No images found in source folder")
        return files_list
    elif os.path.isfile(path):
        try:
            if Image.open(img_file).format in fmats:
                return [path]
        except OSError:
            raise RuntimeError("Invalid source image")
    else:
        raise RuntimeError("No valid source image or source directory specified")

def draw_title(image_obj,
               title_string,
               subtitl_str="none",
               fontsize=24,
               subfontsize=14,
               t_italicized=True,
               s_italicized=True,
               fill_color=(15,15,15,225),
               text_color=(255,255,0,255),
               padding=4):

    pencil = ImageDraw.Draw(image_obj) # The pencil draws labels/recs


    if (t_italicized == True): # handles title (required)
        title_font = ImageFont.truetype("../fonts/ariali.ttf", fontsize)
    else:
        title_font = ImageFont.truetype("../fonts/arial.ttf", fontsize)
    xtent, ytent = title_font.getsize(title_string)

    if subtitl_str == "none": # handles subtitle (optional)
        xtent2, ytent2 = (0,0)
    else:
        if (s_italicized == True):
            subtitle_font = ImageFont.truetype("../fonts/ariali.ttf", subfontsize)
        else:
            subtitle_font = ImageFont.truetype("../fonts/arial.ttf", subfontsize)

        xtent2, ytent2 = subtitle_font.getsize(subtitl_str)


    if (xtent > xtent2): # draws the first set of rectangles
        pencil.rectangle([(0,0), (xtent + (2*padding), ytent + padding)],
                         fill=fill_color)
    else:
        pencil.rectangle([(0,0), (xtent2 + (2*padding), ytent + padding)],
                         fill=fill_color)


    if subtitl_str != "none":
        if (xtent > xtent2): # draws the subtitle set of rectangles (optnl)
            pencil.rectangle([(0, ytent), (xtent + (2*padding), ytent +
                            ytent2 + (padding/2) )],
                            fill= fill_color)
        else:
            pencil.rectangle([(0, ytent), (xtent2 + (2*padding), ytent +
                            ytent2 + (padding/2))],
                            fill= fill_color)

    pencil.text((padding, 0), title_string, font=title_font, fill=text_color)

    if subtitl_str != "none":
        pencil.text((padding, ytent), subtitl_str, font=subtitle_font, fill=text_color)

    del pencil
    return image_obj


if __name__ == '__main__':
    main()
