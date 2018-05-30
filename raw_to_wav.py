###########################################################
# This method converts raw audio files in the project directory to wav files
#
# Author: Johannes Bramauer, Vienna University of Technology
# Created: May 30, 2018
# License: MIT
#
###########################################################
import wave

def rawToWav(filename):

    outfile = wave.open(filename + ".wav", "wb")
    outfile.setframerate(48000)
    outfile.setnchannels(1)
    outfile.setsampwidth(2)

    f = open(filename + ".raw", "rb")
    sample = f.read(4096)
    print 'start conversion: ' + filename + ".raw"

    while sample != "":
        outfile.writeframes(sample)
        sample = f.read(4096)

    outfile.close()
