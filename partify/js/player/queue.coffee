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
    window.Partify.Config.lastFmApiKey = config_lastfm_api_key;
    window.Partify.Config.lastFmApiSecret = config_lastfm_api_secret;
    window.Partify.Config.user_id = config_user_id;
    window.Partify.Config.voting_enabled = config_voting_enabled;
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
            <span class='span-1 padder'>&nbsp;</span>
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
            <span class='span-1 padder'>&nbsp;</span>
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

        if window.Partify.Config.voting_enabled
            this._buildVotingButtons()

        # Update the user playing the track
        $("#player_info_user_name").empty()
        $("#player_info_skip_div").empty()
        $("#player_info_vote_div").empty()
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
            else if window.Partify.Config.voting_enabled
                this._buildPlayerVoteButtons(@tracks[0].id)

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
        user_width = 3
        album_width = 6
        voting_hdr = ""
        if window.Partify.Config.voting_enabled
            user_width = 2
            album_width = 5
            voting_hdr = "<span class='span-2'>Vote</span>"
        "
        <li class='queue_header span-23 last'>
            <span class='span-1 padder'>&nbsp;</span>
            <span class='span-6'>Title</span>
            <span class='span-6'>Artist</span>
            <span class='span-#{album_width}'>Album</span>
            <span class='span-#{user_width}'>User</span>
            #{voting_hdr}
            <span class='span-1 right'>Time</span>
            <span class='span-1 last padder'>&nbsp;</span>
        </li>
        "

    _buildDisplayItem: (track) ->
        user_width = 3
        album_width = 6
        voting_section = ""
        if window.Partify.Config.voting_enabled
            user_width = 2
            album_width = 5
            if track.user_id != window.Partify.Config.user_id
                voting_section = "
                <span class='span-2'><button class='vote_up_button'></button>
                <button class='vote_down_button'></button></span>
                "
            else
                voting_section = "<span class='span-2'>&nbsp;</span>"
        "
        <li class='queue_item queue_item_sortable ui-state-default small span-23 last'>
            <input type='hidden' name='id' value='#{track.id}'>
            <span class='span-1 padder'>&nbsp;</span>
            <span class='span-6'>#{track.title}</span>
            <span class='span-6'>#{track.artist}</span>
            <span class='span-#{album_width}'>#{track.album}</span>
            <span class='span-#{user_width}'>#{track.user}</span>
            #{voting_section}
            <span class='span-1 right'>#{secondsToTimeString(track.length)}</span>
            <span class='span-1 last padder'>&nbsp;</span>
        </li>
        "

    _buildVotingButtons: () ->
        $("li.queue_item span button.vote_up_button").each (idx, up_btn) ->
            id = $(up_btn).parents("span").first().siblings("input:hidden").first().attr 'value'
            id = parseInt(id)

            $(up_btn).button
                icons:
                    primary: "ui-icon-circle-arrow-n"
            
            $(up_btn).click (e) ->
                e.stopPropagation()
                btn = $(e.currentTarget)
                btn.button 'disable'
                btn.button 'option', 'icons',
                    primary: 'ui-icon-loading'
                $.ajax(
                    url: "/vote/up"
                    type: 'POST'
                    data:
                        pqe: id
                    success: (data) ->
                        if data.status == "ok"
                            btn.button 'option', 'icons',
                                primary: "ui-icon-circle-arrow-n"
                            btn.siblings(".vote_down_button").first().button 'enable'
                            if id == window.Partify.Queues.GlobalQueue.tracks[0].id
                                $("button#player_info_vote_up").button 'disable'
                                $("button#player_info_vote_down").button 'enable'
                        else
                            this.error()
                    error: () =>
                        btn.button 'enable'
                        btn.button 'option', 'icons',
                            primary: "ui-icon-circle-arrow-n"
                )
        $("li.queue_item span button.vote_down_button").each (idx, dwn_btn) ->
            id = $(dwn_btn).parents("span").first().siblings("input:hidden").first().attr 'value'
            id = parseInt(id)

            $(dwn_btn).button
                icons:
                    primary: "ui-icon-circle-arrow-s"
            
            $(dwn_btn).click (e) ->
                e.stopPropagation()
                btn = $(e.currentTarget)
                btn.button 'disable'
                btn.button 'option', 'icons',
                    primary: 'ui-icon-loading'
                $.ajax(
                    url: "/vote/down"
                    type: 'POST'
                    data:
                        pqe: id
                    success: (data) ->
                        if data.status == "ok"
                            btn.button 'option', 'icons',
                                primary: "ui-icon-circle-arrow-s"
                            btn.siblings(".vote_up_button").first().button 'enable'
                            if id == window.Partify.Queues.GlobalQueue.tracks[0].id
                                console.log $("button#player_info_vote_down")
                                $("button#player_info_vote_down").button 'disable'
                                $("button#player_info_vote_up").button 'enable'
                        else
                            this.error()
                    error: () =>
                        btn.button 'enable'
                        btn.button 'option', 'icons',
                            primary: "ui-icon-circle-arrow-s"
                )
        $("li.queue_item input:hidden").each (idx, id_input) ->
            id = $(id_input).attr 'value'
            id = parseInt(id)

            $.ajax(
                url: "/vote/status"
                type: 'GET'
                data:
                    pqe: id
                success: (data) ->
                    if data.direction == -1
                        $(id_input).parents("li").first().children("span").children("button.vote_down_button").button 'disable'
                        if id == window.Partify.Queues.GlobalQueue.tracks[0].id
                            $("button#player_info_vote_down").button 'disable'
                            $("button#player_info_vote_up").button 'enable'
                    if data.direction == 1
                        $(id_input).parents("li").first().children("span").children("button.vote_up_button").button 'disable'
                        if id == window.Partify.Queues.GlobalQueue.tracks[0].id
                            console.log 
                            $("button#player_info_vote_up").button 'disable'
                            $("button#player_info_vote_down").button 'enable'
            )


    _buildPlayerImage: (src) ->
        "
       <img id='now_playing_artist_image' class='span-3' src='#{src}' />
        "

    _buildUpNextDisplayItem: (track, last) ->
        comma = if last then '' else ', '
        "#{track.artist} - #{track.title}#{comma}"

    _buildPlayerVoteButtons: (pqe_id) ->
        $("#player_info_vote_div").append "
        <span class='darker'>Vote on this track:</span><br />
        <button id='player_info_vote_up' class='vote_up_button'></button>
        <button id='player_info_vote_down' class='vote_down_button'></button>
        "

        $("button#player_info_vote_up").button
            icons:
                primary: "ui-icon-circle-arrow-n"
        $("button#player_info_vote_down").button
            icons:
                primary: "ui-icon-circle-arrow-s"

        $.ajax(
            url: "/vote/status"
            type: 'GET'
            data:
                pqe: pqe_id
            success: (data) ->
                if data.direction == -1
                    $("button#player_info_vote_down").button 'disable'
                if data.direction == 1
                    $("button#player_info_vote_up").button 'disable'
        )

        $("button#player_info_vote_up").click (e) ->
            e.stopPropagation()
            btn = $(e.currentTarget)
            btn.button 'disable'
            btn.button 'option', 'icons',
                primary: 'ui-icon-loading'
            $.ajax(
                url: "/vote/up"
                type: 'POST'
                data:
                    pqe: pqe_id
                success: (data) ->
                    if data.status == "ok"
                        btn.button 'option', 'icons',
                            primary: "ui-icon-circle-arrow-n"
                        $("button#player_info_vote_down").button 'enable'
                        window.Partify.Queues.GlobalQueue.queue_div.children("li.queue_item").first().children("span").children("button.vote_down_button").button 'enable'
                        window.Partify.Queues.GlobalQueue.queue_div.children("li.queue_item").first().children("span").children("button.vote_up_button").button 'disable'
                    else
                        this.error()
                error: () =>
                    btn.button 'enable'
                    btn.button 'option', 'icons',
                        primary: "ui-icon-circle-arrow-n"
            )   
        $("button#player_info_vote_down").click (e) ->
            e.stopPropagation()
            btn = $(e.currentTarget)
            btn.button 'disable'
            btn.button 'option', 'icons',
                primary: 'ui-icon-loading'
            $.ajax(
                url: "/vote/down"
                type: 'POST'
                data:
                    pqe: pqe_id
                success: (data) ->
                    if data.status == "ok"
                        btn.button 'option', 'icons',
                            primary: "ui-icon-circle-arrow-s"
                        $("button#player_info_vote_up").button 'enable'
                        window.Partify.Queues.GlobalQueue.queue_div.children("li.queue_item").first().children("span").children("button.vote_up_button").button 'enable'
                        window.Partify.Queues.GlobalQueue.queue_div.children("li.queue_item").first().children("span").children("button.vote_down_button").button 'disable'
                    else
                        this.error()
                error: () =>
                    btn.button 'enable'
                    btn.button 'option', 'icons',
                        primary: "ui-icon-circle-arrow-s"
            )    

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

