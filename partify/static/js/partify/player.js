(function() {
  var $, initPlayer, initPlayerUpdating, initPlayerVisuals, updatePlayerInfo, _initPlayerPushUpdates, _initPlayerSynchroPolling, _synchroPollAndSchedule, _updatePlayerInfo, _updatePlayerProgress;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  $ = jQuery;
  $(function() {
    return initPlayer();
  });
  initPlayer = function() {
    initPlayerVisuals();
    return initPlayerUpdating();
  };
  initPlayerVisuals = function() {
    $("#player_progress").progressbar({
      value: 0
    });
    return $("#tabs").tabs();
  };
  initPlayerUpdating = function() {
    _initPlayerPushUpdates();
    return _initPlayerSynchroPolling(5000);
  };
  _initPlayerPushUpdates = function() {
    var worker;
    worker = new Worker('static/js/partify/workers/player_event.js');
    worker.addEventListener('message', __bind(function(e) {
      return console.log(e.data);
    }, this), false);
    return worker.postMessage('Hello world!');
  };
  _initPlayerSynchroPolling = function(poll_frequency) {
    return setInterval(__bind(function() {
      return _synchroPollAndSchedule();
    }, this), poll_frequency);
  };
  _synchroPollAndSchedule = function() {
    return $.ajax({
      url: 'player/status/poll',
      method: 'GET',
      success: __bind(function(data) {
        return updatePlayerInfo(data);
      }, this)
    });
  };
  updatePlayerInfo = function(data) {
    _updatePlayerInfo('track', data.title);
    _updatePlayerInfo('artist', data.artist);
    _updatePlayerInfo('album', data.album);
    return _updatePlayerProgress(Math.round((data.elapsed / data.time) * 100));
  };
  _updatePlayerInfo = function(info_key, data) {
    var info_span;
    info_span = $("#player_info_" + info_key).first();
    return info_span.text(data);
  };
  _updatePlayerProgress = function(progress) {
    return $("#player_progress").progressbar({
      value: progress
    });
  };
}).call(this);
