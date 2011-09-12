(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  self.addEventListener('message', __bind(function(e) {
    var source;
    source = new EventSource('/player/status/idle');
    return source.addEventListener('player', __bind(function(e) {
      var data;
      data = JSON.parse(e.data);
      return self.postMessage(data);
    }, this), false);
  }, this), false);
}).call(this);
