#!/bin/sh
sudo apt install vlc
sudo apt install galculator
sudo apt install python3.6
sudo apt-get install python-pip
pip3 install python-vlc
sudo apt-get install portaudio19-dev python-pyaudio
pip3 install PyAudio
pip3 install PySide2
pip3 install SpeechRecognition
pip3 install pypiwin32
pip3 install pyinstaller
pyinstaller main.py --onefile --noconsole
