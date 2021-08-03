from src.image_handler_singular import collected_filepath_receiver


def file_sorter(unsorted_list_of_files):
    image_files, word_files, pdf_files, csv_files = [], [], [], []
    for file in unsorted_list_of_files:
        if file[-4:] == ".tif" or file[-4:] == ".jpg" or file[-4:] == ".bmp" or file[-4:] == ".png" or file[-5:] == ".jpeg":
            image_files.append(file)
        elif file[-5:] == ".docx":
            word_files.append(file)
        elif file[-4:] == ".pdf":
            pdf_files.append(file)
        elif file[-5:] == ".xlsx" or file[-4:] == ".xle" or file[-4:] == ".xld":
            csv_files.append(file)
    print(len(image_files))
    'insert code to send different lists to each type of file receiver functions, which prepares them and sends a notice when it is done.'