class HistoryQueue extends Queue
    constructor: (queue_div) ->
        super queue_div
        @queue_div.sortable 'option', 'disabled', true

    updateDisplay: () ->
        @queue_div.empty()
        @queue_div.append this._buildDisplayHeader()
        @queue_div.append this._buildDisplayItem(track) for track in @tracks
        if @tracks.length == 0
            @queue_div.append this._buildNoItemsRow()
    
    _buildDisplayHeader: () ->
        "
        <li class='queue_header span-23 last'>
            <span class='span-1 padder'>&nbsp;</span>
            <span class='span-6'>Title</span>
            <span class='span-5'>Artist</span>
            <span class='span-5'>Album</span>
            <span class='span-2'>User</span>
            <span class='span-4 last right'>Played</span>
        </li>
        "

    _buildDisplayItem: (track) ->
        "
        <li class='queue_item queue_item_sortable ui-state-default small span-23 last'>
            <span class='span-1 padder'>&nbsp;</span>
            <span class='span-6'>#{track.title}</span>
            <span class='span-5'>#{track.artist}</span>
            <span class='span-5'>#{track.album}</span>
            <span class='span-2'>#{track.user}</span>
            <span class='span-4 last right timeago' title='#{(track.time_played)}'>now</span>
        </li>
        "

    _buildNoItemsRow: () ->
        "
        <li class='queue_item queue_footer ui-state-default small span-23 last'>
            <span class='span-23 last'><center><p ><em>No tracks have been played yet. Make history... be the first!</em></p></center></span>
        </li>
        "

buildRoboHashUrlFromId = (id, dimension_x, dimension_y) ->
    "http://robohash.org/#{id}.png?size=#{dimension_x}x#{dimension_y}&set=any&bgset=any"
