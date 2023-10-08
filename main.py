import os, filecmp, shutil, schedule, time, logging

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

    def add_file(self):
        for f in (self.errors + self.mismatch):
            temp_path = os.path.join(self.source_path, f)
            if os.path.isdir(temp_path):
                shutil.copytree(temp_path, os.path.join(self.replica_path, f))
                logging.debug(f"{f} folder was added on {self.replica_path}")
            else:
                shutil.copy2(temp_path, self.replica_path)
                logging.debug(f"{f} file was added on {self.replica_path}")

    def del_file(self):
        for f in ([x for x in self.replica_files_list if x not in self.source_files_list] + self.mismatch):
            temp_path = os.path.join(self.replica_path, f)
            if os.path.isdir(temp_path):
                shutil.rmtree(temp_path)
                logging.debug(f"{f} folder was deleted from {self.replica_path}")
            else:
                os.remove(temp_path)
                logging.debug(f"{f} file was deleted from {self.replica_path}")
            


def sync_process(path_1, path_2):
    node1 = file_in_folder(path_1).files()
    node2 = file_in_folder(path_2).files()
    for f in node1:
        if f in node2 and os.path.isdir(os.path.join(path_1, f)):
            node1.remove(f)
            node2.remove(f)
            sync_process(os.path.join(path_1, f), os.path.join(path_2, f))
    node = file_management(path_1, path_2, node1,node2)
    node.compare()
    node.del_file()
    node.add_file()

def log_(log_name):
    logging.basicConfig(filename= log_name, level=logging.DEBUG, format="%(asctime)s %(message)s")

def main():
    source = input("Please insert the source folder path: ")
    clone = input("Please insert the clone folder path: ")
    log_name = input("Please insert the log file name: ")
    log_(log_name)
    period = input('How often do you want to proceed the synchronization? ')
    period_scale = input('What time scale do you prefer for the synchronization? (seconds/ minutes/ hour) ')

    try: 
        int(period)
    except ValueError:
        logging.exception(f'The {period} value is not an integer')
        print(f'The {period} value is not an integer')
        return

    if not (os.path.isdir(source) and os.path.isdir(clone)):
        logging.exception('The source or replica folder file do not exist')
        print('The source or replica folder file do not exist')
        return
    
    if period_scale == "seconds":
        schedule.every(int(period)).seconds.do(sync_process, path_1 = source, path_2 = clone)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif period_scale == "minutes":
        schedule.every(int(period)).minutes.do(sync_process, path_1 = source, path_2 = clone)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif period_scale == "hour":
        schedule.every(int(period)).hour.do(sync_process, path_1 = source, path_2 = clone)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        logging.debug(f'The {period_scale} is not a valid type')
        print(f'The {period_scale} is not a valid type')
        return
    
if __name__ =="__main__": 
    main()