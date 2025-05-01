import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # Qt bindings provided by PyQt5

import matplotlib.pyplot as plt
import resampy  # resampling module

# our modules
import spectrum
import filters


# demonstration of filtering
def main():
    plt.ion()   # enable interactive Matplotlib

    Fs = 8000  # sample rate

    duration_s = 1
    duration_N = duration_s * Fs

    # Construct a signal with sinusoids at the following frequencies:
    centers = [100, 200, 1500, 1800, 3200, 3300, 3400, 3500]
    signal = np.zeros((duration_N,))
    time_s = np.linspace(0, duration_s, duration_N, endpoint=False)
    for c in centers:
        signal += .75 * np.cos(2*np.pi*c*time_s)

    # Show what we are starting with
    spectrum.plot_spectrum(signal, Fs, title="Original signal", newfigure=True)

    # Bandpass filter
    lower_Hz = 1000
    upper_Hz = 2000
    # filters require a transition region between where they allow the signal
    # through and where they attenuate frequency.  The smaller this transition
    # region is, the more complicated it is to create a good filter.
    transition_Hz = 300
    filter = filters.Filter(
        passband_edges=[lower_Hz, upper_Hz],  # passband edges
        stopband_edges=[lower_Hz - transition_Hz, upper_Hz + transition_Hz],  # start/end of transition region
        Fs=Fs
    )
    # Show frequency response of filter
    filter.plot_response(showphase=False)

    # Filter the signal
    filtered_signal = filter.convolve(signal, filtfilt=False)

    # Show resultant signal
    spectrum.plot_spectrum(filtered_signal[200:-200], Fs, title="Filtered signal", newfigure=True)

    # Use a heterodyne to shift the left edge of the pass band to base band (0 Hz)
    # This will create two copies of spectrum overlaid, but the duplicates
    # will be outside of the passband region that has been shifted to zero.
    shifted_signal = filter.shift_freq(filtered_signal, -lower_Hz)
    spectrum.plot_spectrum(shifted_signal, Fs, title="Shifted signal", newfigure=True)

    bandwidth = upper_Hz - lower_Hz
    new_Fs = 2 * bandwidth
    # Resample
    downsampled = resampy.resample(shifted_signal, Fs, new_Fs)
    spectrum.plot_spectrum(downsampled, new_Fs, title="Filtered signal shifted to baseband", newfigure=True)
    print('all done')





if __name__ == '__main__':
    main()

