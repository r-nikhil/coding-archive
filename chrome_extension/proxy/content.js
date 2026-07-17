chrome.browserAction.onClicked.addListener(function(tab) {
    //var url1 = encodeURIComponent(tab.url);

var url3 = new URL(tab.url);
if(url3.path){
var url4 = url3.host+"/"+url3.path;
}
else{var url4 = url3.host}


  var newURL = "https://bitsproxy.appspot.com/" + url4;

    chrome.tabs.update(tab.id, {url: newURL});
});





