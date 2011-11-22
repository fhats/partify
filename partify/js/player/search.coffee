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
                    this.sortResultsBy @sortmode.category, "artist", "album", "track", @sortmode.asc
        
    sortResultsBy: (categories..., is_ascending) ->
        sortfn = (a,b) -> 
            cmp_val = 0
            for category in categories when cmp_val is 0
                do (category) ->     
                    if a[category] < b[category]
                        cmp_val = -1
                    if a[category] > b[category]
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
        @sortmode = {category: "", asc: true}
        
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
                btn = row.children('td.result_add').children('button')
                if data.status == 'ok'
                    btn.button 'option', 'icons',
                        primary: 'ui-icon-check'
                    # Update the user's play queue (global updates will come with the synchropoll)
                    window.Partify.Player._synchroPoll()
                    window.Partify.Queues.UserQueue.update data.queue
                else
                    this._addTrackFail(btn)
            error: () =>
                this._addTrackFail(row.children('td.result_add').children('button'))
            
        )
    
    addAlbum: (spotify_url, album_tracks) ->
        this.disableButton $("tr[id='#{album_tracks[0].file}'] > td.result_album > button")
        this.disableRow $("tr[id='#{track.file}']") for track in album_tracks
        spotify_files = (track.file for track in album_tracks)
        $.ajax(
            url: '/queue/add_album'
            type: 'POST'
            data:
                spotify_files: spotify_files
            traditional: 'true'
            success: (data) ->
                if data.status == 'ok'
                    $("tr[id='#{album_tracks[0].file}'] > td.result_album > button").button 'option', 'icons',
                        primary: 'ui-icon-check'
                    for track in album_tracks
                        do (track) ->
                            $("tr[id='#{track.file}'] > td.result_add > button").button 'option', 'icons',
                                primary: 'ui-icon-check'
                    window.Partify.Player._synchroPoll()
                    window.Partify.Queues.UserQueue.update data.queue
                else
                    this.error()
            error: () =>
                this._addTrackFail $("tr[id='#{album_tracks[0].file}'] > td.result_album > button")
                this._addTrackFail $("tr[id='#{track.file}'] > td.result_add > button") for track in album_tracks
        )
    
    _addTrackFail: (btn) ->
        btn.addClass 'ui-state-error'
        btn.button 'option', 'icons',
           primary: 'ui-icon-alert'
    
    updateResultsDisplay: () ->
        # TODO: Clean this up...
        @results_display.empty()
        if @results.length > 0
            this.buildResultRow(track) for track in @results
            if @sortmode.category != "title"
                # If we can, group the album listing to show the album cover art as well as the name
                # The length metrics were determined empirically
                for track, pos in @results
                    do (track, pos) =>
                        album_length = (t for t in @results when t.album == track.album).length
                        if album_length > 4
                            if track.album == @results[Math.max(pos-1, 0)].album and track.file != @results[Math.max(pos-1, 0)].file
                                $("tr[id='#{track.file}'] > td.result_album").remove()
                            else
                                $("tr[id='#{track.file}'] > td.result_album").attr 'rowspan', album_length 
                                $("tr[id='#{track.file}'] > td.result_album").addClass 'album_details'
                                $("tr[id='#{track.file}'] > td.result_album").empty()
                                d = new Date(track.date)
                                year = d.getFullYear()
                                year_str = if year > 0 then "(" + year + ")" else ""
                                
                                $("tr[id='#{track.file}'] > td.result_album").append "
                                <img id='#{track.file}' src='/static/img/loading.gif' />
                                <p>#{track.album} #{year_str}</p>
                                <button class='album_add_btn'>Add Album</button>
                                "
                                
                                # This needs to be bound for later because of the stupid way Javascript handles 'this'
                                # Apparently Coffeescript doesn't handle this, either...
                                last_track = @results[(pos + album_length - 1)]
                                console.log last_track

                                # Find album art from Last.fm
                                window.Partify.LastFM.album.getInfo 
                                    artist: track.artist,
                                    album: track.album
                                , 
                                {
                                    success: (data) ->
                                        images = data.album?.image
                                        if images?
                                            image_sizes = (image.size for image in images)
                                            target_size = "large"
                                            if target_size in image_sizes
                                                img_url = (image['#text'] for image in images when image.size == target_size)
                                                img_url = img_url[0]
                                                $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").attr 'src', img_url
                                                $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").bind 'load', (e) ->
                                                    $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").addClass 'album_image'
                                                    $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").attr 'width', 174
                                                    $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").attr 'height', 174
                                                    if 4 < album_length < 8
                                                        console.log $("tr[id='#{last_track.file}']")
                                                        $("tr[id='#{last_track.file}']").after "<tr class='album_padding'><td colspan=5>&nbsp;</td></tr>"
                                                        $("tr[id='#{track.file}'] > td.result_album").attr 'rowspan', album_length + 1
                                                if img_url == ""
                                                    $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").remove()
                                    , error: (code, message) =>
                                        $("tr[id='#{track.file}'] > td.result_album > img[id='#{track.file}']").remove()
                                }
                                
                                # Set up the button to add the album to the queue
                                $("tr[id='#{track.file}'] > td.result_album > button").button(
                                    icons:
                                        primary: 'ui-icon-plus'
                                    , text: true
                                )
                                $("tr[id='#{track.file}'] > td.result_album > button").click (e) =>
                                    this.addAlbum track.file, @results[pos...(pos+album_length)]

                        if track.album != @results[Math.max(pos-1, 0)].album
                            $("tr[id='#{track.file}'] > td").addClass 'album_seperator'

                        
        else
            this.buildEmptyResultRow()
        this.skin_add_btns()

    buildResultRow: (track) ->
        row_html = "
        <tr id='#{track.file}'>
            <td class='small result_album'>#{track.album}</td>
            <td class='small result_artist'>#{track.artist}</td>
            <td class='small result_title'>#{track.title}</td>
            <td class='small result_time'>#{secondsToTimeString(track.time)}</td>
            <td class='small result_track'>#{track.track}</td>
            <td class='small result_add'><button class='add_btn'></button></td>
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
        this.disableButton row.children('td.result_add').children('button')
        
    disableButton: (btn) ->
        btn.button 'disable'
        btn.button 'option', 'icons',
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
