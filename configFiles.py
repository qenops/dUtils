__version__ = '0.1'
__author__ = ('David Dunn')

import sys, argparse

def writeModule(object, defaultObj):
    pass

def saveModule(file, string):
    pass

def loadDict(configDict):
    config = type('', (), {})()
    for k,v in configDict.items():
        setattr(config, k, v)
    return config

def loadModule(file, name='config'):
    if sys.version_info[0] == 3:
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    elif sys.version_info[0] == 2:
        import imp
        module = imp.load_source(name,file)
    return module
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--var', nargs='*', action='append', help='A varaible and value pair')
    args = parser.parse_args()
    config = loadModule('config.py')
    if args.var:
        for var in args.var:
            dtype = type(getattr(config, var[0]))
            if len(var) == 2:
                setattr(config, var[0], dtype(var[1]))
