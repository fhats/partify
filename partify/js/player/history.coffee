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
	window.Partify.History = new History($("#history_widget"))

class History
	# A widget for displaying paginated, automatically updating history
	constructor: (widget_div) ->
		@widget_div = widget_div
		@last_update_time = 0
		@ipp = 10
		@page = 1
		@total_pages = 1
		@in_flight_xhr = undefined

		@widget_div.append "<span id='history_last_updated' class='small darker left'><span id='history_update_prefix'>Last updated </span><span class='timeago' id='timeago'>never</span></span>"
		
		this._buildIppSelectors()

		@widget_div.append "<ul id='history_queue'></ul>"
		@widget_div.append "<span id='page_info' class='small darker left'></span>"
	
		this._buildPageSelector()

		@queue = new HistoryQueue($("ul#history_queue"))
		@queue.updateDisplay()

		this.update()

		# Schedule an update of the history every five minutes
		setInterval () =>
			this.update()
		, 1000 * 60 * 5

	update: () ->
		# Indicate that an update is in progress
		this._showUpdateSpinner()

		if @in_flight_xhr
			@in_flight_xhr.abort()
			@in_flight_xhr = undefined

		@in_flight_xhr = $.ajax(
			url: '/history'
			method: 'GET'
			data:
				ipp: @ipp
				page: @page
			success: (data) =>
				if data.status == 'ok'
					@queue.update(data.tracks)
					@last_update_time = data.response_time
					@page = data.page
					@total_pages = data.pages
					this._updateUpdateTime()
					this._updatePageInfo data.page, data.pages
					this._updatePageSelector()
		)

	_updatePageInfo: (displayed_page, total_pages) ->
		page_info = $("span#page_info")
		page_info.empty()
		page_info.append "Page #{displayed_page} of #{total_pages}"

	_updatePageSelector: () ->
		page_left_btn = $("span#page_selector button#page_left")
		page_right_btn = $("span#page_selector button#page_right")
		page_display = $("span#page_selector span#page_display")

		if @page == 1
			page_left_btn.button 'disable'
		else
			page_left_btn.button 'enable'
		if @page == @total_pages
			page_right_btn.button 'disable'
		else
			page_right_btn.button 'enable'
		
		page_display.text @page


	_showUpdateSpinner: () ->
		$("span#history_last_updated > span").empty()
		$("span#history_last_updated > span#history_update_prefix").append "
			<img src='/static/img/loading.gif' class='left' style='margin-right: 5px' />
			Updating...
		"
	
	_updateUpdateTime: () ->
		$("span#history_last_updated > span").empty()
		$("span#history_last_updated > span#history_update_prefix").append "Last updated "
		$("span#history_last_updated > span#timeago").remove()
		$("span#history_last_updated").append "
		<span class='timeago' id='timeago'>never</span>"
		$("span#history_last_updated > span#timeago").attr 'title', @last_update_time
		$("span.timeago").timeago()

	_buildIppSelectors: () ->
		@widget_div.append "<span id='ipp_selector' class='small darker right'>
			<span id='ipp_10'>10</span>&nbsp;
			<a href='#'><span id='ipp_25'>25</span></a>&nbsp;
			<a href='#'><span id='ipp_50'>50</span></a>&nbsp;
			<a href='#'><span id='ipp_100'>100</span></a>&nbsp;
			items per page
			</span>"
		this._buildIppSelectorLinks()

	_buildPageSelector: () ->
		@widget_div.append "<span id='page_selector' class='small right'>
			<button id='page_left'></button>
			<span id='page_display'>#{@page}</span>
			<button id='page_right'></button>
		</span>"

		$("span#page_selector button#page_left").button(
			icons:
				primary: 'ui-icon-carat-1-w'
			text: false
		)
		$("span#page_selector button#page_right").button(
			icons:
				primary: 'ui-icon-carat-1-e'
			text: false
		)

		$("span#page_selector button#page_left").click (e) =>
			@page = Math.max(@page - 1, 1)
			this._updatePageSelector()
			this.update()

		$("span#page_selector button#page_right").click (e) =>
			@page = Math.min(@page + 1, @total_pages)
			this._updatePageSelector()
			this.update()
		
	_buildIppSelectorLinks: () ->
		$("span#ipp_selector a").click (e) =>
			e.stopPropagation()
			$("span#ipp_selector > span#ipp_#{@ipp}").wrap "<a href='#'></a>"
			ipp_span = $(e.currentTarget).children("span").first()
			ipp_span.unwrap()
			
			# Figure out what the page would be given the new IPP
			proposed_ipp = parseInt(ipp_span.text())
			@page = (Math.floor(((@page-1) * @ipp) / proposed_ipp)) + 1

			@ipp = proposed_ipp
			this.update()
			$("span#ipp_selector a").unbind 'click'
			this._buildIppSelectorLinks()
