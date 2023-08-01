#!/usr/bin/env sh

printf os=; uname -a
printf cpu=; grep name /proc/cpuinfo | head -n1 | sed 's/.*:\s*//'
printf cores=; grep processor /proc/cpuinfo | wc -l
printf mem_total=; grep MemTotal /proc/meminfo | sed 's/.*:\s*//'
printf mem_free=; grep MemFree /proc/meminfo | sed 's/.*:\s*//'
printf uptime=; uptime
printf pci=; cut -f2 /proc/bus/pci/devices | tr '\n' ',' | sed 's/.$/\n/'
printf modules=; echo /.__EL_SNEEDIO__/modules.d/*
printf cpu_usage=; awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1) "%"; }' <(grep 'cpu ' /proc/realstat) <(sleep 1; grep 'cpu ' /proc/realstat)
echo END
