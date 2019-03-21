configure:
	cd pyhisto; git pull -r
	cd faster; git pull -r

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

