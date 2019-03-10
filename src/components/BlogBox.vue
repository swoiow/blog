<!-- 右侧栏，博客列表页 -->

<template>
  <v-container
    :fill-height="!posts.length"
    fluid
    v-on="$listeners"
  >
    <v-layout
      class="px-5"
      column
    >
      <v-flex
        v-if="posts.length > 0 && show"
        align-self-end
      >
        <toolbar />
      </v-flex>

      <v-flex class="blog-items">
        <div
          v-if="posts.length > 0 && show"
          class="typo"
        >
          <router-link
            v-for="post in posts"
            :key="post.id"
            :to="'/post/'+post._id"
            class="blog-item"
            tag="div"
          >
            <v-card
              class="my-3 post-item"
              hover
            >
              <v-card-title :data-sid="post._id">
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

        <v-layout
          v-else
          align-center
          fill-height
          justify-center
          row
        >
          <h2 class="mb-5">
            No posts here.
          </h2>
        </v-layout>
      </v-flex>

      <v-layout
        v-if="posts.length > 0 && batch"
        justify-space-around
      >
        <v-btn
          color="primary"
          flat
          light
          small
          @click="Nav('prev')"
        >
          Prev
        </v-btn>
        <v-btn
          color="primary"
          flat
          light
          small
          @click="Nav('next')"
        >
          Next
        </v-btn>
      </v-layout>
    </v-layout>
  </v-container>
</template>

<script>
import toolbar from '@/components/toolbar'

var qs = require('qs')

export default {
  name: 'BlogBox',
  components: {
    toolbar
  },
  data () {
    return {
      show: false,
      posts: [],
      batch: [],
      page: 1
    }
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  created: function () {
    let vm = this
    vm.fetchData()
    vm.$data.show = true
  },
  methods: {
    fetchData: function () {
      let vm = this

      // 考虑不丢弃通用参数. ref: https://segmentfault.com/q/1010000016064754
      let query = vm.$route.query
      let paramas = '?' + qs.stringify(query)
      vm.$http.get(vm.$gc.H + '/api/posts' + paramas)
        .then(function (response) {
          vm.$data.posts = JSON.parse(response.data[0])
          vm.$data.batch = JSON.parse(response.data[1])
        })

      return true
    },

    Nav: function (target) {
      let vm = this

      switch (target) {
        case 'prev':
          vm.$data.page = vm.$data.batch[0][0]
          break
        case 'next':
          vm.$data.page = vm.$data.batch[1][0]
          break
        default:
          vm.$data.page = 1
      }

      let query = vm.$route.query

      let newQy = JSON.parse(JSON.stringify(query))
      newQy.page = vm.$data.page

      vm.$router.replace({ path: '/blog', query: newQy })
    }
  }
}
</script>

<style scoped>
  .post-item {
    border-radius: .5rem;
  }
</style>
