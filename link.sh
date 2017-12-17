#!/bin/bash

mkdir -p .requirements
pip3 install -r requirements.txt -t .requirements
ln -sv .requirements/* .
