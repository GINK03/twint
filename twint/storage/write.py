from . import write_meta as meta
import csv
import json
import os
import gzip
def outputExt(objType, fType):
    if objType == "str":
        objType = "username"
    outExt = f"/{objType}s.{fType}"

    return outExt

def addExt(base, objType, fType):
    if len(base.split('.')) == 1:
        createDirIfMissing(base)
        base += outputExt(objType, fType)

    return base

def Text(entry, f):
    print(entry.replace('\n', ' '), file=open(f, "a", encoding="utf-8"))

def Type(config):
    if config.User_full:
        _type = "user"
    elif config.Followers or config.Following:
        _type = "username"
    else:
        _type = "tweet"

    return _type

def struct(obj, custom, _type):
    if custom:
        fieldnames = custom
        row = {}
        for f in fieldnames:
            row[f] = meta.Data(obj, _type)[f]
    else:
        fieldnames = meta.Fieldnames(_type)
        row = meta.Data(obj, _type)

    return fieldnames, row

def createDirIfMissing(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

from urllib.parse import urlparse
from hashlib import sha224
from pathlib import Path
import json
from os import environ as E
HOME = E.get("HOME")
def Json(obj, config):
    if not isinstance(obj, dict):
        _obj_type = obj.__class__.__name__
        if _obj_type == "str":
            _obj_type = "username"
        null, data = struct(obj, config.Custom[_obj_type], _obj_type)

        # base = addExt(config.Output, _obj_type, "json")
        base = config.Output
        # print(__file__, "InJson", base, data["link"], data)
        """
        cacheのために書き込み
        """
        url = data["link"]
        parse = urlparse(url)._replace(query='').geturl()
        digest = sha224(bytes(parse, "utf8")).hexdigest()

        with open(f"{HOME}/.mnt/cache/twinbee/{digest}", "wb") as fp:
            ser = gzip.compress(bytes(json.dumps(data,ensure_ascii=False), "utf8"))
            fp.write(ser)

        with open(base, "a", newline='', encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False)
            json_file.write("\n")
    else:
        base = config.Output
        obj["CacheHit"] = "True"
        with open(base, "a", newline='', encoding="utf-8") as json_file:
            json.dump(obj, json_file, ensure_ascii=False)
            json_file.write("\n")

