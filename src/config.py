import configparser

import os

class DynamicConfig:
    def __init__(self, conf):
        if not isinstance(conf, dict):
            raise TypeError(f'dict expected, found {type(conf).__name__}')

        self._raw = conf
        for key, value in self._raw.items():
            setattr(self, key, value)

class DynamicConfigIni:
    def __init__(self):
        #if not isinstance(conf, configparser.ConfigParser):
        #    raise TypeError(f'ConfigParser expected, found {type(conf).__name__}')
        cwd = os.getcwd()
        print(cwd)
        conf = configparser.ConfigParser()

        conf.read('moreheat.ini')

        #print(config.sections())
        #print(config['DEFAULT']['alice_outdoorweight'])
        #print(config['DEFAULT']['bob_outdoorweight'])

        #for key in config['DEFAULT']:  
        #    print(key)


        #parser = configparser.ConfigParser()
        #parser.read_file(open('config.ini'))
        
        #config = DynamicConfigIni(parser)

        #print('server:', config.server.host, config.server.port, config.server.timeout)
        #print('user:', config.user.username, config.user.level)

        self._raw = conf
        for key, value in self._raw.items():
            setattr(self, key, DynamicConfig(dict(value.items())))
