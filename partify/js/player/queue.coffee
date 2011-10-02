$ = jQuery

$ ->
    window.Partify = window.Partify || {}
    window.Partify.Queues = window.Partify.Queues || {}
    window.Partify.Queues.GlobalQueue = new GlobalQueue($("#party_queue"), $("#up_next_tracks"))
    window.Partify.Queues.UserQueue = new UserQueue($("#user_queue"))

class Queue
    # Class responsible for encapsulating the tracks in each queue and for updating the display of those queues
    constructor: (queue_div) ->
        @tracks = new Array()
        @queue_div = queue_div
        @queue_div.sortable
        	placeholder: "queue-placeholder"
        	forcePlacerHolderSize: true
        	axis: 'y'
        	cancel: 'li.queue_header'
        	opacity: 0.8
        	items: "li.queue_item"
        @queue_div.disableSelection()
        @queue_div.addClass 'queue'

    update: (tracks) ->
        @tracks = new Array()
        @tracks.push new Track(track) for track in tracks
        this.updateDisplay()

    updateDisplay: () ->
        @queue_div.empty()
        @queue_div.append this._buildDisplayHeader()
        @queue_div.append this._buildDisplayItem(track) for track in @tracks[1..-1]
    
    _buildDisplayHeader: () ->
    	"
    	<li class='queue_header span-23 last'>
    		<span class='span-1 ui-icon ui-icon-arrowthick-2-n-s grip'>&nbsp;</span>
    		<span class='span-6'>Title</span>
	        <span class='span-6'>Artist</span>
	        <span class='span-6'>Album</span>
	        <span class='span-3'>User</span>
	        <span class='span-1 last right'>Len</span>
    	</li>
    	"

    _buildDisplayItem: (track) ->
        "
        <li class='queue_item ui-state-default small span-23 last'>
        	<span class='span-1 ui-icon ui-icon-grip-dotted-vertical grip'>&nbsp;</span>
            <span class='span-6'>#{track.title}</span>
	        <span class='span-6'>#{track.artist}</span>
	        <span class='span-6'>#{track.album}</span>
	        <span class='span-3'>#{track.user}</span>
	        <span class='span-1 last right'>#{secondsToTimeString(track.length)}</span>
        </li>
        "

class GlobalQueue extends Queue
	constructor: (queue_div, up_next_div) ->
		super queue_div
		@up_next_div = up_next_div
		@queue_div.sortable 'option', 'disabled', true
	
	updateDisplay: () ->
		super()
		@up_next_div.empty()
		up_next_dsp = @tracks[1..3]
		@up_next_div.append this._buildUpNextDisplayItem(track, track.mpd_id==up_next_dsp[-1..-1][0].mpd_id) for track in up_next_dsp

	_buildDisplayHeader: () ->
    	"
    	<li class='queue_header span-23 last'>
    		<span class='span-1 padder'>&nbsp;</span>
    		<span class='span-6'>Title</span>
	        <span class='span-6'>Artist</span>
	        <span class='span-6'>Album</span>
	        <span class='span-3'>User</span>
	        <span class='span-1 right'>Time</span>
	       	<span class='span-1 last padder'>&nbsp;</span>
    	</li>
    	"

    _buildDisplayItem: (track) ->
        "
        <li class='queue_item ui-state-default small span-23 last'>
        	<span class='span-1 padder'>&nbsp;</span>
            <span class='span-6'>#{track.title}</span>
	        <span class='span-6'>#{track.artist}</span>
	        <span class='span-6'>#{track.album}</span>
	        <span class='span-3'>#{track.user}</span>
	        <span class='span-1 right'>#{secondsToTimeString(track.length)}</span>
	        <span class='span-1 last padder'>&nbsp;</span>

        </li>
        "

	_buildUpNextDisplayItem: (track, last) ->
		comma = if last then '' else ', '
		"#{track.artist} - #{track.title}#{comma}"

class UserQueue extends Queue
	constructor: (queue_div) ->
		super queue_div
		# Load the user's queue on page load
		@queue_div.bind 'sortupdate', (e, ui) ->
			console.log "Sort event!"
			console.log e
			console.log ui

		this.loadPlayQueue()
	
	loadPlayQueue: () ->
		$.ajax(
			url: 'queue/list'
			type: 'GET'
			success: (data) =>
				if data.status == "ok"
					this.update data.result
			error: () =>
				alert "Failed to populate user play queue!"
		)
	
	updateDisplay: () ->
		super()
		this._createRemoveButtons()

	_buildDisplayHeader: () ->
    	"
    	<li class='queue_header span-23 last'>
    		<span class='span-1 ui-icon ui-icon-arrowthick-2-n-s grip'>&nbsp;</span>
    		<span class='span-7'>Title</span>
	        <span class='span-6'>Artist</span>
	        <span class='span-6'>Album</span>
	        <span class='span-2 '>Time</span>
	        <span class='span-1 last padder'>&nbsp;</span>
    	</li>
    	"

    _buildDisplayItem: (track) ->
        html = "
        <li class='queue_item ui-state-default small span-23 last'>
        	<span class='span-1 ui-icon ui-icon-grip-dotted-vertical grip'>&nbsp;</span>
            <span class='span-7'>#{track.title}</span>
	        <span class='span-6'>#{track.artist}</span>
	        <span class='span-6'>#{track.album}</span>
	        <span class='span-2'>#{secondsToTimeString(track.length)}</span>
	        <span class='span-1 right last'><button id='rm_#{track.id}' class='rm_btn'></button></span>
        </li>"

    removeTrack: (track) ->
    	$.ajax(
    		url: 'queue/remove'
    		type: 'POST'
    		data:
    			track_id: track.mpd_id
    		success: (data) =>
    			if data.status == 'ok'
    				@tracks.remove(track)
    				this.updateDisplay()
    		error: () =>
    			alert "Could not contact the server!"
    	)

	_createRemoveButtons: () ->
    	this._createRemoveButton track for track in @tracks

    _createRemoveButton: (track) ->
    	rm_btn = $('button#rm_' + track.id)
    	rm_btn.button
    		icons:
    			primary: 'ui-icon-close'
    		text: false
    	rm_btn.click (e) =>
    		rm_btn.button 'disable'
    		rm_btn.button 'option', 'icons',
    			primary: 'ui-icon-loading'
    		this.removeTrack(track)
