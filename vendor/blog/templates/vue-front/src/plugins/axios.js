import Vue from 'vue'
import axios from 'axios'


axios.defaults.xsrfCookieName = "_xsrf"
axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded"

axios.interceptors.response.use(function (response) {
  if ("location1" in response.headers) {
    return window.location.href = response.headers.location1
  } else if ("location" in response.headers) {
    return window.location.href = response.headers.location
  } else {
    return response
  }
}, function (error) {
  return Promise.reject(error)
})

Vue.prototype.$http = axios
