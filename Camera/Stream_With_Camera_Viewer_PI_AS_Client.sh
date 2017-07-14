raspivid -t 0 -hf -n -h 540 -w 960 -fps 24 -o - | nc 192.168.199.224 5001
