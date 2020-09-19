function validateURL(url) {
    if(!url.includes("youtube.com/watch?v=")) { return false; }
    return true;
}

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


function getData() {
    var initialURL = document.getElementById('link').value;
    if(!validateURL(initialURL)) {
        console.log(document.getElementById('editor').value);
        alert('URL is not valid!');
        return;
    }

    initialURL = initialURL.substr(initialURL.indexOf('v=')+2);
    var videoID = initialURL.substr(0, initialURL.indexOf('&'));

    var player = new YT.Player('player', {
        height: '100%',
        width: '100%',
        videoId: videoID,
        events: {
            'onReady': onPlayerReady,
        }
    });
}

function onPlayerReady(event) {
    var player = event.target;
    player.playVideo();

    const interval = setInterval(function() {
        console.log(player.getCurrentTime());
        // Use the timestamp dictionary to change information view
      }, 5000);
}