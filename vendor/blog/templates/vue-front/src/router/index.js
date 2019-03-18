import Vue from 'vue'
import Router from 'vue-router'
import paths from './paths'

// import BlogBox from '@/components/BlogBox.vue'
// import RightBox from '@/components/RightBox'
// import PostBox from '@/components/PostBox.vue'

function route (path, view, name) {
  return {
    name: name || view,
    path,
    component: (resovle) => import(
      `@/components/${view}.vue`
      ).then(resovle)
  }
}

Vue.use(Router);
const router = new Router({
  mode: 'history',
  routes: paths.map(path => route(path.path, path.view, path.name)).concat([
    { path: '*', redirect: '/' }
  ]),
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { selector: to.hash }
    }
    return { x: 0, y: 0 }
  }
})

export default router

// export default new Router({
//   // mode: 'history',
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       meta: {
//         keepAlive: false, //此组件需要被缓存
//       },
//       // component: RightBox,
//       component: () => import(/* webpackChunkName: "home" */ './components/LeftBox.vue')
//     },
//     {
//       path: '/blog',
//       name: 'blog',
//       meta: {
//         keepAlive: false, //此组件需要被缓存
//       },
//       // route level code-splitting
//       // this generates a separate chunk (about.[hash].js) for this route
//       // which is lazy-loaded when the route is visited.
//       component: BlogBox
//       // component: () => import(/* webpackChunkName: "posts" */ './views/Blog.vue')
//     },
//     {
//       path: '/post/:post_id',
//       name: 'post',
//       meta: {
//         keepAlive: false, //此组件需要被缓存
//       },
//       component: PostBox,
//       // component: () => import(/* webpackChunkName: "posts" */ '@/components/PostBox.vue')
//     }
//   ]
// })
