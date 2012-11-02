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
	$.Mustache.add("small-queue-item", small_queue_item_template)
	$.Mustache.add("large-queue-item", large_queue_item_template)


popup_template = "
<div data-role='popup' id='popup-{{track.id}}' class='ui-content' style='max-width:280px'>
	<a href='#' data-rel='back' data-role='button' data-theme='a' data-icon='delete' data-iconpos='notext' class='ui-btn-right'>Close</a>
	<p><img class='album_image' src=''></p>
	<p><strong>Track:</strong> {{track.title}}</p>
	<p><strong>Artist:</strong> {{track.artist}}</p>
	<p><strong>Album:</strong> {{track.album}}</p>
	<p><strong>Year:</strong> {{track.date}}</p>
	<p><strong>Time:</strong> {{track.length}}</p>
	<p><strong>Queued by:</strong> <img class='avatar_image' src='{{track.user_url}}' />{{track.user}}</p>
	<a href='' data-role='button'>Search for Album</a>
	<a href='' data-role='button'>Search for Artist</a>
	<a href='#' data-rel='back' data-role='button' data-theme='a'>Close</a>
</div>
"

small_queue_item_template = "
<li data-icon='info'>
	<a data-rel='popup' href='#popup-{{track.id}}'>
		{{track.artist}} - {{track.title}}
	</a>
	#{popup_template}
</li>
"

large_queue_item_template = "
<li data-icon='info' class='large_queue_item'>
	<a data-rel='popup' href='#popup-{{track.id}}'>
		<img width=80 height=80 class='album_image middle_image' />
		<h3>{{track.title}}</h3>
		<p>{{track.artist}}</p>
		<p>{{track.album}}</p>
	</a>
	#{popup_template}
</li>
"

