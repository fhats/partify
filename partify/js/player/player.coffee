`/*
Copyright 2011 Fred Hatfull

This file is part of Partify.

Partify is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Partify is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Partify.  If not, see <http://www.gnu.org/licenses/>.
*/`

$ = jQuery

$ ->
    # Initial setup of the Player object and namespacing within front-end
    window.Partify = window.Partify || {}
    window.Partify.Player = new Player()
    window.Partify.Player.init()
    window.Partify.Queues = window.Partify.Queues || {}
    window.Partify.Queues.GlobalQueue = window.Partify.Queues.GlobalQueue || {}

class Player
    # Class responsible for the functions of the "player", which displays information about the currently playing track
    constructor: () ->
        @info =
            artist: ''
            title: ''
            album: ''
            elapsed: 0
            time: 100
            date: 1970
            volume: 0
            state: 'pause'
            file: ''
            last_global_playlist_update: 0
        @config =
            up_next_items = 3
        @last_update_time = (new Date()).getTime()

    init: () -> 
        this.initPlayerVisuals()
        this.initPlayerUpdating()
        @info.last_global_playlist_update = (new Date()).getTime()

    initPlayerVisuals: () ->
        $("#player_progress").progressbar value: 0
        # This is not really related to the player and should move elsewhere eventually.
        $("#tabs").tabs()

    initPlayerUpdating: () ->
        # Set up push events
        #_initPlayerPushUpdates()

        # Set up intermittent polling for synchronization
        this._initPlayerSynchroPolling 3000

        # Update the progress counter without needing to hit the server every time
        this._initPlayerLocalUpdate()

    _initPlayerPushUpdates: () ->
        # Use WebWorkers here to get around the fact that most modern browsers 
        # hang using SSEs...
        worker = new Worker('static/js/partify/workers/player_event.js')

        worker.addEventListener 'message', (e) =>
            console.log e.data
        , false

        worker.postMessage 'Start checking push'

    _initPlayerSynchroPolling: (poll_frequency) ->
        # Initializes and is responsible for running polling updates with the server
        this._synchroPoll()

        # poll_frequnecy is in ms
        setInterval () => 
            this._synchroPoll()
        , poll_frequency

    _synchroPoll: () ->
        # Performs the polling updates with the server
        $.ajax(
            url: '/player/status/poll'
            method: 'GET'
            data: 
                current: @info.last_global_playlist_update
            success: (data) =>
                if data.elapsed
                    data.elapsed = parseFloat(data.elapsed)
                data.time = parseFloat(data.time)
                this.updatePlayerInfo data

                if data.global_queue
                    window.Partify.Queues.GlobalQueue.update(data.global_queue)
                    window.Partify.History.update()
                    window.Partify.Statistics.update()
                if data.user_queue
                    window.Partify.Queues.UserQueue.update data.user_queue
        )

    _initPlayerLocalUpdate: () ->
        # Sets up the timer that updates the player's progressbar every second
        setInterval () =>
            this._playerLocalUpdate()
        , 1000
            
    _playerLocalUpdate: () ->
        last_update_time = @last_update_time
        @last_update_time = (new Date()).getTime()
        # Updates the player to stay in sync with the Mopidy server without actually polling it.
        if @info.state == 'play'
            @info.elapsed = if Math.floor(@info.elapsed) < @info.time then @info.elapsed + ((@last_update_time - last_update_time) / 1000) else @info.elapsed
            this.updatePlayerProgress()
            if @info.elapsed >= @info.time
                this._synchroPoll()
                window.Partify.Queues.UserQueue.loadPlayQueue()

    updatePlayerInfo: (data) -> 
        # Takes an array of data items and populates the appropriate HTML elements
        info = for key, value of @info
            if data.state != 'stop' or key=='last_global_playlist_update'
                data[key] or= @info[key] # Fills in data with information from info in case that key does not exist in data. Prevents nasty undefineds everywhere
            @info[key] = data[key]
            # Special cases!
            if key == 'date'
                year = yearFromDateString(data[key])
                @info[key] = if year != "" and year > 0 then year else ""
        this._updatePlayerTextFromInfo text for text in ['artist', 'title', 'album', 'date']
        this.updatePlayerProgress()

    _updatePlayerTextFromInfo: (info_key) -> 
        # Responsible for updating player text from info in the player class
        this._updatePlayerText info_key, @info[info_key]

    _updatePlayerText: (info_key, data) ->
        # Responsible for updating text associated with the player
        info_span = $("#player_info_" + info_key).first()
        info_span.text data

    updatePlayerProgress: () ->
        # Update the actual progressbar element
        progress = Math.round( (@info.elapsed / @info.time) * 100 )
        $("#player_progress").progressbar value: progress
        this._updatePlayerText 'elapsed', secondsToTimeString @info['elapsed']
        this._updatePlayerText 'time', secondsToTimeString @info['time']

yearFromDateString = (date_string) ->
    d = new Date(date_string)
    year = d.getUTCFullYear()
    year

secondsToTimeString = (seconds) ->
    # In case seconds isn't already an int
    seconds = parseInt(Math.round(seconds))
    # Converts a number of seconds to a string representing a human-readable time (eg. MM:SS)
    seconds = Math.floor(seconds)
    minutes = Math.floor(seconds / 60 )
    hours = Math.floor(seconds / (60*60))
    days = Math.floor(hours / 24)
    seconds = (seconds % 60)

    time_s = ""

    if days > 0
        hours = hours % 24
        time_s += "" + days + ":"
        if hours < 10
            time_s += "0"
    if hours > 0
        minutes = minutes % 60
        time_s += "" + hours + ":"
        if minutes < 10
            time_s += "0"

    time_s += "" + minutes + ":"
    # zero-padding
    time_s += if seconds < 10 then '0' else ''
    time_s += seconds
    time_s

Array::remove = (e) -> @[t..t] = [] if (t = @indexOf(e)) > -1
