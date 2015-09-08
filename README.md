findgaps
=========================================

Simple python script to find gaps in a regular series of files

Dependencies
-----------------------------------------
[docopt](https://github.com/docopt/docopt) - just put the docopt.py file in to the repository


Installation
-----------------------------------------

Deliberately not 'packaged' since this is sucha simple script. Just get it and docopt, and then use it.

```
git clone https://github.com/samwisehawkins/findgaps.git
git clone https://github.com/docopt/docopt.git
cp docopt/docopt.py findgaps/
```


Usage
-----------------------------------------
See `find_gaps.py --help`
 
Examples: 

```
python find_gaps.py --chars=18,24 --verbose --date-only --fmt="%y%m%d" --freq=24 GFS_Global_0p5deg_*
```





