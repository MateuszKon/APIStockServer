import configparser


class ConfigFile(configparser.ConfigParser):

    def __init__(self, config_path):
        super().__init__()
        self.read(config_path)

    def read_file_defined_by_key(self, section, key):
        """
        Takes path from config file at 'section' and 'key', reads file and return list of lines of the file
        :param section: section name of the config file
        :param key: key name of the selected section of the config file
        :return: all lines of the file as list
        """
        with open(self[section][key]) as f:
            return f.readlines()


if __name__ == "__main__":
    config = ConfigFile("/home/user/Documents/PyCharm/APIStockServer/APIStockServer/config.ini")
    print(config.read_file_defined_by_key("API Keys", "finnhub"))
    print(config.read_file_defined_by_key("API Keys", "goldapi"))
