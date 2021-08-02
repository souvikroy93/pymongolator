import json
mech_test_list = ['Microhardness', 'Tensile Test', 'TT', 'Fractography', 'Fatigue', 'Crash test', 'Impact test']
atomizatn_list = ['Atomizer', 'Atomization', 'EIGA', 'VIGA']
powder_ch_list = ['Camsizer']


class DataWrapper:
    def __init__(self, input_tuple):
        self.accept_tmp = input_tuple
        self.dict = dict()
        self.temp_list = []
        self.return_dict = dict()

    def wrapper(self):
        'breaks the list and frames the dict for further parsing into JSON format. Schema of variables to be set'
        self.dict = {'material': self.accept_tmp[0], 'operator': self.accept_tmp[1], 'date': self.accept_tmp[2],
                     'type_experiment': self.accept_tmp[3], 'sample_no': self.accept_tmp[4], 'etchant': self.accept_tmp[5], 'etching_time': self.accept_tmp[6],
                     'magnification':self.accept_tmp[7], 'load_microhardness': self.accept_tmp[8], 'din_std':self.accept_tmp[9], 'psd': self.accept_tmp[10],
                     'type_psd':self.accept_tmp[11], 'charge_powder': self.accept_tmp[12], 'lot_powder': self.accept_tmp[13], 'mfg':self.accept_tmp[14],
                     'psd_mfg': self.accept_tmp[15], 'additional_info': self.accept_tmp[16], 'url_archive': self.accept_tmp[17]}

        for keys in self.dict:
            if self.dict[keys] == "":
                self.temp_list.append(keys)

        for item in self.temp_list:
            if item in self.dict:
                self.dict.pop(item)

    def getter(self):
        return self.return_dict

    def parser(self):
        'parses each dictionary based on 1.type of experiment and which collection in DB it should belong to, 2.material, 3.datum itself and returns true for errorless parsing'
        temp_type = ''
        powder_flag = False
        "to make changes in the dict according to the function dataPusher.check_for_data_entrance_db, kind of dict accepted there"
        collec_type = self.dict['type_experiment']
        powder_id = ['type_psd', 'psd', 'psd_mfg', 'charge_powder', 'lot_powder', 'mfg']
        for i in powder_id:
            if i in self.dict.keys():
                powder_flag = True
        if collec_type in atomizatn_list:
            temp_type = 'Atomization'
        elif collec_type in mech_test_list:
            temp_type = 'Mechanical Test'
        elif collec_type in powder_ch_list or powder_flag:
            temp_type = 'Powder Characterization'
        else:
            temp_type = 'LPBF Built Part'
        self.return_dict = {'material': self.dict["material"], "type": temp_type, "datum": self.dict}
        return True
