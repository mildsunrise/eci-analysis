import configparser
from io import StringIO
import re

with open('synthDrivers/eloquence/ECI.INI.orig', 'r+') as f:
    conf = configparser.ConfigParser(default_section=False)
    conf.optionxform = str
    conf.read_file(f)
    sections = { k: dict(v) for k, v in conf.items() }
    del sections[False]

    sections = dict(sorted(sections.items()))
    for section in sections.values():
        section['Path'] = 'ENGINE_PATH\\' + re.fullmatch(r'.+?([^\\]+)', section['Path']).group(1)

    conf.clear()
    conf.read_dict(sections)
    conf.write(out := StringIO(), space_around_delimiters=False)
    out = out.getvalue().rstrip() + '\n'
    f.seek(0)
    f.truncate(0)
    f.write(out)
