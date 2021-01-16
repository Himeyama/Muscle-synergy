import numpy as np
import os
import csv
import glob
import filter

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


def preparation(emg, f, hiparams=(10, 3, 3, 10), lowparams=(15, 22, 3, 10)):
    emg = filter.highpass(emg, f, *hiparams)
    emg = np.abs(emg)
    emg = filter.lowpass(emg, f, *lowparams)
    emg[emg < 0] = 0
    return emg


def pMat(Es, f=1925.926):
    ss = np.zeros(Es.shape)
    _, m_size, t_size = Es.shape
    for i, session in enumerate(ss):
        ms = np.zeros((m_size, t_size))
        for m in range(m_size):
            emg = Es[i][m]
            ms[m] = preparation(emg, f)
        ss[i] = ms
    return ss


def max(Es):
    maxE = np.zeros(Es.shape[2])
    for i, m in enumerate(Es.T):
        maxE[i] = np.max(m)
    return maxE
