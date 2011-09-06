from werkzeug.serving import run_simple

from partify import app

if __name__ == "__main__":
	# Experiment with IDLE
	# ...
	run_simple('localhost', 5000, app, use_reloader=True, threaded=True)
