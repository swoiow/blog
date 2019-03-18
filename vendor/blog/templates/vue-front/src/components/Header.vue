<template>
  <v-card color="grey lighten-4"
          flat
  >
    <v-toolbar color="grey darken-1" dark>
      <v-toolbar-side-icon></v-toolbar-side-icon>

      <v-menu :nudge-width="100">
        <v-toolbar-title slot="activator">
          <span>All</span>
          <v-icon dark>arrow_drop_down</v-icon>
        </v-toolbar-title>

        <v-list>
          <v-list-tile :key="item"
                       v-for="item in items"
          >
            <v-list-tile-title v-text="item"></v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>

      <v-spacer></v-spacer>

      <v-btn href="/logout" icon>
        <v-icon>logout</v-icon>
      </v-btn>
    </v-toolbar>
  </v-card>
</template>

<script>
  export default {
    name: "Header",
    data: () => ({
      items: [
        "首页", "文章管理", "标签管理", "个人中心"
      ]
    })
  }
</script>

<style scoped>

</style>
