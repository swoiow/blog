<template>
  <v-container fluid>
    <v-layout
      align-center
      fill-height
      justify-center
      mt-5
      row
    >
      <v-flex>
        <div class="text-xs-center">
          <a href="/dashboard">
            <v-avatar size="125px">
              <img
                class="img-circle elevation-7 mb-1"
                :src="avatar"
              >
            </v-avatar>
          </a>
          <div class="headline pt-1">
            {{ title_l }} <span style="font-weight:bold">
              {{ title_r }}
            </span>
          </div>
          <div class="subheading text-xs-center grey--text pt-1 pb-3">
            {{ description }}
          </div>
        </div>
      </v-flex>
    </v-layout>

    <v-layout
      align-center
      column
      justify-space-around
      mt-3
    >
      <div
        v-for="v in nav"
        :key="v.name"
      >
        <router-link
          v-if="v.router"
          :to="v.href"
        >
          <v-btn
            class="blue--text--4"
            flat
          >
            {{ v.name }}
          </v-btn>
        </router-link>

        <v-btn
          v-else
          :href="v.href"
          :target="v.blank ? '_blank' : ''"
          class="blue--text--4"
          flat
        >
          {{ v.name }}
        </v-btn>
      </div>
    </v-layout>

    <v-layout>
      <v-toolbar
        card
        color="rgba(255, 0, 0, 0)"
        flat
        light
        prominent
      >
        <v-btn icon>
          <v-icon @click="search">
            search
          </v-icon>
        </v-btn>
        <v-text-field
          hide-details
          single-line
          placeholder="Full Text Search ..."
          @keyup.enter="search"
        />
      </v-toolbar>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'LeftBox',
  data () {
    return {
      title_l: 'a',
      title_r: 'Pythonista',
      avatar: 'https://www.gravatar.com/avatar/ba7eacd36a440d894441cf83d6245b38?s=200',
      description: '>>> import this',
      nav: [
        { name: 'Home', href: '/', router: true }
      ]
    }
  },
  mounted: function () {
    let vm = this

    vm.$http.get(vm.$gc.H + '/api/query/blog_nav')
      .then(function (response) {
        vm.$data.nav = response.data
      })
  },

  methods: {
    search: function () {
      let vm = this
      let kw = vm.$el.querySelector('input').value

      let query = vm.$route.query

      let newQy = JSON.parse(JSON.stringify(query))
      newQy.q = kw

      vm.$router.push({ path: '/blog', query: newQy })
    }
  }
}
</script>

<style scoped>
  a {
    text-decoration: none;
  }
</style>
