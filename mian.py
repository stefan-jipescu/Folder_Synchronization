import os, filecmp, shutil
class file_in_folder:
    def __init__(self,folder_path) -> None:
        self.folder_path = folder_path
        self.file_list = os.listdir(self.folder_path)
    def files(self):
        return os.listdir(self.folder_path)


class file_management():
    def __init__(self, source_path, replica_path,source_files_list, replica_files_list) -> None:
        self.source_path = source_path
        self.replica_path = replica_path
        self.source_files_list = source_files_list
        self.replica_files_list = replica_files_list

    def compare(self):
        self.match, self.mismatch, self.errors = filecmp.cmpfiles(self.source_path, self.replica_path,self.source_files_list)
        print(f'match : {self.match}')
        print(f'mismatch : {self.mismatch}')
        print(f'errors : {self.errors}')
    def add_file(self):
        for f in (self.errors + self.mismatch):
            temp_path = os.path.join(self.source_path, f)
            shutil.copy2(temp_path, self.replica_path)

    def del_file(self):
        for f in ([x for x in self.replica_files_list if x not in self.source_files_list] + self.mismatch):
            temp_path = os.path.join(self.replica_path, f)
            os.remove(temp_path)


def main(): 
    node1 = file_in_folder('./source').files()
    node2 = file_in_folder('./replica').files()
    node = file_management('./source', './replica', node1,node2)
    node.compare()
    node.del_file()
    node.add_file()

if __name__ =="__main__": 
    main()