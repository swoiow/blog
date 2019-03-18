import Vue from 'vue'

// https://cli.vuejs.org/zh/guide/mode-and-env.html
Vue.prototype.$gc = {
  H: process.env.VUE_APP_BLOG_HOST,
  domain: process.env.VUE_APP_BLOG_HOST,
};

// css async
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
