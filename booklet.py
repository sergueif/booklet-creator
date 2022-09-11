#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A script to rearrange the order of a PDF document so that if
printed in Tabloid style, it reads like a book.

Here is how it works: 
E.g., for a document with 8 pages, this code rearranges the pages to
the following order:
4, 5, 6, 3, 2, 7, 8, 1

@author: ChongChong He, on Nov 19, 2019. Tested with Python 3.6.7 on
macOS. Contact: chongchong@astro.umd.edu

"""

import sys
import os
import math
import numpy as np
from PyPDF2 import PdfFileWriter as Writer, PdfFileReader as Reader

def main(fname):
    """ Input file name; output a rearanged pdf file in the same folder
    The documentation uses a file with 44 pages as an example"""

    orig = Reader(open(fname, 'rb'))
    origpages = orig.pages
    nop = len(origpages)

    # padding
    pages_mod_4 = nop % 4
    if pages_mod_4 > 0:
        pages_to_add = (4 - pages_mod_4) % 4
        pad_file = Writer()
        i = 0
        while i < nop:
            pad_file.addPage(origpages[i])
            i += 1

        pad = 0
        while pad < pages_to_add:
            pad_file.addBlankPage(origpages[0].mediabox.getWidth(), origpages[0].mediabox.getHeight())
            pad += 1


        padded_file = os.path.join(os.path.dirname(fname),
                          os.path.basename(fname) + ".padded.pdf")
        with open(padded_file, 'wb') as f:
            pad_file.write(f)

        orig = Reader(open(padded_file, 'rb'))
        origpages = orig.pages
        nop = len(origpages)

    new = Writer()

    # main thing
    new.addPage(origpages[nop - 1]) # add last page
    pages_moved = 1

    index_up = 0
    index_down = (nop - 1) - 1

    step = 0
    while pages_moved < nop:
        if step == 0 or step == 1:
            new.addPage(origpages[index_up])
            index_up += 1
        elif step == 2 or step == 3:
            new.addPage(origpages[index_down])
            index_down -= 1
        else:
            print("whoa xxxxxxxxx")

        step = (step + 1) % 4
        pages_moved += 1

#    nop_booklet = int(math.ceil(nop / 4.0)) # = 11
#
#    base = np.arange(nop_booklet) + 1
#    base = 2 * base
#    base = base[::-1]
#    pages = []
#    for i in base:
#        num = nop_booklet * 4 + 1 # = 45
#        pages.append(i)
#        pages.append(num - i)
#        pages.append(num - i + 1)
#        pages.append(num - (num - i + 1))
#
#    for i in pages:
#        if i > nop:
#            # new.addBlankPage(origpages[0].mediabox.getWidth(), origpages[0].mediabox.getHeight())
#            new.addBlankPage()
#        else:
#            idx = int(i - 1)
#            new.addPage(origpages[idx])
#
#    # save the modified pdf file
    fn = os.path.join(os.path.dirname(fname),
                      os.path.basename(fname) + ".booklet.pdf")
    with open(fn, 'wb') as f:
        new.write(f)
    print("File saved as {}".format(fn))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python booklet.py path/to/PDF/file \n")
        print("Setups for your printer:")
        print("\t1. Paper size: Tabloid (11*17 in) for academic papers, books, etc;")
        print("\t2. Layout: 2 pages per sheet. Set layout direction to normal 'Z' layout. Set two-sided to Short-Edge binding.")
        print("\t3. Scale to fit the page. An example setup for ARA&A:")
        print("\t\t162% on 11*17 Borderless")
    else:
        main(sys.argv[1])
