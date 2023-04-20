N=6
Trazas=100
#seq $N
#seq $N > seq

# https://askubuntu.com/questions/878948/how-do-i-generate-a-running-cumulative-total-of-the-numbers-in-a-text-file
#sed 'a+p' seq | dc -e0 -

echo math
gmt math -o0 T -T0/$Trazas/$(($N+1))+n = > SEQ.txt
cat SEQ.txt
echo RINT=
gmt math SEQ.txt RINT = 