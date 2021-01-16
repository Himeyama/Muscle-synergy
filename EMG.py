import numpy as np
import os
import csv
import glob
import filter
import matplotlib.pyplot as plt


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
    maxE = np.zeros(Es.shape[1])
    for i, m in enumerate(Es):
        maxE[i] = np.max(m)
    return maxE


def plot_synergy(W):
    plt.rcParams["font.family"] = "Noto Sans CJK JP"
    colors = ["#f44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#2196F3", 
            "#03A9F4", "#00BCD4", "#009688", "#4CAF50", "#8BC34A", "#CDDC39",
            "#FFEB3B", "#FFC107", "#FF9800", "#FF5722"]
    muscle_names = ["前脛骨筋", "長腓骨筋", "外側広筋", "内側広筋", "大腿直筋", "長内転筋",
        "外側腓腹筋", "内側腓腹筋", "ヒラメ筋", "大腿二頭筋", "半腱様筋", "大腿筋膜張筋",
        "中殿筋", "大殿筋", "脊柱起立筋", "外腹斜筋"]

    for i, session in enumerate(W):
        plt.figure(figsize=(12, 36), dpi=125)
        for j, synergy in enumerate(session.T):
            plt.subplots_adjust(hspace=0.6)
            plt.subplot(8, 2, j + 1)
            plt.title(f"セッション: {i + 1}, シナジー: {j + 1}")
            plt.bar(muscle_names, synergy, color=colors)
            plt.xticks(muscle_names, muscle_names, rotation=90)
            plt.grid(axis="y")
        plt.show()


def plot_synergy_activities(C, ct=0.5, fs=1925.926):
    t = np.arange(C[0].shape[1]) / fs
    for i, session in enumerate(C):
        for j, synergy in enumerate(session):
            c = np.convolve(synergy, np.ones(int(fs * ct)) / int(fs * ct), mode='same')
            plt.figure(figsize=(24, 2))
            plt.title(f"セッション: {i + 1}, シナジー: {j + 1}")
            plt.grid()
            plt.plot(t, c)
            plt.show()


def e(E, w, c):
    return E - w.dot(c)


def vaf(E, w, c):
    return (1 - np.sum(np.power(e(E, w, c), 2)) / np.sum(np.power(E, 2))) * 100


def vafm(vafma, session, E, w, c):
    for i in range(len(E)):
        vafma[session][i] = (1 - np.sum(e(E, w, c).T[i]) / np.sum(E.T[i])) * 100


def isVAF(E, w, c, vafma, session, vafp=90, vafmp=75):
    v = vaf(E, w, c)
    vafm(vafma, session, E, w, c)
    return v, (v > vafp and np.min(vafma[session]) >= vafmp)
