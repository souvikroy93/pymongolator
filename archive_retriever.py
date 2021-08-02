import os

# initializing a list of all kinds of data
list_of_formats = ['jpg', 'tif', 'jpeg', 'bmp', '.csv', '.xlsx', '.xls']


class ArchiveGetter:
    def __init__(self, startpath):
        self.startpath = startpath
        self.word_files, self.pdf_files, self.csv_files, self.txt_files, self.ppt_files, self.other_files = [], [], [], [], [], []
        self.image_files = []
        self.return_dict = dict()

    def get_files(self):
        'function to take all files from archive folder and sort them'
        filepaths = []
        for root, dirs, files in os.walk(self.startpath):
            if len(files) != 0:
                filepaths.append([root+"\\"+f for f in files])
        for path_bunch in filepaths:
            for path in path_bunch:
                if path[-4:].lower() == ".tif" or path[-4:].lower() == ".jpg" or path[-4:].lower() == ".bmp" or path[-4:].lower() == ".png" or path[-5:].lower() == ".jpeg":
                    self.image_files.append(path)
                elif path[-5:] == ".docx":
                    self.word_files.append(path)
                elif path[-4:] == ".txt":
                    self.txt_files.append(path)
                elif path[-4:] == ".pdf":
                    self.pdf_files.append(path)
                elif path[-5:] == ".xlsx" or path[-4:] == ".xle" or path[-4:] == ".xld" or path[-4:] == ".xls":
                    self.csv_files.append(path)
                elif path[-5:] == ".pptx":
                    self.ppt_files.append(path)
                else:
                    self.other_files.append(path)
        print('other files : ', self.other_files)
        return {"img": self.image_files, "pdf": self.pdf_files, "csv": self.csv_files, "text": self.txt_files, 'word': self.word_files ,"others": self.other_files}
