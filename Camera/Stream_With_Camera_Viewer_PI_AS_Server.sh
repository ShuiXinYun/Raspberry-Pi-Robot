raspivid -t 0 -hf -n -h 400 -w 600 -fps 30 -o - | nc -l -p 5001