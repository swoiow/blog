import Vue from 'vue'

// https://cli.vuejs.org/zh/guide/mode-and-env.html
Vue.prototype.$gc = {
  H: process.env.VUE_APP_BLOG_HOST,
  domain: process.env.VUE_APP_BLOG_HOST
}

// css async
const loadDeferredStyles = function () {
  let addStylesNode = document.getElementById('deferred-styles')
  let replacement = document.createElement('div')
  replacement.hidden = true
  replacement.innerHTML = addStylesNode.textContent
  document.body.appendChild(replacement)
  addStylesNode.parentElement.removeChild(addStylesNode)
}
const raf = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame || window.msRequestAnimationFrame
if (raf) {
  raf(function () {
    window.setTimeout(loadDeferredStyles, 0)
  })
} else window.addEventListener('load', loadDeferredStyles)
