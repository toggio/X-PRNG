"""
Universal Cross-Platform Multi-Language Pseudo Random Number Generator (pseudoRandom) v0.9

A Set of libraries for Pseudo-Random Number Generation across environments

X-PRNG is an advanced set of libraries designed to provide developers with tools
for generating pseudo-random numbers across various computing environments. It
supports a wide range of applications, from statistical analysis and data simulation
to secure cryptographic functions. These libraries offer a simple yet powerful
interface for incorporating high-quality, pseudo-random numbers into applications
written in different programming languages, ensuring consistency and reliability
across platforms.

Copyright (C) 2024 under GPL v. 2 license
18 March 2024

@author Luca Soltoggio
https://www.lucasoltoggio.it
https://github.com/toggio/X-PRNG
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
PseudoRandom Number Generator Python Class

This class implements a pseudo-random number generator (PRNG) using a linear
congruential generator (LCG) algorithm.
"""

import time
import zlib

class pseudoRandom:

    def __init__(self, seed=None):
        """
        Constructor to initialize the PRNG with an optional seed.
        If a string is provided as a seed, it uses crc32 to convert it into an integer.
        If no seed is provided, it uses the current time.
        
        :param seed: Optional seed for the PRNG.
        """
        self._a = 1664525  # Multiplier
        self._c = 1013904223  # Increment
        self._m = 4294967296  # Modulus (2^32)
        self._counter = 0
        if isinstance(seed, str):
            self._RSeed = zlib.crc32(seed.encode()) & 0xffffffff
        elif seed is not None:
            self._RSeed = abs(int(seed))
        else:
            self._RSeed = int(time.time())
        self._counter = 0

    def reSeed(self, seed=None):
        """
        Function to re-seed the PRNG. This can be used to reset the generator's state.
        
        :param seed: Optional new seed for the PRNG.
        """
        self.__init__(seed)

    def saveState(self):
        """
        Saves the current state of the PRNG for later restoration.
        """
        self._savedRSeed = self._RSeed

    def restoreState(self):
        """
        Restores the PRNG to a previously saved state.
        """
        if self._savedRSeed is not None:
            self._RSeed = self._savedRSeed

    def randInt(self, min=0, max=255):
        """
        Generates a pseudo-random integer within a specified range.
        
        :param min: The lower bound of the range (inclusive).
        :param max: The upper bound of the range (inclusive).
        :return: A pseudo-random integer between min and max.
        """
        self._c = zlib.crc32((str(self._counter) + str(self._RSeed) + str(self._counter)).encode()) & 0xffffffff
        self._RSeed = (self._RSeed * self._a + self._c) % self._m
        self._counter += 1
        return int((self._RSeed / self._m) * (max - min + 1) + min)

    def randBytes(self, length=1, decimal=False, readable=False):
        """
        Generates a string of pseudo-random bytes of a specified length.

        :param length: The length of the byte string.
        :param decimal: If true, returns an array of decimal values instead of a byte string.
        :param readable: If true, ensures the generated bytes are in the readable ASCII range.
        :return: A string or an array of pseudo-random bytes.
        """
        bytes = []
        for _ in range(length):
            if readable:
                byte = self.randInt(32, 126)
            else:
                byte = self.randInt(0, 255)
            if decimal:
                bytes.append(byte)
            else:
                bytes.append(chr(byte))
        return bytes if decimal else ''.join(bytes)
