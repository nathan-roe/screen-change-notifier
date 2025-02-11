#!/bin/bash
mkdir -p build
pushd build
source ../../screen-notifier/bin/activate
pyinstaller --onefile ../../src/main.py
popd
