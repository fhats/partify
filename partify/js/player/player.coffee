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
    # Initial setup of the Player object and namespacing within front-end
    window.Partify = window.Partify || {}
    window.Partify.Player = new Player()
    window.Partify.Player.init()
    window.Partify.Queues = window.Partify.Queues || {}
    window.Partify.Queues.GlobalQueue = window.Partify.Queues.GlobalQueue || {}
    window.Partify.Search = new Search()
    window.Partify.Search.skin_add_btns()
    window.Partify.Statistics = new Statistics($("#stats_widget"))
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
    window.Partify.History = new History($("#history_widget"))
