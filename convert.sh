#/bin/bash

set -e

# Thanks to https://github.com/SpaceinvaderOne/Beep-Music-Converter

if [[ -z $2 ]]; then
    echo "Example: $0 test.mp3 out.txt"
    exit 1
fi

if [[ -f tmp.wav ]]; then
    echo "ERROR: Please remove tmp.wav file."
    exit 2
fi

sox -G $1 -r 16000 -c 1 -b 16 tmp.wav

python3 wavtobeep.py --verbose -w ${time:-50} --silent tmp.wav > $2

rm -rf tmp.wav

echo "Done. Check output in $2 file."
echo "Have a nice day!"
