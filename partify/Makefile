# Copyright 2011 Fred Hatfull

# This file is part of Partify.

# Partify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Partify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Partify.  If not, see <http://www.gnu.org/licenses/>.

all: player.js

player.js:
	coffee -o static/js/partify/workers/ -c js/player/workers/
	coffee  --join static/js/partify/player.js -c js/player/*.coffee

continuous:
	coffee --watch -o static/js/partify/workers/player_event.js -c js/player/workers/player_event.coffee
	coffee --watch --join static/js/partify/player.js -c js/player/*.coffee

clean:
	rm -rf static/js/partify/workers/*.js
	rm -rf static/js/partify/player.js
