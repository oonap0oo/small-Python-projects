import sys, os
from PIL import Image, ImageOps

# use the command line argument as directory, if present and valid
def get_directory_from_command_line_args():
    directory = None
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            print(f"Using command line argument {sys.argv[1]}")
            directory = sys.argv[1]
        else:
            print(f"Command line argument {sys.argv[1]} not a valid directory")
    return(directory)

# prompt user for directory using a default
def input_working_directory(default_directory):
    answer_valid = False
    while not answer_valid:
        print(f"Current directory is:\n{default_directory}")
        answer = input("Enter to use the current directory\nor input new path: ")
        if answer == "":
            new_directory = default_directory
            answer_valid = True
        elif os.path.exists(answer):
            new_directory = answer
            answer_valid = True
        else:
            print(f"{answer} is not a valid directory")
    return(new_directory)

# generate list of image file names in the directory
def get_image_files(path, extensions, filter_exclude):
    list_dir_entries = os.listdir(path)
    list_valid_images = []
    for dir_entry in list_dir_entries:
        file_name, extension = os.path.splitext(dir_entry)                
        if (extension.replace(".","") in extensions) and (filter_exclude not in file_name):
            list_valid_images.append(dir_entry)
    return(list_valid_images)

# print the list of iage file names
def print_image_list(image_list):
    length_longest_name = len(max(image_list, key=len))
    print("\nImage files found:")
    for index, image_name in enumerate(image_list, start = 1):
        spacing = length_longest_name + 2 - len(image_name)
        print(image_name, end = " " * spacing)
        if index % 3 == 0:
            print()
    print()


# get image size to be used for resizing, default is provided
def input_new_size(default_size = 1000):
    answer_valid = False
    while not answer_valid:
        print("\nChoose the longest side of the images after resizing")
        print(f"Enter for default value of {default_size} pixels")
        answer = input("Or enter another size: ")
        if answer == "":
            size = default_size
            answer_valid = True
        else:
            try:
                size = int(answer)
            except:
                answer_valid = False
                print(f"{answer} is not a valid size in pixels")
            else:
                answer_valid = True
    print(f"The longest side of the images after resizing will be {size} pixels\n")
    return(size)
    
# open the image file given and return as pillow Image object
def open_image_file(path):  # open the image file and create image object
    with Image.open(path) as image_pillow_object:
        image_pillow_object.load()
    ImageOps.exif_transpose(image_pillow_object, in_place = True) # apply EXIF orientation if necessary
    return(image_pillow_object)

# resize an image, the logest side in pixels is given
def resize_image(image_pillow_object, new_longest_side):
    width_height_ratio = image_pillow_object.width / image_pillow_object.height
    if width_height_ratio > 1:
        new_width = new_longest_side
        new_height = int(new_width / width_height_ratio)
    else:
        new_height = new_longest_side
        new_width = int(new_height * width_height_ratio)
    image_pillow_object_resized = image_pillow_object.resize((new_width, new_height), pillow_resize_filter)
    return(image_pillow_object_resized)
    
# save resized image to a new file
def save_image_file(image_pillow_object, path):
    image_pillow_object.save(path)
    
# parameters
image_file_extentions = ("jpg","jpeg","tif","tiff","png","webp") # supported image file extensions
image_file_resized_addon = "_resized" # txt to be added to file name of resized image file
pillow_resize_filter = Image.Resampling.LANCZOS # filter for resizing Lancos gives best quality

print("Batch Image Resizer")
print("-------------------")

# first use the command line argument if present and valid else prompt user for path
# a default working directory is provided
current_working_directory = get_directory_from_command_line_args()
if current_working_directory == None:
    current_working_directory = input_working_directory(os.getcwd())


# get names of image files and list them
print("\nSupported formats:", *image_file_extentions)
image_files_list = get_image_files(current_working_directory, image_file_extentions, image_file_resized_addon)
if len(image_files_list) == 0:
    print(f"No image files found at {current_working_directory}, terminating")
    quit()
print_image_list(image_files_list)

# get image size to be used for resizing, default is provided
longest_side_after_resize = input_new_size()

# loop through the list with image file names, resize and save them
for image_file_path in image_files_list:
    full_image_file_path = os.path.join(current_working_directory, image_file_path)
    image_pillow_object = open_image_file(full_image_file_path)
    image_resized_pillow_object = resize_image(image_pillow_object, longest_side_after_resize)
    file_name, extension = os.path.splitext(full_image_file_path)
    modified_image_file_path = f"{file_name}{image_file_resized_addon}{extension}"
    print(f"Resized image saving as {modified_image_file_path}")
    save_image_file(image_resized_pillow_object, modified_image_file_path)

    
