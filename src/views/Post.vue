<template>
  <PostBox />
</template>

<script>
import PostBox from '@/components/PostBox'

export default {
  name: 'Post',
  components: {
    PostBox
  },
  mounted: function () {
    let vm = this

    vm.$store.commit('setNav', false)
  }
}
</script>

<style scoped>

</style>
