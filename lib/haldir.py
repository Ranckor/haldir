"""main library for the HALDir-Project

"""

import csv
import re
from glob import  glob

ocr_dir = "ocr/"
file_comp_sets = "data/lists.csv"
file_comp_female= "data/female.txt"
file_comp_male= "data/male.txt"
act_year =  0                           #holds actual year given by filename
act_page =  0                           #holds actual year given by filename

### OCR specific procedures ###

def get_ocr_files(ocr_path=ocr_dir):
    "returns a alphabeticaly sorted list of files in given path"

    try:
        ocr_files = sorted(glob(ocr_path + "*ocr*"),key=str.lower)
    except Exception as e:
        print(e)
        print("Verzeichnis {} konnte nicht geöffnet werden".format(ocr_path))
        return

    return ocr_files

def print_ocr_files(ocr_files):
    "prints ocr files"
    i=0
    for ocr_file in ocr_files:
        i += 1
        print("{0:>4}: {1:<20}".format(i,ocr_file))


def get_ocr_lines(ocr_dir):
    """creates filehandle for the given file path, acts as generator
    and returns lines for all ocr files."""

    def set_act_year(ocr_filename):
        year = ocr_filename[5:9]
        print("\n\n---- {} ----\n\n".format(year))
        # TBD - check if year ist a 4 digit number
        act_year = year
    
    def set_act_page(ocr_filename):
        page = ocr_filename[10:14]
        print("\n\n---- Page:  {} ----\n\n".format(page))
        # TBD - check for validity and cut the zeros
        act_page = page

    try:
        for ocr_file in get_ocr_files():
            set_act_year(ocr_file)
            set_act_page(ocr_file)
            with open(ocr_file, 'r') as f:
                for ocr_line in f:
                    ocr_line = ocr_line.rstrip()
                    yield ocr_line
    
    except Exception as e:
        print(e)
        print("OCR-Datei {} konnte nicht geöffnet werden".format(ocr_file))
        return

def print_ocr_lines():
    "prints lines of all ocr files"

    for line in get_ocr_lines(ocr_dir):
        print(line)

def get_csv_rows():
    "Method parses ocr_lines as csv data and acts as generator, returns actual row"
    
    csv_reader = csv.reader(get_ocr_lines(ocr_dir),delimiter=',')
    for row in csv_reader:
        yield row




### importing sets for comparision ###

#main set from chris
def build_comp_sets(path=file_comp_sets):
    "Builds sets out of csv file. Needed for comparison."

    comp_sets = { 
        "streets" :       set([]),
        "names" :         set([]),
        "fnames" :        set([]),
        "names_add" :     set([]),
        "stores_assoc" :  set([]),
        "heirs" :         set([]),
        "cooporations" :  set([]),
        "siblings" :      set([]),
        "professions" :   set([]),
        "titles" :        set([]),
        "medals" :        set([]),
        "cities" :        set([]),
        "add_chars" :     set([]),
        "double_means" :  set([]) 
    }

    try:
        with open(path, 'r') as f_lists:
            csv_reader = csv.reader(f_lists,delimiter=';')
            for row in csv_reader:
                if len(row[0]) > 0:
                    comp_sets["streets"].add(row[0])
                if len(row[1]) > 0:
                    comp_sets["names"].add(row[1])
                if len(row[2]) > 0:
                    comp_sets["fnames"].add(row[2])
                if len(row[3]) > 0:
                    comp_sets["names_add"].add(row[3])
                if len(row[4]) > 0:
                    comp_sets["stores_assoc"].add(row[4])
                if len(row[5]) > 0:
                    comp_sets["heirs"].add(row[5])
                if len(row[6]) > 0:
                    comp_sets["cooporations"].add(row[6])
                if len(row[7]) > 0:
                    comp_sets["siblings"].add(row[7])
                if len(row[8]) > 0:
                    comp_sets["professions"].add(row[8])
                if len(row[9]) > 0:
                    comp_sets["titles"].add(row[9])
                if len(row[10]) > 0:
                    comp_sets["medals"].add(row[10])
                if len(row[11]) > 0:
                    comp_sets["cities"].add(row[11])
                if len(row[12]) > 0:
                    comp_sets["add_chars"].add(row[12])
                if len(row[13]) > 0:
                    comp_sets["double_means"].add(row[13])

    except Exception as e:
        print(e)
        print("LISTS-Datei {} konnte nicht geöffnet werden".format(path))

    return comp_sets


# sets needed for identifying sex

def build_male_set(malepath=file_comp_male,femalepath=file_comp_female):
    """ Builds a set out of male names and returns the set. Needed for identifying
        sex"""

    try:
        comp_male_set = set()
        comp_female_set = set()

        with open(malepath, 'r') as f_lists:
            for line in f_lists:
                comp_male_set.add(line.strip()) 

        with open(femalepath, 'r') as f_lists:
            for line in f_lists:
                comp_female_set.add(line.strip()) 

    except Exception as e:
        print(e)
        print("Die Dateien {} konnten nicht geöffnet werden".format(path))

    return (comp_male_set, comp_female_set)




#TBD BETA
def is_new_row(row,comp_sets):
    """ Function takes a raw csv-row and checks if this is the beginning of
        a new data set """
    
    re_names = re.compile(r"^-\s.*")
    # a line with "-" at the beginning
    
    try:

        if row[0] in comp_sets["names"]:
            print(row[0], "exisits in lists")
            return True
        elif re.search(re_names,row[0]):
            print(row[0], "exisits in lists")
            return True
        else:
            return False

    except Exception as e:
        print(e)
        print("Probleme bei der Zeilenprüfung: neue Zeile")

#TBD BETA
def assemble_lines(comp_sets):

    temp_row    = []
    fin_row     = []
    proceeded = 0
    try:
        for act_row in get_csv_rows():
            proceeded += 1
            print("Zeile: ", proceeded)
            #print(act_row)
            
            if is_new_row(act_row,comp_sets):
                #tbd temp_row_zusammenfügen
                if len(temp_row) > 0:
                    fin_row += temp_row
                    print("\n\nFINAL::",fin_row, "\n-----\n")
                    temp_row = []
                    fin_row = []

                temp_row.append(act_row)
                print(len(temp_row))
                #print(temp_row[i])

            else:
                temp_row.append(act_row)


    except Exception as e:
        print(e)
        print("Probleme beim Zusammenfügen der Zeilen")

