import Vue from 'vue'
import './plugins/vuetify'
import Auth from './App.vue'

Vue.config.productionTip = false;

new Vue({
  render: h => h(Auth),
}).$mount('#app');


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
