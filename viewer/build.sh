#!/bin/bash

#rm -rf build
mkdir -p build
cd build

##sudo apt-get install ninja-build
#cmake -G "Ninja" "-DCMAKE_BUILD_TYPE=Release" ..
cmake ..
cmake --build . --target install
cd ..
