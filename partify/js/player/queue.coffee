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
    window.Partify = window.Partify || {}
    window.Partify.Queues = window.Partify.Queues || {}
    window.Partify.Queues.GlobalQueue = new GlobalQueue($("#party_queue"), $("#up_next_tracks"))
    window.Partify.Queues.UserQueue = new UserQueue($("#user_queue"))
    window.Partify.Config = window.Partify.Config || {};
    window.Partify.Config.lastFmApiKey = config_lastfm_api_key;           # The backticks here mean pass the content through as vanilla JS rather than being compiled
    window.Partify.Config.lastFmApiSecret = config_lastfm_api_secret;     # I used them here to pass the {{}} template content through the coffeescript compiler.
    window.Partify.Config.user_id = config_user_id;
    window.Partify.LastCache = new LastFMCache()
    window.Partify.LastFM = new LastFM
        apiKey: window.Partify.Config.lastFmApiKey
        apiSecret: window.Partify.Config.lastFmApiSecret
        cache: window.Partify.LastCache

class Queue
    # Class responsible for encapsulating the tracks in each queue and for updating the display of those queues
    constructor: (queue_div) ->
        @tracks = new Array()
        @queue_div = queue_div
        @queue_div.sortable
            placeholder: "queue-placeholder"
            forcePlacerHolderSize: true
            axis: 'y'
            cancel: 'li.queue_header, li.queue_footer'
            opacity: 0.8
            items: "li.queue_item_sortable"
        @queue_div.disableSelection()
        @queue_div.addClass 'queue'

    update: (tracks) ->
        @tracks = new Array()
        @tracks.push new Track(track) for track in tracks
        this.updateDisplay()

    updateDisplay: () ->
        @queue_div.empty()
        @queue_div.append this._buildDisplayHeader()
        @queue_div.append this._buildDisplayItem(track) for track in @tracks
        @queue_div.append this._buildDisplayFooter()
    
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
        <li class='queue_item queue_item_sortable ui-state-default small span-23 last'>
            <span class='span-1 ui-icon ui-icon-grip-dotted-vertical grip'>&nbsp;</span>
            <span class='span-6'>#{track.title}</span>
            <span class='span-6'>#{track.artist}</span>
            <span class='span-6'>#{track.album}</span>
            <span class='span-3'>#{track.user}</span>
            <span class='span-1 last right'>#{secondsToTimeString(track.length)}</span>
        </li>
        "

    _buildDisplayFooter: () ->
        if @tracks.length > 0
            this._buildQueueSummary()
        else
            this._buildNoItemsRow()
        
    _buildQueueSummary: () ->
        total_queue_time = (t.length for t in @tracks).reduce (a,b) -> a + b
        "
        <li class='queue_item queue_footer ui-state-default small span-23 last'>
            <span class='span-23 last'><center><p>#{@tracks.length} tracks - #{ secondsToTimeString(total_queue_time) }</p></center></span>
        </li>
        "

    _buildNoItemsRow: () ->
        "
        <li class='queue_item queue_footer ui-state-default small span-23 last'>
            <span class='span-23 last'><center><p ><em>There's nothing in this queue right now!</em></p></center></span>
        </li>
        "

    _buildAvatarImage: (username) ->
        "
        <img id='player_info_user_avatar' src='#{ buildRoboHashUrlFromId(username, 70, 70) }' />
        "

    removeTrack: (track) ->
        $.ajax(
            url: '/queue/remove'
            type: 'POST'
            data:
                track_id: track.mpd_id
            success: (data) =>
                if data.status == 'ok'
                    @tracks.remove(track)
                    this.updateDisplay()
                    window.Partify.Player._synchroPoll()
            error: () =>
                console.log "Could not contact the server!"
        )


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

        # Update the user playing the track
        $("#player_info_user_name").empty()
        $("#player_info_skip_div").empty()
        $("#user_avatar_container").empty()
        if @tracks.length > 0
            $("#player_info_user_name").append @tracks[0].user
            $("#user_avatar_container").append this._buildAvatarImage(@tracks[0].username)

            if @tracks[0].user_id == window.Partify.Config.user_id
                $("#player_info_skip_div").append "<a href='#' id='player_skip_btn'>Skip My Track</a>"
                $("#player_skip_btn").click (e) =>
                    this.removeTrack(@tracks[0])
                    e.stopPropagation()
                    $("#player_skip_btn").remove()

            # Update the now playing artist picture
            window.Partify.LastFM.artist.getInfo 
                artist: @tracks[0].artist
            , 
            {
                success: (data) =>
                    images = data.artist?.image
                    if images?
                        console.log 'Got images'
                        image_sizes = (image.size for image in images)
                        preferred_sizes = ['large', 'medium', 'small']
                        preferred_sizes.remove size for size in preferred_sizes when size not in image_sizes
                        target_size = preferred_sizes[0]
                        img_url = (image['#text'] for image in images when image.size == target_size)
                        img_url = img_url[0]
                        $('#now_playing_artist_image').attr 'src', img_url
                , error: (code, message) =>
                    console.log "#{code} - #{message}"
            }
        else
            $('#now_playing_artist_image').attr 'src', "http://debbiefong.com/images/10%20t.jpg"

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
        <li class='queue_item queue_item_sortable ui-state-default small span-23 last'>
            <span class='span-1 padder'>&nbsp;</span>
            <span class='span-6'>#{track.title}</span>
            <span class='span-6'>#{track.artist}</span>
            <span class='span-6'>#{track.album}</span>
            <span class='span-3'>#{track.user}</span>
            <span class='span-1 right'>#{secondsToTimeString(track.length)}</span>
            <span class='span-1 last padder'>&nbsp;</span>
        </li>
        "

    _buildPlayerImage: (src) ->
        "
       <img id='now_playing_artist_image' class='span-3' src='#{src}' />
        "

    _buildUpNextDisplayItem: (track, last) ->
        comma = if last then '' else ', '
        "#{track.artist} - #{track.title}#{comma}"

