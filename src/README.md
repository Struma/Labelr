# Source files

This directory contains all the source files for labelr.

## Main files

* **Labelr.py** - Main file (will be renamed labelr.py soon)
* **../fonts/** - Font files for PIL
* **../sample_imgs/** - test files

## Basic Usage

Labelr.py is a conventional script file that requires 2 arguments.

`Labrlr.py    arg1    arg2`

1. argument1 is a path string to an image file or directory containing image files.
   * will throw an error if no compatible image files are found (compatible with all PIL supported formats)

2. argument2 is a path string to an output folder (will be created if it doesn't exist.)

## Installation

Pull the library to a directory where you don't mind it hanging out. 

`git pull Struma/labelr.git`

If you type `$PATH` in bash it will show you what directories the shell searches for program files (by default). The PATH variable is what makes it possible to type a program name without any breadcrumb. 
Therefore, if X is in PATH, typing `X` in bash is equivelinet to typing `/usr/bin/X` -which is how you execute a file in most shells.

Running the install script moves a small helper script into a path directory and allows you to call labelr from the command line.

### **Under Construnction**

You will soon be able to run the install.sh script and I can use bash to pass off argv[0] to the python script
