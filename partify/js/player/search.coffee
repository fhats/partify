$ = jQuery

$ ->
    window.Partify = window.Partify || {}
    window.Partify.Search = new Search()
    window.Partify.Search.skin_add_btns()

class Search
    @results = new Array()
    @results_display

    constructor: () ->
        this.initializeFormHandlers()
        @results_display = $("table#results_table > tbody")
        @results = new Array()

    initializeFormHandlers: () ->
        $("#track_search_form").submit (e) =>
            e.stopPropagation()
            title = $("input#search_title").val()
            artist = $("input#search_artist").val()
            album = $("input#search_album").val()
            this.processSearch title, artist, album
            return false

    processSearch: (title, artist, album) ->
        @results = new Array()
        this._show_wait_spinner()

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
            <td class='small'><button class='add_btn'></button></td>
        </tr>
        "
        @results_display.append row_html
    
    buildEmptyResultRow: () ->
        row_html = "
        <tr>
            <td colspan='4' class='results_empty small'>
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
            <td colspan='4' class='results_empty'>
                <center><img src='/static/img/loading.gif'></img></center>
            </td>
        </tr>
        ")

# TODO: Need a Track class to hold track result information that isn't necessarily displayed (like Spotify URI...)
class Track
    @title = ""
    @artist = ""
    @album = ""
    @track = ""
    @file = ""
    @time = ""
    @date = ""
    @mpd_id = 0

    constructor: (data) ->
        @title = data.title
        @artist = data.artist
        @album = data.album
        @track = data.track
        @file = data.file
        @time = data.time
        @date = data.date
        if data.mpd_id
            @mpd_id = data.mpd_id
