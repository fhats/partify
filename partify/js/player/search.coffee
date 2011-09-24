$ = jQuery

$ ->
    window.Partify = window.Partify || {}
    window.Partify.Search = new Search()

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
            method: 'GET'
            data: request_data
            success: (data) =>
                if data.status == 'ok'
                    @results.push new Track(result) for result in data.results
                    this.updateResultsDisplay()
        )
    
    updateResultsDisplay: () ->
        this.buildResultRow(track) for track in @results

    buildResultRow: (track) ->
        row_html = "
        <tr>
            <td>#{track.title}</td>
            <td>#{track.artist}</td>
            <td>#{track.album}</td>
        </tr>
        "
        console.log row_html
        @results_display.append row_html


    _show_wait_spinner: () ->
        @results_display.empty()

# TODO: Need a Track class to hold track result information that isn't necessarily displayed (like Spotify URI...)
class Track
    @title = ""
    @artist = ""
    @album = ""
    @track = ""
    @file = ""
    @time = ""
    @date = ""

    constructor: (data) ->
        @title = data.title
        @artist = data.artist
        @album = data.album
        @track = data.track
        @file = data.file
        @time = data.time
        @date = data.date