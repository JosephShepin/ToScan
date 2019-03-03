document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('test');
    // onClick's logic below:
    link.addEventListener('click', function() {


          chrome.tabs.query({'active': true, 'lastFocusedWindow': true, 'currentWindow': true}, function (tabs) {
        var url = tabs[0].url;
        url = url.replace("https://", "");
        url = url.replace("http://", "");
        for(i=0; i<255; i++) {
          url = url.replace(new RegExp('/'), "-slash-");
        }
        chrome.tabs.create({'url':"http://76.29.91.11:3003/ScanTosExtention/" + url});
    });


    });
});
