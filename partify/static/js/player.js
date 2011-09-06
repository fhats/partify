$(function(){
    $("#player_progress").progressbar({
        value: 0
    });

    $("#tabs").tabs();

    initPlayer();
});

function initPlayer(){
    if (!!window.EventSource) {
        var source = new EventSource('/player/status');
        source.addEventListener('message', function(e){
            console.log(e.data);
        }, false);
        source.addEventListener('open', function(e) {
            console.log("Connection opened");
        }, false);
        source.addEventListener('error', function(e) {
            if (e.eventPhase == EventSource.CLOSED) {
                console.log("Connection closed.");
            }
        }, false);
    } 
    else {
        // Result to xhr polling :(
        // OR NOTHING
    }
}