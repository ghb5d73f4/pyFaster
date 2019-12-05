set chan=%1


\Users\ghenning\anaconda\python.exe scripts\project2D.py --axis='y' < output\%chan%.clean.2d.txt > output\%chan%.clean.energy.1d.txt 
\Users\ghenning\anaconda\python.exe scripts\project2D.py --axis='x' < output\%chan%.clean.2d.txt > output\%chan%.clean.time.1d.txt 
\Users\ghenning\anaconda\python.exe scripts\project2D.py --axis='y' < output\%chan%.all.2d.txt > output\%chan%.all.energy.1d.txt 
\Users\ghenning\anaconda\python.exe scripts\project2D.py --axis='x' < output\%chan%.all.2d.txt > output\%chan%.all.time.1d.txt 

\Users\ghenning\anaconda\python.exe scripts\Draw2Dh.py output\%chan%.clean.2d.txt output\%chan%.all.2d.txt

\Users\ghenning\anaconda\python.exe scripts\Draw1Dh.py output\%chan%.counters.1d.txt output\%chan%.all.time.1d.txt output\%chan%.all.energy.1d.txt output\%chan%.clean.time.1d.txt output\%chan%.clean.energy.1d.txt 

