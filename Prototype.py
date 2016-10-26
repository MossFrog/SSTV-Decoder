import pyaudio
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
img = Image.new( 'L', (120,120), "black")
pixels = img.load()

CHUNK = 64
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 150000
FREQUENCY_STEP = float(RATE)/float(CHUNK)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

x = 0
y = 0

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)

    #-- Decode the Data Chunk into a 16 Bit integer array
    decodedArray = numpy.fromstring(data, 'Int16');

    #-- Normalize the values between 1-0
    for j in range(0,CHUNK):
        decodedArray[j] = float(decodedArray[j]/pow(2,16))
        
    #-- Pad the Decode Array with zeroes
    while(len(decodeArray) < 512):
        np.hstack(decodeArray,(0))
        
    print(decodeArray)

    #-- Apply the FFT to acquire a frequency analysis of the samples
    freqDomain = numpy.fft.fft(decodedArray)
    
    
    #-- Create a magnitude vector
    magVector = freqDomain
    for j in range(0, CHUNK):
        magVector[j] = numpy.sqrt(pow(freqDomain[j].real,2) + pow(freqDomain[j].imag,2))
        magVector[j] = magVector[j].real

    #print(magVector)
    #plt.plot(magVector)
    #plt.show()
    

    for j in range(0, CHUNK):
       if (magVector[j] > 50):
           if((j*FREQUENCY_STEP < 2350) and (j*FREQUENCY_STEP > 1450)):
               #-- Decode within these frequencies (2350Hz-1450Hz)
               pixelVal = abs((j*FREQUENCY_STEP - 1500)/3.15)
               pixels[x,y] = (pixelVal)
               #print(j*FREQUENCY_STEP)
               #print(pixelVal)
               x = x + 1
               if(x > 119):
                   x = 0
               
           if((j*FREQUENCY_STEP < 1300) and (j*FREQUENCY_STEP > 1200)):
               #-- Horizontal Sync Pulse
               #print(j*FREQUENCY_STEP)
               y = y + 1
               if(y >= 119):
                y = 119
                img.show()
                raw_input()
               
    
    #-- Uncomment this section to Play the audio 
    #stream.write(data, CHUNK)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()

