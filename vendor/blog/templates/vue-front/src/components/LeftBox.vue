<template>
  <v-container fluid>
    <v-layout align-center fill-height justify-center mt-5 row>
      <v-flex>
        <div class="text-xs-center">
          <a href="/dashboard">
            <v-avatar size="125px">
              <img class="img-circle elevation-7 mb-1" v-bind:src="avatar">
            </v-avatar>
          </a>
          <div class="headline pt-1"> {{ title_l }} <span style="font-weight:bold"> {{ title_r }} </span>
          </div>
          <div class="subheading text-xs-center grey--text pt-1 pb-3"> {{ description }}</div>
        </div>
      </v-flex>
    </v-layout>

    <v-layout align-center column justify-space-around mt-3>
      <div :key="v.name" v-for="v in nav">
        <router-link :to="v.href" v-if="v.router">
          <v-btn class="blue--text--4"
                 flat> {{ v.name }}
          </v-btn>
        </router-link>

        <v-btn :href="v.href" :target="v.blank ? '_blank' : ''"
               class="blue--text--4"
               flat
               v-else> {{ v.name }}
        </v-btn>
      </div>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    name: 'LeftBox',
    data() {
      return {
        title_l: "a",
        title_r: "Pythonista",
        avatar: "https://www.gravatar.com/avatar/ba7eacd36a440d894441cf83d6245b38?s=200",
        description: ">>> import this",
        nav: [
          {name: "Home", href: "/", router: true},
          // {name: "Blog", href: "/blog", router: true},
          {name: "Github", href: "https://github.com/swoiow", blank: true},
          // {name: "APIS", href: "/apis"},
        ]
      }
    },
    mounted: function () {
      let vm = this

      vm.$http.get(vm.$gc.H + '/api/query/blog_nav')
        .then(function (response) {
          vm.$data.nav = response.data
        })
    }
    }
</script>

<style scoped>
  a {
    text-decoration: none;
  }
</style>
