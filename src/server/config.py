import os, sys

def read_config(file):
    c = {}
    if os.path.exists(file):
        with open(file, 'r') as f:
            p = None
            for line in f.read().split("\n"):
                if line.endswith("\\"):
                    if not p:
                        p = line[0:-1]
                    else:
                        p = p + line[0:-1]
                else:
                    if p:
                        line = p + line
                        p = None
                    if not line.startswith("#") and line.find("=") > -1:
                        i = line.find("=")
                        kv = (line[0:i], line[(i+1):])
                        c[kv[0]] = kv[1]
    return c

def get_config(name="config"):
    v = None
    for k in os.environ.keys():
        if "APP_HOME" == k:
            v = os.environ.get(k) 
    if not v:
        v = os.path.abspath(os.path.join(\
            os.path.dirname(__file__), '..', '..', '..'))
    file = os.path.join(v, 'etc', "%s.properties" % name)
    return read_config(file)

config = get_config('config')
