# DiogenesList

DiogenesList is a multiplatform CLI-only clone of [Snap2HTML](http://www.rlvision.com/snap2html/about.php). I created it because I needed to use Snap2HTML on Linux but didn't want to have to install WINE. Also because I wanted to make it possible to use it on a headless machine, so that's why there is no GUI 

It's purpose is to create single page HTML+Javascript browsable lists of the contents of a given directory

## Usage
The program only takes two arguments, the directory to be indexed and the output file name without the extension, so:

 *diogeneslist.py /home/user filelist*
 
Will index the contents of /home/user and save them to filelist.html on the current directory. Simple as that


## License
The diogeneslist.py file is licensed under GPLv2

The template.html file is taken directly from Snap2HTML an thus is licensed as freeware
