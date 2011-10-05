all:
	cd partify; make
clean:
	rm -rf *.pyc
	cd partify; make clean
