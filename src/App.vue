<template>
  <v-app>
    <v-navigation-drawer
      id="blog-nav"
      v-model="drawer"
      :mini-variant.sync="model"
      app
    >
      <LeftBox />
    </v-navigation-drawer>

    <v-toolbar
      v-if="!drawer"
      dense
      fixed
      style="width: 50px"
    >
      <v-toolbar-side-icon @click.stop="drawer =! drawer" />
      <!--<v-toolbar-title>Vuetify</v-toolbar-title>-->
    </v-toolbar>

    <v-content id="blog-content">
      <keep-alive>
        <router-view v-if="$route.meta.keepAlive">
          <!-- 这里是会被缓存的视图组件 -->
        </router-view>
      </keep-alive>

      <router-view v-if="!$route.meta.keepAlive">
        <!-- 这里是不被缓存的视图组件 -->
      </router-view>
    </v-content>

    <Footer id="blog-footer" />
  </v-app>
</template>

<script>
import LeftBox from '@/components/LeftBox'
import Footer from '@/components/Footer'

export default {
  name: 'App',
  components: {
    // Blog,
    LeftBox,
    Footer
  },
  data () {
    return {
      drawer: true,
      model: null
    }
  }
}
</script>

<style>
  html {
    overflow-y: auto;
  }

  #blog-nav {
    /*background-color: #fdf6e3;*/
    background-color: rgba(253, 246, 227, 0.8);
  }

  /*#blog-content {*/
  /*background-color: #eee8d5 !important;*/
  /*background: rgba(245, 245, 213, .5) !important;*/
  /*}*/

  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  /* 滚动槽 */
  ::-webkit-scrollbar-track {
    /*-webkit-box-shadow:inset 0 0 6px rgba(0,0,0,0.3);*/
    border-radius: 10px;
  }

  /* 滚动条滑块 */
  ::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.1);
    /*-webkit-box-shadow:inset 0 0 6px rgba(0,0,0,0.5);*/
  }

  ::-webkit-scrollbar-thumb:window-inactive {
    background: rgba(255, 0, 0, 0.2);
  }
</style>
