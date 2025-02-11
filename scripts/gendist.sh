#!/bin/bash
mkdir build
pushd ./build
source ../screen-notifier/bin/activate
pyinstaller --onefile ../src/main.py
popd
