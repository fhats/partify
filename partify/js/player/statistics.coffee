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
	window.Partify.Statistics = new Statistics($("#stats_widget"))

class Statistics
	constructor: (widget_div) ->
		@widget_div = widget_div
		@last_update_time = 0
		@in_flight_xhr = undefined
		@deferred_images = new Array()

		@widget_div.append "<span id='statistics_last_updated' class='small darker left'><span id='statistics_update_prefix'>Last updated </span><span class='timeago' id='timeago'>never</span></span>"
		@widget_div.append "<div id='stats_container' class='span-23 last'></div>"

		this.update()

		# Update statistics every 15 minutes
		setInterval () =>
			this.update()
		, (1000 * 60 * 15)

	update: () ->
		# Indicate that an update is in progress
		this._showUpdateSpinner()

		@in_flight_xhr = $.ajax(
			url: '/statistics'
			method: 'GET'
			success: (data) =>
				if data.status == 'ok'
					@last_update_time = data.response_time
					this._updateUpdateTime()
					this.updateStatisticsDisplay data
		)

	updateStatisticsDisplay: (data) ->
		statistics = data.statistics
		stats_container = $("div#stats_container")
		stats_container.empty()

		this._buildStatisticsTimeSection statistics.day, "Today", stats_container
		this._buildStatisticsTimeSection statistics.week, "This Week", stats_container
		this._buildStatisticsTimeSection statistics.month, "This Month", stats_container
		this._buildStatisticsTimeSection statistics.year, "This Year", stats_container
		this._buildStatisticsTimeSection statistics.all, "All Time", stats_container

	_buildStatisticsTimeSection: (section, label, stats_container) ->
		stats_container.append "
		<h4>#{label}</h4>
		"

		label = label.replace(" ", "_")
		stats_container.append "<div class='stat_border span-23 last append-bottom' id='#{label}_container'>
			<div class='span-23 last append-bottom'><span class='small'>#{section.total_tracks} tracks played (#{secondsToTimeString(section.total_time)})</span></div>
			</div>"

		stats_container = $("div##{label}_container")

		this._buildStatisticsSegment(section.top_artists, 'artists', stats_container, label)
		this._buildStatisticsSegment(section.top_albums, 'albums', stats_container, label)
		this._buildStatisticsSegment(section.top_users, 'users', stats_container, label)

	_buildStatisticsSegment: (segment, type, stats_container, label) ->
		segment_vpad = if type == "users" then "" else "append-bottom"
		stats_container.append "
		<div class='span-23 last #{segment_vpad}'><h5>Top #{type}</h5></div>"

		segment_container = stats_container.children("div").last()

		max_rank = Math.max((rank for rank, e of segment)...)
		if max_rank > 0
			if type == "artists"
				this._buildTopArtist segment[rank].artist, segment[rank].plays, rank, segment_container, label for rank in [1..max_rank]
			else if type == "albums"
				this._buildTopAlbum segment[rank].artist, segment[rank].plays, segment[rank].album, rank, segment_container, label for rank in [1..max_rank]
			else if type == "users"
				this._buildTopUser segment[rank].username, segment[rank].user, segment[rank].plays, rank, segment_container, label for rank in [1..max_rank]
			segment_container.append "<div class='span-#{ ((5 - max_rank) * 5) + 3} last'>&nbsp;</div>"
		else
			this._buildNoData segment_container


	_buildTopArtist: (artist, plays, rank, segment_container, label) ->
		segment_container.append "
		<div class='span-5'>
			<div class='span-5 last top_stat'><span>#{artist}</span></div>
			<div class='span-5 last'><span class='darker'>#{plays} plays</span></div>
			<img class='span-5 last' id='#{label}_top_artist_#{rank}' src />
		</div>
		"
		this._buildArtistImage artist, $("img##{label}_top_artist_#{rank}")

	_buildTopAlbum: (artist, plays, album, rank, segment_container, label) ->
		segment_container.append "
		<div class='span-5'>
			<div class='span-5 last top_stat'><span>#{album}</span></div>
			<div class='span-5 last top_stat'><span class='darker'>by </span><span>#{artist}</span></div>
			<div class='span-5 last'><span class='darker'>#{plays} plays</span></div>
			<img class='span-5 last' id='#{label}_top_album_#{rank}' />
		</div>
		"
		this._buildAlbumImage artist, album, $("img##{label}_top_album_#{rank}")
	
	_buildTopUser: (username, user, plays, rank, segment_container, label) ->
		segment_container.append "
		<div class='span-5'>
			<div class='span-5 last top_stat'><span>#{user}</span></div>
			<div class='span-5 last'><span class='darker'>#{plays} plays</span></div>
			<img id='#{label}_top_user_#{rank}' />
		</div>
		"
		this._buildUserImage username, $("img##{label}_top_user_#{rank}")

	_buildArtistImage: (artist, img_element) ->
		window.Partify.LastFM.artist.getInfo
			artist: artist
		,
		{
			success: (data) =>
				images = data.artist?.image
				if images?
					image_sizes = (image.size for image in images)
					preferred_sizes = ['extralarge', 'large', 'medium', 'small']
					preferred_sizes.remove size for size in preferred_sizes when size not in image_sizes
					target_size = preferred_sizes[0]
					img_url = (image['#text'] for image in images when image.size == target_size)
					img_url = img_url[0]
					
					img_element.attr 'src', img_url
			, error: (code, message) =>
				console.log "#{code} - #{message}"
		}

	_buildAlbumImage: (artist, album, img_element) ->
		window.Partify.LastFM.album.getInfo 
			artist: artist
			album: album
		, 
		{
			success: (data) ->
				images = data.album?.image
				if images?
					image_sizes = (image.size for image in images)
					preferred_sizes = ['large', 'medium', 'small']
					preferred_sizes.remove size for size in preferred_sizes when size not in image_sizes
					target_size = preferred_sizes[0]
					img_url = (image['#text'] for image in images when image.size == target_size)
					img_url = img_url[0]
					
					img_element.attr 'src', img_url
			, error: (code, message) =>
				console.log "#{code} - #{message}"
		}

	_buildUserImage: (user, img_element) ->
		img_element.attr 'src', buildRoboHashUrlFromId(user, 190, 190)

	_showUpdateSpinner: () ->
		$("span#statistics_last_updated > span").empty()
		$("span#statistics_last_updated > span#statistics_update_prefix").append "
			<img src='/static/img/loading.gif' class='left' style='margin-right: 5px' />
			Updating...
		"

	_updateUpdateTime: () ->
		$("span#statistics_last_updated > span").empty()
		$("span#statistics_last_updated > span#statistics_update_prefix").append "Last updated "
		$("span#statistics_last_updated > span#timeago").remove()
		$("span#statistics_last_updated").append "
		<span class='timeago' id='timeago'>never</span>"
		$("span#statistics_last_updated > span#timeago").attr 'title', @last_update_time
		$("span.timeago").timeago()