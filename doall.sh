rm *.png
#python daygraph.py
python dailygraph.py
#python timezonegraph.py
python dayline.py
mutt -s [ELECTRICITY] -a *.png -- $1 < /dev/null