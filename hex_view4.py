# simple console hex viewer
import sys, os

# get path from command line arguments or via user input"
def get_path_to_file():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = choose_file_name()
    return(path) 

def show_title():
    print(create_line(len(title)))
    print(title)
    print(create_line(len(title)))

# list the names of files in the directory
def show_file_names():
    show_title()
    print("List of files:")
    current_working_directory = os.getcwd()
    list_dir_entries = os.listdir(current_working_directory)
    list_files = list( filter(os.path.isfile,list_dir_entries) )
    list_files.sort()
    length_longest_entry =  len(max(list_files, key=len))
    for number, dir_entry in enumerate(list_files):
        file_size_KB = os.path.getsize(dir_entry) / 1024
        print(f"{number} - {dir_entry:<{length_longest_entry}s} {file_size_KB:>12.2f} KB")
        if (number + 1) % 18 == 0:
            input("Hit <Enter> for more files")
    print("Type <q> to exit\n" + create_line(len(title)))        
    return(list_files)

# let user choose a file by typing it's number or quit the application
def choose_file_name():
    valid_answer = False
    while not valid_answer:
        list_files = show_file_names()
        answer = input("\nWhich file to use?\nType number: ")
        print()
        if answer.isnumeric():
            if -1 < int(answer) < len(list_files):
                file_name_chosen = list_files[int(answer)]
                valid_answer = True
            else:
                print("Invalid answer:",answer)
        elif answer.lower() == "q":
            sys.exit()
        else:
            print("Invalid answer:",answer)
    return(file_name_chosen)

# create a string containing line with (length) characters
def create_line(length):
    line = "=" * length
    return(line)

# print the header above the data
def show_header(path, offset):
    header_txt = f"{'location':<8s}   "
    for column in range(number_bytes):
        header_txt += f"{column:02d}"
        if (column + 1) % 4 == 0:
            header_txt += "  "
        else:
            header_txt += " "
    header_txt += f"|{'as character':^16s}|"
    width = len(header_txt)
    line_txt = create_line(width)
    path_txt = f"File: {path} from location {offset:x} onwards"
    header_txt = f"\n{line_txt}\n{path_txt:^{len(header_txt)}}\n{line_txt}\n{header_txt}\n{line_txt}"
    print(header_txt)
    return(width)

# create a string containing one line of data with position, hex format and character format
def create_one_line_of_data(data_bytes, offset):
    hex_txt = ""
    for column, number in enumerate(data_bytes, start = 1):
        hex_txt += f"{number:02x}"
        if column % 4 == 0:
            hex_txt += "  "
        else:
            hex_txt += " "
    char_txt = ""
    for number in data_bytes:
        ch = chr(number)
        if not ch.isprintable():
            ch = "."
        char_txt += ch
    txt = f"{offset:08x} - {hex_txt:<52s}|{char_txt:<16s}|"
    return(txt)

# print one page of data out of a file
def print_page_of_data(file, width):
    lines_completed = True
    txt = ""
    for _ in range(number_lines):
        offset = file.tell()
        data_bytes = file.read(number_bytes)
        if not data_bytes:
            lines_completed = False
            break
        txt += create_one_line_of_data(data_bytes, offset) + "\n"
    print(txt, end = "")
    print(create_line(width))
    if not lines_completed:
        print("End of file")
    return(lines_completed)

# go though content of a file
def visit_data_of_one_file(path):           
    options="""<Enter> to continue, <j> jump to location, <u> move upwards,
<e> to jump to end of file, <b> jump to beginning of file, <q> to close file """
    with open(path,"rb") as file:
        while True:
            prev_loc = file.tell()
            data_width = show_header(path, prev_loc)
            lines_completed = print_page_of_data(file, data_width)
            answer = input(options).lower().strip()
            match answer:
                case "q":
                    close_file(path)
                    return
                case "e":
                    goto_end(file)
                case "u":
                    move_up(file, prev_loc)
                case "b":
                    file.seek(0)
                case "j":
                    jump_to(file)
                case "":
                    next_page(file, lines_completed, prev_loc)

# close current file
def close_file(path):
    print(f"Closing file {path}\n")

# jump to the last page showing data of file
def goto_end(file):
    loc = -number_lines * number_bytes
    try:
        file.seek(loc, os.SEEK_END)
    except:
        file.seek(0)

# jump to previous page in file
def move_up(file, prev_loc):
    loc = prev_loc - number_lines * number_bytes
    loc = max(0, loc)
    file.seek(loc)

# jump to page of file containing user given offset
def jump_to(file):
    loc_hex = input("location in hex? ")
    try:
        loc = int(loc_hex, base = 16)
    except:
        print(f"Invalid hex location: {loc_hex}")
    else:
        loc = (loc // 16) * 16
        file.seek(loc)

# go to next page of data out of file
def next_page(file, lines_completed, prev_loc):
    if not lines_completed:
        file.seek(prev_loc)


                      
# parameters
number_lines = 21
number_bytes = 16
title = f"{'Simple Hex Viewer':^80s}"

# main loop
while True:
    path = get_path_to_file()
    visit_data_of_one_file(path)


        
        
