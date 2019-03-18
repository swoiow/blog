<template>
  <v-footer absolute app id="footer-side" inset>
    <div class=" px-3 copyright">
      &copy; {{ new Date().getFullYear() }}
      >>>
      Using <a href="https://www.python.org/"
               target="_blank">Python</a>
      &
      <a href="https://vuetifyjs.com/zh-Hans/themes/premium"
         target="_blank">Vuetify</a>
    </div>
  </v-footer>
</template>

<script>
  export default {
    name: 'Footer',
    data() {
      return {}
    }
  }
</script>

<style scoped>
  #footer-side a {
    text-decoration: none;
  }
</style>
