navigator.getUserMedia = navigator.webkitGetUserMedia ;// This webkitGetUserMedia is for chrome.

var constraints = {audio: false, video: true}; //constraints to ask for a video-only MediaStream:

var video = document.querySelector("video");

function successCallback(stream) {

  window.stream= stream; // this is for console logging. you can inspect the stream variable later to know details


    video.src = window.URL.createObjectURL(stream);
    // converts media stream into blob url(for other browsers you use video.src=stream directly)

  video.play(); // this plays the video.
}
function errorCallback(error){
  console.log("navigator.getUserMedia error: ", error);
}
// just call getUserMedia() on the navigator object
navigator.getUserMedia(constraints, successCallback, errorCallback);
