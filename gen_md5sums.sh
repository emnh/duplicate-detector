#!/bin/bash
time ( find -type f -print0 | xargs -0 md5sum > sums.txt )
