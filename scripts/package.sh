#!/bin/bash

rm -rf build/code
mkdir -p build/code
pip3.6 install -r requirements.txt -t build/code
find "build/code" -name "*.so" | xargs strip
cd build/code
if [ -e pandas/tests ]
then
	rm -rf pandas/tests
fi
if [[ -e numpy/.libs && -e scipy/.libs ]]
then
	diff -qs numpy/.libs/ scipy/.libs/|sed -ne '/ are identical$/ { s|Files \(.\+\) and \(.\+\) are identical$|rm \2; ln -s ../../\1 \2|; p; }'|bash
fi
