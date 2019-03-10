import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    hasNav: true
  },
  mutations: {
    setNav (state, st) {
      state.hasNav = st
    }
  }
})

export default store
