# -*- coding: utf-8 -*-
"""
Godfried Search

This module is called Godfried Search, and is the 
base module that will be used to cross reference Godfried Library
aginst known Genus and Species (ideally with barcodes)

Godfried.code() returns the Url to the specimen matching the barcode
Godfried.genu() returns the search page for genus
Godfried.spec() returns the specific search page on which the species begin to appear.

"""
from bs4 import BeautifulSoup
import requests
import re
import webbrowser



def name_parser(name_str, bar ):
    
    if bar == False:
        pattern = r'(\w+)(?:\W*)(\w*\s*\w*\s*\w*\W*$)'  #pull that_gen_spec_barcode
    else: 
        pattern = r'(^\d*)(?:\s*)(\w+)(?:\s*)(\w*\s*\w*\s*\w*\W*$)'
    parse = re.compile(pattern, re.IGNORECASE )
    name = parse.search(name_str)
    
    
    if (bar == False):
        name_obj = ["NA", name.group(1), name.group(2)]
    else: 
        name_obj = [name.group(1), name.group(2), name.group(3)]
    # list[0] = barcode, 1 = genus 2= species
    return name_obj



class Godfrey:  #return urls from sepcimen Data FSU Godfried Herbarium
    #this class will take three potential values barcode, genus, species
    #and fetch and store the right urls
    def __init__(self, genus = 0, species = 0, barcode = 0):
        self.herb_url = "http://herbarium.bio.fsu.edu/"
        self.fsu_url = 'http://herbarium.bio.fsu.edu/search-specimens.php'
        self.add_url = '?search=Search&toggle_showhide=on&CollectionCodeID='
        
        
        if barcode != 0:
            self.code(barcode)
        elif ((genus != 0) & (species != 0)):
            self.quick_genus_species(genus, species)
        elif (genus !=0 & species == 0):
            self.genu(genus)

        
    def code(self, barcd):
        request_url = self.fsu_url + self.add_url
        payload = {'accid': barcd}
        p = requests.post(request_url, params=payload)
        soup = BeautifulSoup(p.content, 'html.parser')
        report_table = soup.find(id = "report_table")
        final_table = report_table.find_next("table")
        
        if final_table.find('a') is not None:
            self.bc_url = self.herb_url + final_table.find('a')['href']
            
    def genu(self, gen_nm):
        request_url = self.fsu_url + self.add_url
        payload = {'taxon_rank_gen': gen_nm}
        p = requests.post(request_url, params=payload)
        p = requests.get(p.url)
        soup = BeautifulSoup(p.content, 'html.parser')
        report_table = soup.find(id = "report_table")
        final_table = report_table.find_next("table")
        self.spec_tag = final_table
            
        self.pg_list = []
        loc_find = soup.find(onchange="location = this.options[this.selectedIndex].value;") #this is the right tag
        for x in loc_find.find_all('option'):
            self.pg_list.append(self.herb_url + x['value'])  # a list of all the links
            
        break_flag = 0    
        
        for x in self.pg_list:
       
            
            temp = requests.get(x)
            temp_soup = BeautifulSoup(temp.content, 'html.parser')
            report_table = temp_soup.find(id = "report_table")
            final_table = report_table.find_next("table")
        
            regex = r'(?<=Species: )\w+\W+\w+'
            prog = re.compile(regex, re.IGNORECASE )
            
            for y in final_table.find_all('a'):
                if break_flag == 1:
                    break
                result = prog.search(y.find('img')['onmouseover'])
                if result != None:
                    j = result.group().split(" ")
                    
                    if break_flag == 0:
                        
                        try:
                            if j[0] == gen_nm:
                                self.gen_url = x
                                #webbrowser.open(self.gen_url)
                                break_flag = 1
                                
                        except IndexError:
                            pass
                        try:
                            if j[1] == gen_nm:
                                self.gen_url = x
                            #webbrowser.open(self.gen_url)
                                break_flag = 1
                        except IndexError:
                            pass
        
        
    
            
    def quick_genus_species(self, genu, specu):
        request_url = self.fsu_url + self.add_url
        plantname = (genu + "+" + specu)
        payload = {'taxon_rank_sp': plantname,"toggle_showhide": "on", "cdat_crit":"=", "cdat2_crit":"=", "sort_by": "gen,sp,isprk,isp" , "output_type": "Thumbnails" }
        p = requests.post(request_url, params=payload)
        self.genspec_url = p.url.replace("%2B", "+")
        
            
            
            
  
   
#aloe = Godfrey("Pinus", "palustris", 0)
#Pinus throws an error because the fist page that we search for a genus is not always just the genus Pinus also gets lupinus
#baisically there are 17 pages that i need to dig through to get the link to the page on which the 
#pinus species begins.


