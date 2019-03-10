<template>
  <v-container
    class="typo"
    fill-height
    fluid
  >
    <v-layout
      align-center
      fill-height
      justify-center
      row
    >
      <pre class="mb-5">
      <code
              class="blockquote"
              style="padding-right: 2rem"
      >
dict(
    高度熟练=["Python"],

    WEB栈=[
        "Flask", "Tornado", "Django", "Celery",
        "Vue", "Bootstrap", "Element", "JavaScript"
    ],

    数据栈=[
        "Scrapy", "Requests", "Beautiful Soup",
        "Puppeteer", "Splash",
    ],

    其他栈=[
        "Docker", "Openshift",
        "Sqlalchemy", "Mysql", "Pgsql", "Oracle",
        "Kafka", "Elasticsearch", "Redis", "gRPC",
        "FastDFS", "Ceph",
    ],

    在学=["Golang",],
)
      </code>
    </pre>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'RightBox',
  data () {
    return {}
  }
}
</script>

<style scoped>
  pre {
    background: unset;
    border: unset;
  }
</style>
