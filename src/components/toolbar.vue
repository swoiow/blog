<template>
  <v-system-bar>
    <!--fixed-->
    <v-toolbar-side-icon @click.stop="detail =! detail" />

    <!--<v-toolbar-items class="hidden-screen-only">-->
    <v-toolbar-items :class="[detail ? 'hidden-sm-and-down' : '']">
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
