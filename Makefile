configure: scripts/lib/pyhisto/__init__.py \
	scripts/lib/faster/__init__.py \
	scripts/lib/grapheme/__init__.py
	#
	cd scripts/lib/pyhisto; git pull -r
	cd scripts/lib/faster; git pull -r
	cd scripts/lib/grapheme; git pull -r

scripts/lib/pyhisto/__init__py:
	git clone https://gitlab.in2p3.fr/gregoire.henning/pyhisto.git scripts/lib/pyhisto

scripts/lib/faster/__init__.py:
	git clone https://gitlab.in2p3.fr/gregoire.henning/faster.git scripts/lib/faster

scripts/lib/grapheme/__init__.py:
	git clone https://gitlab.in2p3.fr/gregoire.henning/grapheme-faster-config.git scripts/lib/grapheme

clean:
	rm -rfv scripts/lib/
	rm -rfv __pycache__
	rm -rfv *.pyc  


