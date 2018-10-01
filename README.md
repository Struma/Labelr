# Labelr
Labelr is an interactive script utility for batch authoring scientific images for upload to databases. The standard utility is modeled off of the Atlas of Florida Plants image standards.

<p align="center">
  <img src="https://raw.githubusercontent.com/Struma/Labelr/master/ref/Seed_example.png" alt="example_imgs"/>
  
</p>
<p align="center"> Fig 1. The above images are generated from this script. </p>

How to install
------
Install with Pip! 

1. download this directory `git clone https://github.com/Struma/Labelr.git ~/.labelr` this directory
2.  
 




AOFP Image Labeling Guidlines
------

The file that outlines the AOFP standards are available ->
[here](https://github.com/Struma/Labelr/blob/master/ref/Live%20plant%20photo%20instructions%20for%20the%20Atlas.doc) <- and are summarized as follows.

* Images must be 72ppi Jpegs
* Aspect Ratios must conform to these pixel dimesions
  1. 750-650 for landscape
  2. 650-550 for square
  3. 550-450 for portrait
  4. 400-300 for slender *this format is too small and superflous*
  e* 
* Text is to be formatted in Times New Roman, Bold italics, and Pure yellow 0xFFFF00
* Taxon name ex.(Genus species) in 24pt font
* Author name ex.(Photo by John Doe) in 14pt font
* Name of final image file formatted as ex.(genus_species.jpg) in snake case

Script Utility goals/asperations
------
* Interactive or batch processing power
* Support for Information Interchange Model (IPTC) Metada labeling
* Automatic archiving
* output logging
* folder scanning
* file conversion
* comply with PEP 8

