export default [
  {
    path: '/',
    name: 'home',
    view: 'RightBox',
  },
  {
    path: '/blog',
    name: "blog",
    view: 'BlogBox',
  },
  {
    path: '/post/:post_id',
    name: 'post',
    view: 'PostBox',
  },
]
