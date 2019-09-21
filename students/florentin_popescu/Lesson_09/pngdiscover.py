# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:52:09 2019
@author: Florentin Popescu
"""

# imports
import os
import operator as op
# =================================


def get_png(path, ext):
    """
        recursive search for png files
    """
    folder, pngs = [], []

    list(pngs.append(png) if op.and_(png.endswith(ext), op.gt(len(png), 0))
         else folder.extend(get_png("".join((path, "/", png)), ext))
         for png in os.listdir(path))

    folder.append(path)
    return op.iadd(folder, pngs)

# =================================


if __name__ == "__main__":
    list(print(repr(ent)) for ent in get_png(op.add(os.getcwd(), "/data"),
                                             ".png"))
