configure:
	rm -rvf pyhisto
	git clone https://gitlab.in2p3.fr/gregoire.henning/pyhisto.git
	rm -rfv faster 
	git clone https://gitlab.in2p3.fr/gregoire.henning/faster.git


clean:
	rm -rfv faster 
	rm -rfv pyhisto
	rm -rfv __pycache__
	rm -rfv *.pyc  

commit:
	git add -u
	git status
	git commit -m "`date +%F-%H-%M-%S-000%w`"
	git push -u origin master

