<template>
  <v-system-bar>
    <v-toolbar-side-icon
      @click.stop="detail =! detail"
      @mouseover="detail = 0"
      @mouseleave="detail = 1"
    />

    <v-toolbar-items
      :class="[detail ? 'hidden-screen-only' : '']"
      @mouseover="detail = 0"
      @mouseleave="detail = 1"
    >
      <v-btn
        color="blue-grey darken-3"
        flat
        href="/blog"
      >
        Posts
      </v-btn>

      <v-btn
        color="blue-grey darken-3"
        flat
        href="/api/tags"
      >
        Tags
      </v-btn>

      <v-btn
        color="blue-grey darken-3"
        flat
        :href="this.$route.path+'/@edit'"
      >
        Edit
      </v-btn>
    </v-toolbar-items>
  </v-system-bar>
</template>

<script>
export default {
  name: 'Toolbar',
  data () {
    return {
      detail: true
    }
  }
}
</script>

<style scoped>

</style>
