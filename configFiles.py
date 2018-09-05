__version__ = '0.1'
__author__ = ('David Dunn')

import sys, argparse

def writeModule(object, defaultObj):
    pass

def saveModule(file, string):
    pass

def configDiff(orig, config):
    # not going to look for removed items - that is not the point
    diff = {}
    for k,v in config.__dict__.items():
        if not hasattr(orig, k) or getattr(orig,k) != v:
            diff[k] = v
    return diff

def copyModule(old):
    new = type(old)(old.__name__, old.__doc__)
    new.__dict__.update(old.__dict__)
    for k,v in new.__dict__.items():
        if isinstance(v, dict):
            new.__dict__[k] = copy.copy(v)
    return new

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
