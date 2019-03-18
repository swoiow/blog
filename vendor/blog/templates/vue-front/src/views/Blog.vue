<template>
  <v-content>
    <v-container fill-height>
      <v-layout align-center row wrap>
        <LeftBox v-if="showNav"></LeftBox>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
  import LeftBox from '@/components/LeftBox'

  export default {
    name: "Blog",
    components: {
      LeftBox,
    },
    data() {
      return {}
    },
    mounted: function () {
      let vm = this;

      vm.$store.commit('setNav', true)
    },
    computed: {
      showNav: function () {
        let vm = this;

        return vm.$store.state.hasNav;
      }
    }
  }
</script>

<style scoped>

</style>
