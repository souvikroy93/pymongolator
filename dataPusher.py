from pymongo import MongoClient


class DataPusher:
    def __init__(self, input_list, connection_str):
        self._push_list = input_list
        self._conn_str = connection_str
        self._connection = MongoClient(self._conn_str)
        self.success_counter = 0
        self.failure_counter = 0

    def check_for_data_entrance_db(self, element):
        material_name = element['material']
        type_coll = element['type']
        success_flag = False
        collection_flag = False
        db_flag = False
        try:
            for i in self._connection.list_database_names():
                if material_name.lower() == i.lower():
                    #  position = self._connection.list_database_names().index(i)
                    db_flag = True
            if db_flag:
                'if that material database exists, then check collection exists or not'
                for j in self._connection[material_name].list_collection_names():
                    if type_coll.lower() == j.lower():
                        'if collection exists'
                        self._connection[material_name][type_coll].insert_one(element['datum'])
                        collection_flag = True
                        success_flag = True
                if not collection_flag:
                    'if collection not present but material present in mongo'
                    collection_temp = self._connection[material_name][type_coll]
                    collection_temp.insert_one(element['datum'])
                    success_flag = True
            else:
                'if material does not exist on db'
                db = self._connection[material_name]
                collec = db[type_coll]
                collec.insert_one(element['datum'])
                success_flag = True
        except Exception:
            print('exception: ', )
            return False
        else:
            if success_flag:
                return True
            else:
                return False

    def data_receiver(self):
        print('length of push list = ', len(self._push_list))
        for datum in self._push_list:
            if self.check_for_data_entrance_db(datum):
                self.success_counter += 1
            else:
                self.failure_counter += 1
        return self.success_counter, self.failure_counter

    def processer(self):
        return self.data_receiver()