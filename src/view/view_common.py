import os

def read_template_file(filename):
    f = os.path.join(os.path.dirname(__file__), '../../res/' + filename)
    return open(f, "r").read()
