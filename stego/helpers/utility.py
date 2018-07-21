# -*- coding: utf-8 -*-
import filetype

def fileformat(filename):
    kind = filetype.guess(filename)
    if kind is None:
        return "Unknown"
    return kind.mime.split("/")[0]
