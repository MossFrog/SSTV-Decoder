from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import pyaudio
import numpy as np
from PIL import Image
from scipy.signal import hilbert

#-- Initial Variables
SRate = 44100

#-- Create the lines array (image)
img = Image.new( 'L', (140,140), "white")
pixelData = img.load()

#-- Copy all the samples into an array
input_data = read("example.wav")
audio = input_data[1]

#-- Generate the Hilbert transformed vector of the samples
analytic_signal = hilbert(audio)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.unwrap(np.angle(analytic_signal))
i_frequency = np.diff(instantaneous_phase) / (2.0*np.pi) * SRate


#-- Plot the frequency over time graph
plt.plot(i_frequency)
plt.ylabel('Frequency')
plt.show()

lineCount = 0
sampleBuffer = 0
#-- Search for the line sync pulses (Should be approx above 190 samples below 1300hz
for i in range(0, len(i_frequency)-2800):
    
    #-- If the frequency is below 1300Hz start counting
    if(i_frequency[i] < 1300):
        sampleBuffer = sampleBuffer + 1

    #-- If over 207 samples below the given frequency are found increment the line count
    if(sampleBuffer > 207):
        lineCount = lineCount + 1
        sampleBuffer = 0

        lineBuffer = 0
        lineIndex = 0
        #-- Grab the whole line data
        for j in range(i, i + 2700):
            lineBuffer = lineBuffer + 1
            if(lineBuffer > 22):
                lineBuffer = 0
                
                #-- Map each individual data point into a pixel value
                if(i_frequency[j] < 1500):
                    pixelData[lineIndex,lineCount] = 0
                elif(i_frequency[j] > 2300):
                    pixelData[lineIndex,lineCount] = 255
                    
                #-- Normalize the value from frequency to Grayscale and map the pixel
                else:
                    pixelData[lineIndex,lineCount] = np.int(((i_frequency[j] - 1500.0)/800.0)*255.0)
                    
                #-- Skip a line
                lineIndex = lineIndex + 1
        
    
    #-- Safety check to prevent extra line detection
    if(i_frequency[i] > 1300):
        sampleBuffer = 0
    
print("-- Line Count --")
print(lineCount)
print("-- Sample Rate --")
print(SRate)
print("-- Number of Samples --")
print(len(i_frequency))
print("")
print("== Operation Complete, Press any key to see the result... ==")
raw_input()      
    
#-- Display the resulting image
img.show()

