#!/bin/bash

#if [ $# -eq 2 ] ; then
#output='tmpdl'
output=$(date +%s.%N)
if [ $# -ge 1 ] ; then

    wget $1 -O $output --quiet
    titlestring=$(grep "property='og:description'>" $output)
    echo $titlestring |  sed "s/<meta content='//" | sed "s/' property='og:description'>//"
    rm $output
fi
