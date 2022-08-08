#!/usr/bin/python
"""

This small script converts a wav file to a sequence of *beep* calls, through
frequency analysis.

@author: T. Teijeiro
"""

import os
from scipy.io import wavfile
import numpy as np
import argparse

def frequency(note, octave):
    """http://latecladeescape.com/t/Frecuencia+de+las+notas+musicales"""
    return (440.0 * np.exp(((octave-4)+(note-10)/12.0)*np.log(2)))

#Accepted frequencies
FREQS = np.array([1] + [frequency(n,o)
    for o in range(10)
        for n in range(1,13)])

#Argument parsing
parser = argparse.ArgumentParser(
    description='.wav conversion to sequence of pcspeaker beeps.')
parser.add_argument('file', help='raw .wav file to be converted.')
parser.add_argument('-w', metavar='TIME',
    help='Time window for frequency analysis (in ms). Default 50 ms.' )
parser.add_argument('--verbose', action='store_true',
    help='Prints the beep command.')
parser.add_argument('--silent', action='store_true',
    help='Does not execute the generated beep command.')
parser.add_argument('--arduino', action='store_true',
    help='Additionally print arduino equivalent order')
args = parser.parse_args()

#Maximum permitted length of the processed data (in seconds)
MAX_LEN = 40
#Resolution of the time window for frequency analysis.
CH_MS = 50 if not args.w else int(args.w)
fs, data = wavfile.read(args.file)
data = data[:MAX_LEN * fs]
#Window size and overlap definition for the spectral analysis
w = int(fs/1000.0 * CH_MS)
overlap = w/2
#Number of chunks with the selected parameters
n = len(data)/(w-overlap)
#Duration of each beep
dur = int(1000.0*(len(data)/float(fs))/n)
#Array of frequencies
freq = np.arange(0,fs/2.0,(fs/2.0)/(w/2))
#We truncate the data array to be a multiplo of the step
data = data[:int(n*(w-overlap))]
blw = np.blackman(w)
freql = []
for i in range(0, len(data), int(w-overlap)):
    chunk = data[i:i+w]
    if len(chunk) != w:
        chunk = chunk.copy()
        chunk.resize(w)
    chunk = chunk * blw
    chunk = chunk-np.mean(chunk)
    ft = np.fft.fft(chunk)
    ft = ft[:int(w/2)]
    #Get the most representative frequency of the chunk
    hz = freq[np.absolute(ft).argmax()]
    #We check the frequency table to get the closest
    hz = FREQS[np.abs(FREQS-hz).argmin()]
    if freql and freql[-1][1] == hz:
        freql[-1] = (freql[-1][0]+dur, hz)
    else:
        freql.append((dur, hz))
#Command build (beep version)
#Example: beep -l 50 -f 140.0 -n -l 250 -f 370.0 -n -l 50 -f 190.0
com = 'beep '
for msec, freq in freql:
   com = com + '-l {0} -f {1} -n '.format(msec,freq)
com = com[:-4]
if args.verbose:
    print(com)
if not args.silent:
    os.system(com)

#Arduino version
if args.arduino:
    com = ''
    for msec, freq in freql:
        com += 'tone(4, {0}, {1});\ndelay({2});\n'.format(freq, msec, msec)
    if args.verbose:
        print('Arduino equivalent order:')
        print(com)