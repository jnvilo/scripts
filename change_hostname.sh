#!/bin/bash 
h=`/bin/hostname`
cat /etc/sysconfig/network  | sed "s/^HOSTNAME=$h/HOSTNAME=$1/w /etc/sysconfig/network"
hostname $1

