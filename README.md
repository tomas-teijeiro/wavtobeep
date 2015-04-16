# wavtobeep
Converts a wav file to a sequence of *beep* PC-speaker calls through frequency analysis using the fft transform.

## Getting started

1. Download the script
2. Check the PC-speaker module is loaded:
 `~$ modprobe pcspkr`
3. Execute it:

 `~$ python wavtobeep.py [-h] [-w TIME] [--verbose] [--silent] wav_file`
 
#### Lovely example included!

 `python wavtobeep.py monkey-island-sample.wav`
