chrome.browserAction.onClicked.addListener(function(tab) {
var base = "https://hellobuddy.in/search/products/?flipkartURL=";
var url = tab.url;
var final = base + url;
chrome.tabs.create({ url: final });
});
