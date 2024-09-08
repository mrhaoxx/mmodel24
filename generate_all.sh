#!/bin/bash -xe

rm -f *.ans
rm -f *.csv
rm -f *.xlsx

python 1-simloc_qustion1.py > 1.loc.ans
python 1-simspeed_qustion1.py > 1.spd.ans

python 2-collison_time_question2.py > 2.time.ans
python 2-simloc_qustion2.py `cat 2.time.ans` > 2.loc.ans
python 2-simspeed_qustion2.py `cat 2.time.ans` > 2.spd.ans

python 4-simloc_question4.py > 4.loc.ans
python 4-simspeed_question4.py > 4.spd.ans


python csv_to_xlsx_question1_latex.py 1.loc.ans 1.spd.ans
python csv_to_xlsx_question2_latex.py 2.loc.ans 2.spd.ans
python csv_to_xlsx_question4_latex.py 4.loc.ans 4.spd.ans

python csv_to_xlsx_question1.py 1.loc.ans 1.spd.ans
python csv_to_xlsx_question2.py 2.loc.ans 2.spd.ans
python csv_to_xlsx_question4.py 4.loc.ans 4.spd.ans