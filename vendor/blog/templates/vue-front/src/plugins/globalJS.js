/*
* axios
* */
import Vue from 'vue'

const axios = Vue.prototype.$http;

axios.defaults.xsrfCookieName = "_xsrf";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

axios.interceptors.response.use(function (response) {
  if ("location1" in response.headers) {
    return window.location.href = response.headers.location1;
  } else if ("location" in response.headers) {
    return window.location.href = response.headers.location;
  } else {
    return response;
  }
}, function (error) {
  return Promise.reject(error);
});


/*
 * others
 * */

var loadDeferredStyles = function () {
  var addStylesNode = document.getElementById("deferred-styles");
  var replacement = document.createElement("div");
  replacement.innerHTML = addStylesNode.textContent;
  document.body.appendChild(replacement);
  addStylesNode.parentElement.removeChild(addStylesNode);
};
var raf = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
if (raf) raf(function () {
  window.setTimeout(loadDeferredStyles, 0);
});
else window.addEventListener('load', loadDeferredStyles);