class UserQueue extends Queue
    constructor: (queue_div) ->
        super queue_div
        @queue_div.bind 'sortupdate', (e, ui) =>
            track_list = {}
            priority = 0
            if @tracks[0].id == window.Partify.Queues.GlobalQueue.tracks[0].id
                priority = 2
                track_list[@tracks[0].id] = 1
            else
                priority = 1
            for track in @queue_div.children("li.queue_item").children('input')
                do (track) =>
                    target_track_id = parseInt($(track).val())
                    track_obj = t for t in @tracks when t.id == target_track_id
                    track_list[track_obj.id] = priority
                    priority++
            console.log track_list

            $.ajax(
                url: 'queue/reorder'
                type: 'POST'
                data: track_list
                success: (data) ->
                    if data.status == 'ok'
                        console.log 'Everything worked out'
                    else
                        this.error()
                error: () =>
                    console.log 'Error reordering the queue!'
                    this.loadPlayQueue()
            )

        # Load the user's queue on page load
        this.loadPlayQueue()
    
    loadPlayQueue: () ->
        $.ajax(
            url: 'queue/list'
            type: 'GET'
            success: (data) =>
                if data.status == "ok"
                    this.update data.result
            error: () =>
                console.log "Failed to populate user play queue!"
        )
    
    updateDisplay: () ->
        @queue_div.empty()
        @queue_div.append this._buildDisplayHeader()
        @queue_div.append this._buildDisplayItem(track) for track in @tracks when track.id != window.Partify.Queues.GlobalQueue.tracks[0].id
        @queue_div.append this._buildDisplayFooter()
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
        <li class='queue_item queue_item_sortable ui-state-default small span-23 last'>
            <input type='hidden' name='id' value='#{track.id}'>
            <span class='span-1 ui-icon ui-icon-grip-dotted-vertical grip'>&nbsp;</span>
            <span class='span-7'>#{track.title}</span>
            <span class='span-6'>#{track.artist}</span>
            <span class='span-6'>#{track.album}</span>
            <span class='span-2'>#{secondsToTimeString(track.length)}</span>
            <span class='span-1 right last'><button id='rm_#{track.id}' class='rm_btn'></button></span>
        </li>"

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

buildRoboHashUrlFromId = (id, dimension_x, dimension_y) ->
    "http://robohash.org/#{id}.png?size=#{dimension_x}x#{dimension_y}&set=any&bgset=any"
