all:
	cd partify; make
clean:
	find ./ -name "*.pyc" -delete
	cd partify; make clean
