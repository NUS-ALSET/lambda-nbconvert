#!/bin/bash

rm -rf build/code
mkdir -p build/code
pip3.6 install -r requirements.txt -t build/code
