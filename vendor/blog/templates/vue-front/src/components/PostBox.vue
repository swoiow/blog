<!--Post & Page-->

<template>
  <v-container fluid>
    <v-layout class="px-5" column fill-height>
      <v-flex align-self-end>
        <toolbar></toolbar>
      </v-flex>
    </v-layout>

    <v-layout class="typo typo-selection" id="wrapper">
      <v-flex>
        <h1 class="mb-1">
          {{ post.title }}
        </h1>
        <div id="tagline">
          {{ post.tag }}
        </div>
        <div v-html="post.content">
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  /*eslint no-console: ["error", { allow: ["log", "warn", "error"] }] */
  import toolbar from '@/components/toolbar'

  export default {
    name: "PostBox",
    components: {
      toolbar,
    },
    data() {
      return {
        is_md: null,
        post: {
          title: "I'm a Title",
          tag: ["tag1", "tag2"],
          content: "This is content",
        },
      }
    },
    mounted: function () {
      let vm = this

      vm.$store.commit('setNav', false)
      vm.fetchData()
    },

    methods: {
      fetchData: function () {
        let vm = this

        vm.$http.get(vm.$gc.H + "/api/post/" + vm.$route.params.post_id)
          .then(function (response) {
            vm.$data.post = response.data
            vm.$data.is_md = response.data.type === "Markdown" && true || false
          })
          .catch(function (err) {
            let fake = {
              title: err.message,
              content: err.stack,
            }

            vm.$data.post = fake
          })
          .then(function () {
            if (vm.$data.is_md) {
              console.log("render as markdown")
              !("marked" in window) && vm.loadMarkDownJS() || vm.renderMarkDown()
            } else {
              console.log("render as normal html")
            }
          })

        return true
      },

      loadMarkDownJS: function () {
        let vm = this

        return new Promise(function (resolve) {
          const s = document.createElement("script")
          s.type = "text/javascript"
          s.src = "https://unpkg.com/marked@0.5.2/marked.min.js"
          s.onload = function () {
            vm.renderMarkDown() // ugly
          }
          // s.integrity = "sha384-I2nqUi8qf3ekoF24PvLsQdMXV0PATvtN8jkyiXNMTvUbnxbX715AZN241NnitpIi";
          // s.crossorigin = "anonymous";
          document.getElementById("_js").appendChild(s)

          return resolve()
        })
      },

      renderMarkDown: function () {
        let vm = this
        vm.$data.post.content = marked(vm.$data.post.content)
      },
    },
  }
</script>

<style scoped>
  code {
    color: #1abc9c;
  }

  pre {
    white-space: pre-wrap;
  }

  i.serif {
    text-transform: lowercase;
    color: #1abc9c;
  }

  :-moz-any(h1, h2, h3, h4, h5, h5) i.serif {
    text-transform: capitalize;
  }

  i.serif:hover {
    color: inherit;
  }

  #wrapper {
    padding: 5% 10%;
    position: relative;
    background-color: white;
  }

  #tagline {
    color: #999;
    font-size: 1em;
    margin: -2em 0 2em;
    padding-bottom: 2em;
    border-bottom: 3px double #eee;
  }

  #table {
    margin-bottom: 2em;
    color: #888;
  }

  @media only screen and (max-width: 640px) {
    table {
      word-break: break-all;
      word-wrap: break-word;
      font-size: 12px;
    }

    .typo table th, .typo table td, .typo-table th, .typo-table td .typo table caption {
      padding: 0.5em;
    }
  }
</style>

<style>
  #wrapper code::before, code::after {
    content: unset;
  }

  #wrapper code {
    background-color: unset;
    box-shadow: unset;
    -webkit-box-shadow: unset;
  }
</style>
