1ms = 44,1 samples of the signal (Minimum window should be close to this 44100Hz)
Strangely the "classic.wav" uses a sample rate of 22050Hz equating to 22 odd samples per milisecond
8 Second Signal
15 Lines per second (Including the vertical sync pulse approx)
Line sync pulse 1200Hz
Range for actual line data is 1500-2300Hz
Vertical Sync Pulse 30ms (Questionable)
Horizontal Sync Pulse 5ms (600ms of the signal at the end of every line or beginning (arbitrary))
Online souurces use "32 to 64 samples and zero padded the FFT to 512 or 1024" (How does this effect the frequency resolution?)
0.55ms Per pixel (Not realistic how can one decode pixel by pixel??)

"SSTV uses 15 lines per second, this gives each line a duration of 66.67 ms. 
5 ms of this time is consumed by the line sync pulse, so each row must be interpolated to cover 61.67 ms"

Maths:
Given each line is 66.67ms
One would need 2941 samples per line of data


Different Methods

    Decode the VIS code and start image decoding according to the mode read from the VIS code
    Ignore the VIS code and decode an image according to a previously set mode
    Ignore the VIS code, start decoding when enough number of sync pulses have been received using a previously set mode
    Autodetect the mode, start decoding when enough sync pulses have been received for the autodetection

In our case we have one or two modes 
Robot 8
or
Classic Black and White
(What is the difference?? VIS codes)

Revelation!
= Short Time Fourier Transform =


    Pick out a short segment of data from the overall signal
    Multiply that segment against a half-cosine function
    Pad the end of the segment with zeros
    Take the Fourier transform of that segment and normalize it into positive and negative frequencies
    Combine the energy from the positive and negative frequencies together, and display the one-sided spectrum
    Scale the resulting spectrum into dB for easier viewing
    Clip the signal to remove noise past the noise floor which we don’t care about


    The number of samples of data in is equal to the number of frequency bins out
    The maximum frequency that can be represented is the Nyquist frequency, or half the sampling frequency of the data.

    In the the Discrete Fourier Transform (what we are using) 
    the order of the frequency bins is 0 Hz (DC component), positive frequencies, Nyquist Frequency, negative frequencies

    The data from the Fourier transform needs to be scaled by the number of samples 
    in the transform to maintain equal energy (according to Parseval’s theorem)

Structure:

Ignore the VIS Codes

Begin segmenting the data into an array of lines
Each line (Without line sync signal) is 61.67ms
Each line contains the raw sample data after recieving the 1200Hz signal for 5ms (44*61.67 samples or 22*61.67 samples)
Convert line data into pixel data by applying the FFT on small groups of samples and then normalizing (Note pad zeroes to get better results?)



Resources:
http://brainwagon.org/2011/09/25/classic-black-white-sstv/
http://www.sstv-handbook.com/
http://www.g0hwc.com/sstv_modes.html
http://brainwagon.org/2011/09/26/classic-black-and-white-sstv-timings/
https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/
http://www.acasper.org/2011/10/14/sstv-through-water-communication-link/


