export default [
  {
    path: '/',
    name: 'home',
    view: 'RightBox'
  },
  {
    path: '/(blog|posts)',
    name: 'blog',
    view: 'BlogBox'
  },
  {
    path: '/(post|page)/:post_id',
    name: 'post',
    view: 'PostBox'
  }
]
