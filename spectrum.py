
import numpy as np
import numpy.typing as npt
import scipy
import matplotlib.pyplot as plt

def plot_spectrum(signal: npt.ArrayLike, Fs: float, title: str="", newfigure: bool=True):
    """
    Plot the spectrum of the signal
    :param signal:  time series
    :param Fs: sample rate
    :param newfigure: plot in new figure?
    :return: None
    """
    # Compute the discrete Fourier transform (DFT)
    omega = np.fft.fft(signal * scipy.signal.windows.hamming(signal.shape[-1]))
    dB = 20 * np.log10(np.abs(omega))
    # Determine frequencies at which we sampled the DFT
    # The DFT computes from -Nyquist : Nyquist
    # and the fftfreq function has these shifted, so we undo it.
    freqs = scipy.fft.fftshift(np.fft.fftfreq(omega.shape[-1], 1.0/Fs))
    dB = scipy.fft.fftshift(dB)

    # Show it
    if newfigure:
        plt.figure()
    plt.plot(freqs, dB)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB rel.)')

    if title != "":
        plt.title(title)






