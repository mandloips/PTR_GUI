import os
from pathlib import Path
import logging
import json
from datetime import datetime

class Datalog():

    def make_logfile(self, name):
        ROOT= Path(os.path.expanduser('~'))
        save_dir = ROOT / 'PTR_logs'
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        file_name = name+"-"+str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))+'.json'
        logging.basicConfig(filename=save_dir / file_name,format=' %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger()
    
    def log_data(self, data):
        json_object = json.dumps(data)
        self.logger.info(json_object)