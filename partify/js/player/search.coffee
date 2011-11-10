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
    window.Partify.Search = new Search()
    window.Partify.Search.skin_add_btns()

class Search
    @results = new Array()
    @results_display
    @sortmode = {category: "", asc: true}

    constructor: () ->
        this.initializeFormHandlers()
        this.initializeSortHandlers()
        @results_display = $("table#results_table > tbody")
        @results = new Array()
        @sortmode = {category: "", asc: true}

    initializeFormHandlers: () ->
        $("#track_search_form").submit (e) =>
            e.stopPropagation()
            title = $("input#search_title").val()
            artist = $("input#search_artist").val()
            album = $("input#search_album").val()
            this.processSearch title, artist, album
            return false

    initializeSortHandlers: () ->
        for category in ['title', 'artist', 'album']
            do (category) =>
                $("#results_header_" + category).click (e) =>
                    e.stopPropagation()
                    if @sortmode.category == category
                        @sortmode.asc = !@sortmode.asc
                    else
                        @sortmode.category = category
                        @sortmode.asc = true
                    this.sortResultsBy @sortmode.category, @sortmode.asc
        
    sortResultsBy: (category, is_ascending, sub_category = "track") ->
        sortfn = (a,b) -> 
            cmp_val = 0
            if a[category] < b[category]
                cmp_val = -1
            if a[category] > b[category]
                cmp_val = 1
            if cmp_val == 0
                if a[sub_category] < b[sub_category]
                    cmp_val = -1
                if a[sub_category] > b[sub_category]
                    cmp_val = 1
            return cmp_val
        @results.sort sortfn
        if !is_ascending
            @results.reverse()
        this.updateResultsDisplay()
        this.setSortIndicator()

    setSortIndicator: () ->
        this.clearSortIndicators()
        $("#results_header_" + @sortmode.category).append "<span id='sort_indicator_arrow' class='ui-icon ui-icon-triangle-1-#{if @sortmode.asc then 'n' else 's'} grip' style='float:left'>&nbsp;</span>"

    clearSortIndicators: () ->
        $("#sort_indicator_arrow").remove()

    processSearch: (title, artist, album) ->
        @results = new Array()
        this._show_wait_spinner()
        this.clearSortIndicators()

        request_data = {}
        if title != ""
            request_data['title'] = title
        if artist != ""
            request_data['artist'] = artist
        if album != ""
            request_data['album'] = album

        $.ajax(
            url: '/track/search'
            type: 'GET'
            data: request_data
            success: (data) =>
                if data.status == 'ok'
                    @results.push new Track(result) for result in data.results
                    this.updateResultsDisplay()
                else
                    this.updateResultsDisplay()
        )

    addTrack: (spotify_url, row) ->
        $.ajax(
            url: '/queue/add'
            type: 'POST'
            data:
                spotify_uri: spotify_url
            success: (data) =>
                btn = row.children('td').children('button')
                if data.status == 'ok'
                    btn.button 'option', 'icons',
                        primary: 'ui-icon-check'
                    # Update the user's play queue (global updates will come with the synchropoll)
                    window.Partify.Player._synchroPoll()
                    window.Partify.Queues.UserQueue.update data.queue
                else
                    this._addTrackFail(btn)
            error: () =>
                this._addTrackFail(row.children('td').children('button'))
            
        )
    
    _addTrackFail: (btn) ->
        btn.addClass 'ui-state-error'
        btn.button 'option', 'icons',
           primary: 'ui-icon-alert'
    
    updateResultsDisplay: () ->
        @results_display.empty()
        if @results.length > 0
            this.buildResultRow(track) for track in @results
        else
            this.buildEmptyResultRow()
        this.skin_add_btns()

    buildResultRow: (track) ->
        row_html = "
        <tr id='#{track.file}'>
            <td class='small'>#{track.title}</td>
            <td class='small'>#{track.artist}</td>
            <td class='small'>#{track.album}</td>
            <td class='small'>#{secondsToTimeString(track.time)}</td>
            <td class='small'>#{track.track}</td>
            <td class='small'><button class='add_btn'></button></td>
        </tr>
        "
        @results_display.append row_html
    
    buildEmptyResultRow: () ->
        row_html = "
        <tr>
            <td colspan='6' class='results_empty small'>
                <center><em>No results found. Please try a different search using the form above.</em></center>
            </td>
        </tr>"
        @results_display.append row_html

    skin_add_btns: () ->
        $("button.add_btn").button(
            icons: 
                primary: 'ui-icon-plus'
            , text: false
        )
        $("button.add_btn").click (e) =>
            track_row = $(e.currentTarget).parent('td').parent('tr').first()
            spotify_url = track_row.attr 'id'
            this.disableRow track_row
            this.addTrack spotify_url, track_row

    disableRow: (row) ->
        row.children('td').children('button').button 'disable'
        row.children('td').children('button').button 'option', 'icons',
            primary: 'ui-icon-loading'


    _show_wait_spinner: () ->
        @results_display.empty()
        @results_display.append("
        <tr>
            <td colspan='6' class='results_empty'>
                <center><img src='/static/img/loading.gif'></img></center>
            </td>
        </tr>
        ")

class Track
    @id = 0
    @title = ""
    @artist = ""
    @album = ""
    @track = ""
    @file = ""
    @time = ""
    @date = ""
    @length = ""
    @user = ""
    @user_id = 0
    @playback_priority = 0
    @user_priority = 0
    @mpd_id = 0

    constructor: (data) ->
        @id = parseInt(data.id) or data.id
        @title = data.title
        @artist = data.artist
        @album = data.album
        @track = parseInt(data.track) or data.track
        @file = data.file
        @time = parseInt(data.time) or data.time
        @date = data.date
        @length = data.length
        @user = data.user
        @username = data.username
        @user_id = data.user_id
        @playback_priority = data.playback_priority
        @user_priority = data.user_priority
        if data.mpd_id
            @mpd_id = data.mpd_id
