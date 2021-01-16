import numpy as np
import os
import csv
import glob


def load(filename):
    basename = os.path.basename(filename).split(".", 1)[0]
    dirname = os.path.dirname(filename)
    npy_dirname = f"{dirname}/.npy"
    npy_filename = f"{npy_dirname}/{basename}.npy"
    if not os.path.isdir(npy_dirname):
        os.makedirs(npy_dirname)
    a = None
    if not os.path.isfile(npy_filename):
        with open(filename, encoding="cp932", newline="\r\n") as f:
            reader = csv.reader(f)
            a = np.array(list(map(lambda x: list(map(float, x)), list(reader)[117:]))).T[1:]
        np.save(npy_filename, a)
    else:
        a = np.load(npy_filename)
    return a


def get(dirname):
    emgfiles = glob.glob(f"{dirname}/*.csv")
    a = None
    for emgfile in emgfiles:
        a = load(emgfile)
        break
    Es = np.zeros((len(emgfiles), a.shape[0], a.shape[1]))
    for i, emgfile in enumerate(emgfiles):
        Es[i] = load(emgfile)
    return Es


def done(text=None):
    if text is not None:
        print(f"\x1b[32m{text} [完了]\x1b[0m")
    else:
        print(f"\x1b[32m完了\x1b[0m")
