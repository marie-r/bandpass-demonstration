import numpy as np
import numpy.typing as npt
from scipy.signal import iirdesign, freqz_sos, sosfilt, sosfiltfilt
import matplotlib
import matplotlib.pyplot as plt

class Filter:
    def __init__(self, passband_edges, stopband_edges, pass_dB=.1, stop_dB=75, Fs=1):
        """
        Design a filter.
        bandpass - specify pairs of passband/stopband edges
        lowpass - specify 1 stopband edge > passband edge
        highpass - specify 1 stopband edge < passband edge

        :param passband_edges:  Edges where signal passes
        :param stopband_edges: Edges where signal is attenuated
        :param pass_dB:  passband magnitude adjust
        :param stop_dB: stopband magnitude attenuation
        :param Fs:  sample rate

        Sample rate Fs is only meaningful to allow one to pass edges in Hz
        as opposed to a normalized number between [0, 1] representing the
        0 Hz and the Nyquist frequency (Fs/2).
        """

        # Store parameters in instance
        self.passband_edges = passband_edges
        self.stopband_edges = stopband_edges
        self.stop_dB = stop_dB
        self.pass_dB = pass_dB
        self.Fs = Fs

        # Construct infinite impulse response filter
        self.filter = iirdesign(passband_edges, stopband_edges,
                                gpass=pass_dB,
                                gstop=stop_dB,
                                analog=False,
                                output='sos',
                                fs=Fs)

    def plot_response(self, showphase=True):
        """
        Plot the frequency/phase response of the filter.
        :param showphase: whether to show the phase response
        :return: None
        """

        fig, ax1 = plt.subplots()
        # Compute the frequency response
        freq, resp = freqz_sos(self.filter, fs=self.Fs)
        # Visualize how each frequency is modified in magnitude
        ax1.plot(freq, 20 * np.log10(abs(resp)), 'b')
        if self.Fs != 1:
            ax1.set_xlabel('Frequency (Hz)')
        else:
            ax1.set_xlabel('Frequency (radians)')
        ax1.set_ylabel('Magnitude (dB rel.)', color='b')
        ax1.grid(True)

        if showphase:
            # Visualize the phase response
            ax2 = ax1.twinx()
            phase = np.unwrap(np.angle(resp))
            ax2.plot(freq, phase, 'g:')
            ax2.set_ylabel('Phase (radians)', color='g')
            ax2.grid(True)
            ax2.axis('tight')
            ax2.set_ylim((-6, 1))

            nticks = 8
            ax2.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))
            ax1.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))
            ax1.set_title("Frequency/Phase Response")
        else:
            ax1.set_title('Frequency Response')

    def convolve(self, signal: npt.ArrayLike, filtfilt=False):
        """
        Convolve the filter with an input signal.
        :param signal: Signal to be filtered
        :param filtfilt: If True, forward and backward filtering
           are applied, resulting in a zero-phase filtered signal.
        :return: filtered signal
        """

        if filtfilt:
            output = sosfiltfilt(self.filter, signal)
        else:
            output = sosfilt(self.filter, signal)

        return output

    def shift_freq(self, signal: npt.ArrayLike, Hz: float):
        """
        Shift a frequencies in a signal by +/- Hz at the filter sample rate.
        Only produces valid results when the sample rate was set on
        object construction and the signal is of the same sample rate.

        :param signal:  signal to be shifted
        :param Hz:  Amount to shift by
        :return:  shifted signal

        Caveats:
        Signal should be fitlered prior to shifting.
        See https://wirelesspi.com/the-heterodyne-principle-and-the-superheterodyne-receiver/
        for an explanation of the heterodyne principle.
        """

        # Heterodyne shift the signal
        # Create a carrier wave that copies two versions of the
        # signal shifted by +/- Hz.

        time_s = np.linspace(0, stop=signal.shape[0]/self.Fs,
                             num=signal.shape[0], endpoint=False)
        f_local = np.cos(2*np.pi*Hz*time_s)
        het_signal = f_local * signal

        return het_signal












