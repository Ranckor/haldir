#!/usr/bin/env python3

import sys
sys.path[0] = sys.path[0] + "/lib/"

import haldir as hd

#generate lists for comparisions
comp_sets = hd.build_comp_sets()

#generate sets for identifying sex
male_set, female_set = hd.build_male_set()



#### test and fix ####

#print(comp_sets["medals"])
#print(male_set)
#print(type(male_set))

#print(female_set)
#print(type(female_set))
#print all lines of all ocr files
hd.print_ocr_lines()

#hd.print_ocr_files(hd.get_ocr_files())

#print(hd.act_year)

#for i in hd.get_csv_rows():
#    print(i)







