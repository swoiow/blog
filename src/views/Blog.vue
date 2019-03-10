<template>
  <v-content>
    <v-container fill-height>
      <v-layout
        align-center
        row
        wrap
      >
        <LeftBox v-if="showNav" />
        <keep-alive>
          <router-view />
        </keep-alive>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import LeftBox from '@/components/LeftBox'

export default {
  name: 'Blog',
  components: {
    LeftBox
  },
  data () {
    return {}
  },
  computed: {
    showNav: function () {
      let vm = this

      return vm.$store.state.hasNav
    }
  },
  mounted: function () {
    let vm = this

    vm.$store.commit('setNav', true)
  }
}
</script>

<style scoped>

</style>
