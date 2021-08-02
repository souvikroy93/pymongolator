import base64


def add_image_file(filepath):
    with open(filepath, "rb") as imageFile:
        str_image = base64.b64encode(imageFile.read())

    return str_image


def retrieve_image(binary_str):
    img64_decode = base64.b64decode(binary_str)
    # using local folder path for storing the retrieved image; any other path can also be used
    fh = open("D:\\trial_archive_thesis\\built_part_LPBF\\Light_Optical_Microscopy\\test2_wuerfel_1,2343Mod.jpg", "wb")
    fh.write(img64_decode)


def collected_filepath_receiver(list_of_filpaths):
    list_of_str_imags = []
    for filepath in list_of_filpaths:
        list_of_str_imags.append(add_image_file(filepath))
    return list_of_str_imags
