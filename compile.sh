#!/bin/sh

# got this trick from http://blog.ablepear.com/2012/10/bundling-python-files-into-stand-alone.html

zip -r kernelstat.zip src/*
echo '#!/usr/bin/env python' | cat - kernelstat.zip > kernelstat
chmod +x kernelstat
rm kernelstat.zip
