N=3
Trazas=100
#seq $N
#seq $N > seq

# https://askubuntu.com/questions/878948/how-do-i-generate-a-running-cumulative-total-of-the-numbers-in-a-text-file
#sed 'a+p' seq | dc -e0 -

gmt math -o1 T -T0/$Trazas/$(($N+1))+n = 
gmt math -o1 T -T0/$Trazas/$(($N+1))+n RINT =
