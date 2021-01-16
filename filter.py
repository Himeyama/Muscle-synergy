#!/usr/bin/env python
from scipy import signal


def bandpass(x, f, fp, fs, gpass, gstop):
    """
    Parameters
    ----------
    x : データー
    f: サンプリング周波数
    fp: 通過域端周波数 [Hz]
    fs: 阻止域端周波数 [Hz]
    gpass: 通過域最大損失量 [dB]
    gstop: 阻止域最小減衰量 [dB]

    Returns
    -------
    y : ndarray
    """

    fn = f / 2
    wp = fp / fn
    ws = fs / fn
    n, wn = signal.buttord(wp, ws, gpass, gstop)
    b, a = signal.butter(n, wn, "band")
    y = signal.filtfilt(b, a, x)
    return y


def highpass(x, f, fp, fs, gpass, gstop):
    """
    Parameters
    ----------
    x : データー
    f: サンプリング周波数
    fp: 通過域端周波数 [Hz]
    fs: 阻止域端周波数 [Hz]
    gpass: 通過域最大損失量 [dB]
    gstop: 阻止域最小減衰量 [dB]

    Returns
    -------
    y : ndarray
    """

    fn = f / 2
    wp = fp / fn
    ws = fs / fn
    n, wn = signal.buttord(wp, ws, gpass, gstop)
    b, a = signal.butter(n, wn, "high")
    y = signal.filtfilt(b, a, x)
    return y


def lowpass(x, f, fp, fs, gpass, gstop):
    """
    Parameters
    ----------
    x : データー
    f: サンプリング周波数
    fp: 通過域端周波数 [Hz]
    fs: 阻止域端周波数 [Hz]
    gpass: 通過域最大損失量 [dB]
    gstop: 阻止域最小減衰量 [dB]

    Returns
    -------
    y : ndarray
    """

    fn = f / 2
    wp = fp / fn
    ws = fs / fn
    n, wn = signal.buttord(wp, ws, gpass, gstop)
    b, a = signal.butter(n, wn, "low")
    y = signal.filtfilt(b, a, x)
    return y
