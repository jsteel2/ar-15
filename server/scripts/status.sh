#!/usr/bin/env sh

printf os=; uname -a
printf cpu=; grep name /proc/cpuinfo | head -n1 | sed 's/.*:\s*//'
printf cores=; grep processor /proc/cpuinfo | wc -l
printf mem_total=; grep MemTotal /proc/meminfo | sed 's/.*:\s*//'
printf mem_free=; grep MemFree /proc/meminfo | sed 's/.*:\s*//'
printf uptime=; uptime
printf pci=; cut -f2 /proc/bus/pci/devices | tr '\n' ',' | sed 's/.$//'
echo END
