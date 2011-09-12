all: player.js

player.js:
	coffee -o static/js/partify/workers/ -c js/player/workers/
	coffee --join static/js/partify/player.js -c js/player/*.coffee

continuous:
	coffee --watch -o static/js/partify/workers/player_event.js -c js/player/workers/player_event.coffee
	coffee --watch --join static/js/partify/player.js -c js/player/*.coffee	
