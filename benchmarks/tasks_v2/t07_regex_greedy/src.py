import re

def extract_tags(s):
    return re.findall(r"\[(.+)\]", s)
