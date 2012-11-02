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

# Fix transitions (i.e. turn them off)
$(document).bind "mobileinit", () ->
    $.mobile.defaultPageTransition = "none"

$ ->
    window.Partify = window.Partify || {}
    window.Partify.Player = new Player()
    window.Partify.Player.initPlayerVisuals = initPlayerVisuals
    window.Partify.Player.init()
    window.Partify.Queues = window.Partify.Queues || {}
    window.Partify.Queues.GlobalQueue = new MobileGlobalQueue($("#global_queue"), $("#up_next_list"))
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

    # Hack up the navbar to make it work as expected.
    # I'm already feeling unsure about jQuery mobile...
    $("div[data-role='page']").each (idx, page) ->
        page_id = $(page).attr('id')

        $(page).find("a[href='#" + page_id + "']").addClass("ui-btn-active ui-state-persist")

initPlayerVisuals = () ->

# Define a custom progressbar component that can be used like jQueryUI's progressbar
$.fn.extend
    progressbar: (options) ->
        value = options.value

        $(this).find(".progress_fill").css("width", value + "%")


# Redefine both of our Queues based on the API that is consistent wit hthe web interface
class MobileQueue
    constructor: (queue_element) ->
        @tracks = new Array()
        @queue_element = queue_element

    update: (tracks) ->
        @tracks = new Array()
        @tracks.push new Track(track) for track in tracks
        this.updateDisplay()

    updateDisplay: () ->
        @queue_element.empty()
        @queue_element.append this._buildDisplayItem(track) for track in @tracks
        @queue_element.listview('refresh')

    _buildDisplayItem: (track_) ->
        track = $.extend(true, {}, track_)
        track.length = secondsToTimeString(track_.length)
        track.user_url = buildRoboHashUrlFromId(track.username, 25, 25)

        output = $.Mustache.render('small-queue-item', {track: track})
        output_element = $(output)

        popupdiv = output_element.find("div")
        popupdiv.find("a[data-role='button']").buttonMarkup()
        popupdiv.popup()
        output_element.find("a").click () ->
            popupdiv.popup("open")

        getAlbumImage(track, "large", (url) ->
            popupdiv.find("img.album_image").attr("src", url)
        , (code, message) ->
            console.log "Failed to fetch album image for track #{track}"
        )

        return output_element


class MobileGlobalQueue extends MobileQueue
    constructor: (queue_element, up_next_div) ->
        super queue_element
        @up_next_div = up_next_div

    updateDisplay: () ->
        @queue_element.empty()
        @up_next_div.empty()

        @up_next_div.append (_, __) =>
            (this._buildLargeDisplayItem(track) for track in @tracks[1..3])

        @queue_element.append (_, __) =>
            (this._buildDisplayItem(track) for track in @tracks[4..])

        this._updateNowPlayingUser(@tracks[0])

        # update the now playing information
        if @tracks[0]?
            getAlbumImage(@tracks[0], "large", (url) ->
                $("#now_playing_artist_image").attr('src', url)
            , (code, message) ->
                $("#now_playing_artist_image").attr('src', "http://debbiefong.com/images/10%20t.jpg")
            )
        else
            $("#now_playing_artist_image").attr('src', "http://debbiefong.com/images/10%20t.jpg")

        @queue_element.listview('refresh')
        @up_next_div.listview('refresh')

    _buildLargeDisplayItem: (track_) ->
        track = $.extend(true, {}, track_)
        track.length = secondsToTimeString(track_.length)
        track.user_url = buildRoboHashUrlFromId(track.username, 25, 25)

        output = $.Mustache.render('large-queue-item', {track: track})
        output_element = $(output)

        popupdiv = output_element.find("div")
        popupdiv.find("a[data-role='button']").buttonMarkup()
        popupdiv.popup()
        output_element.find("a").click () ->
            popupdiv.popup("open")

        getAlbumImage(track, "large", (url) ->
            output_element.find("img.album_image").attr("src", url)
            popupdiv.find("img.album_image").attr("src", url)
        , (code, message) ->
            console.log "Failed to fetch album image for track #{track}"
        )
        return output_element

    _updateNowPlayingUser: (track) ->
        this._updateNowPlayingAvatar(track)
        $("#played_by_container #player_info_user_name").text(track?.user)

    _updateNowPlayingAvatar: (track) ->
        if track?
            src = buildRoboHashUrlFromId(track.username, 25, 25)
        else
            src = ""

        $("#played_by_container img").attr("src", src)

