<template>
  <v-content>
    <v-container grid-list-md text-xs-center>
      <v-layout justify-space-between row wrap>
        <v-flex xs10>
          <v-text-field
                  label="标题"
                  v-model="title"
          ></v-text-field>

        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs2>
          <v-switch
                  label="宽屏"
                  v-model="full_style"
          ></v-switch>
        </v-flex>

        <v-flex v-show="!full_style" xs12>
          <v-text-field
                  label="地址栏别称"
                  v-model="alias"
          ></v-text-field>
        </v-flex>


        <v-flex v-show="!full_style" xs3>
          <v-select
                  :items="type_items"
                  item-text="v"
                  item-value="k"
                  label="类型"
                  v-model="type"
          ></v-select>

          <v-select
                  :items="fmt_items"
                  label="格式"
                  v-model="fmt"
          ></v-select>

          <v-select
                  :items="st_items"
                  label="状态"
                  v-model="status"
          ></v-select>

          <v-select
                  :items="tag_items"
                  chips
                  item-text="v"
                  item-value="k"
                  label="标签"
                  multiple
                  v-model="tags"
                  v-show="type==`post`"
          ></v-select>

          <v-textarea
                  label="简述"
                  name="description"
                  rows="10"
                  v-model="description"
                  v-show="type==`post`"
          ></v-textarea>

          <v-textarea
                  label="元数据"
                  name="meta"
                  v-model="meta"
          ></v-textarea>
        </v-flex>

        <v-flex>
          <!--<froala :config="config" :tag="'textarea'" v-model="txt"></froala>-->
          <!--<froalaView v-model="txt"></froalaView>-->
          <v-textarea
                  color="teal lighten-3"
                  label="正文"
                  name="txt"
                  rows="33"
                  v-model="txt"
          ></v-textarea>
        </v-flex>
      </v-layout>

      <div class="text-xs-center">
        <v-btn @click="save" color="teal" dark round small> 提交</v-btn>
      </div>
    </v-container>
  </v-content>

</template>

<script>
  var qs = require('qs');

  export default {
    name: "Editor",
    data: () => ({
      fmt: "Markdown",
      fmt_items: ["Html", "Markdown"],
      type: "post",
      type_items: [
        {k: "post", v: "文章"},
        {k: "page", v: "页面"}
      ],
      st_items: [],
      tag_items: [],
      full_style: false,
      config: {
        events: {
          'froalaEditor.initialized': function () {
            console.log('initialized')
          }
        }
      },

      title: null,
      alias: null,
      status: null,
      tags: null,
      description: null,
      meta: null,
      txt: null,
    }),
    mounted: function () {
      let vm = this;

      vm.$http.get(vm.$gc.H + "/tags")
        .then(function (response) {
          vm.$data.tag_items = response.data
        })
        .then(() => {
          // toastr["success"]("标签加载完成")
        });

    },

    methods: {
      save() {
        let vm = this;
        vm.save_post()
      },
      save_post() {
        let vm = this;

        let data = vm.generate_data();
        vm.$http.post(vm.$gc.H + "/api/posts", qs.stringify(data))
          .then(function (response) {
            return response;
          })
      },
      save_page() {
        let vm = this;

        let data = vm.generate_data();
        delete data["tags"];
        delete data["description"];

        console.log(qs.stringify(data));
        // axios.post("/api/pages", Qs.stringify(data))
        //     .then(function (response) {
        //           return response;
        //       })
      },
      generate_data() {
        let vm = this;

        return {
          title: vm.$data.title,
          alias: vm.$data.alias,
          status: vm.$data.status,
          tags: vm.$data.tags && vm.$data.tags.join(","),
          description: vm.$data.description,
          meta: vm.$data.meta,
          content: vm.$data.txt,
        }
      }
    }
  }
</script>

<style scoped>

</style>
