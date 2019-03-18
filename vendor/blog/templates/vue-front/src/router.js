import Vue from 'vue'
import Router from 'vue-router'

import BlogBox from '@/components/BlogBox.vue'
import RightBox from '@/components/RightBox'
import PostBox from '@/components/PostBox.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      meta: {
        keepAlive: true, //此组件需要被缓存
      },
      component: RightBox,
      // component: () => import(/* webpackChunkName: "home" */ './components/LeftBox.vue')
    },
    {
      path: '/blog',
      name: 'blog',
      meta: {
        keepAlive: false, //此组件需要被缓存
      },
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: BlogBox
      // component: () => import(/* webpackChunkName: "posts" */ './views/Blog.vue')
    },
    {
      path: '/post/:post_id',
      name: 'post',
      meta: {
        keepAlive: false, //此组件需要被缓存
      },
      component: PostBox,
      // component: () => import(/* webpackChunkName: "posts" */ '@/components/PostBox.vue')
    }
  ]
})
