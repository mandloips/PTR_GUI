


class Sensors():

    def make_logfile(self):
        ROOT= Path(os.path.expanduser('~'))
        save_dir = ROOT / 'PTR_logs'
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        file_name = name+"-"+str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))+'.json'
        logging.basicConfig(filename=save_dir / file_name,format=' %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger()
    
    def log_data(self):
        json_object = json.dumps(data, indent = 4)
        self.logger.info(json_object)