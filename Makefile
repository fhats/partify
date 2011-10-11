all:
	cd partify; make

test:
	testify tests

clean:
	find ./ -name "*.pyc" -delete
	cd partify; make clean
