#!/bin/bash

function csum() {
  cmd=$1
  lines=$2
  find -type f -print0 | tee >(tr '\0' '\n' | pv -l -s $lines > /dev/null) | xargs -0 $cmd > $cmd.txt
}

lines=$(find -type f | wc -l)
time csum xxh32sum $lines
time csum xxh64sum $lines
time csum xxh128sum $lines
