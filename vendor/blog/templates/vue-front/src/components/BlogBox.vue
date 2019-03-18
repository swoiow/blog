<!-- 右侧栏，博客列表页 -->

<template>
  <v-container :fill-height="!posts.length" fluid>
    <v-layout class="px-5" column>
      <v-flex align-self-end v-if="posts.length > 0 && show">
        <toolbar></toolbar>
      </v-flex>

      <v-flex class="blog-items">
        <div class="typo" v-if="posts.length > 0 && show">
          <router-link :key="post.id"
                       :to="'/post/'+post._id"
                       class="blog-item"
                       tag="div"
                       v-for="post in posts">

            <v-card class="my-3" hover >
              <v-card-title v-bind:data-sid="post._id">
                <div class="headline">
                  {{ post.title }}
                </div>
              </v-card-title>

              <v-card-text class="text--grey-lighten-3">
                <i> {{ post.description }} </i>
              </v-card-text>

              <!--<v-card-actions>-->
              <!--<v-spacer></v-spacer>-->
              <!--<v-btn color="brown lighten-2" flat>Read More</v-btn>-->
              <!--</v-card-actions>-->
            </v-card>
          </router-link>
        </div>

        <v-layout align-center fill-height justify-center row v-else>
          <h2 class="mb-5">No posts here.</h2>
        </v-layout>
      </v-flex>

      <v-layout justify-space-around v-if="posts.length > 0 && batch">
        <v-btn @click="Nav('prev')" color="primary" flat light small>
          Prev
        </v-btn>
        <v-btn @click="Nav('next')" color="primary" flat light small>
          Next
        </v-btn>
      </v-layout>
    </v-layout>
  </v-container>
</template>

<script>
  import toolbar from '@/components/toolbar'

  var qs = require('qs');

  export default {
    name: "BlogBox",
    components: {
      toolbar
    },
    data() {
      return {
        show: false,
        posts: [],
        batch: [],
        page: 1,
      }
    },
    created: function () {
      let vm = this;
      vm.fetchData();
      vm.$data.show = true
    },
    watch: {
      // 如果路由有变化，会再次执行该方法
      '$route': 'fetchData'
    },
    methods: {
      showPost: function () {
        let vm = this;

        vm.$router.push({name: "blog", query: {p: vm.$data.page}});
      },
      fetchData: function () {
        let paramas;
        let vm = this;

        // 考虑不丢弃通用参数. ref: https://segmentfault.com/q/1010000016064754
        let query = vm.$route.query;
        let queryString = '';

        for (let key in query) {
          if (key !== 'p') {
            queryString += `&${key}=${query[key]}`
          } else {
            vm.$data.page = query[key]
          }
        }

        paramas = "?" + qs.stringify({page: vm.$data.page});
        vm.$http.get(vm.$gc.H + "/api/posts" + paramas)
          .then(function (response) {

            vm.$data.posts = JSON.parse(response.data[0]);
            vm.$data.batch = JSON.parse(response.data[1])
          });

        return true
      },
      Nav: function (target) {
        let vm = this;

        if (target === "prev") {
          vm.$data.page = vm.$data.batch[0][0];
        } else if (target === "next") {
          vm.$data.page = vm.$data.batch[1][0];
        }

        vm.$router.push({name: "blog", query: {p: vm.$data.page}});

        // vm.$data.show = false;
        // vm.fetchData();
        // vm.$data.show = true
      },
    }
  }
</script>

<style scoped>

</style>
