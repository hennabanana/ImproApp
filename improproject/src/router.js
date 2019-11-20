import Vue from 'vue'
import Router from 'vue-router'
import Spectator from '@/components/Spectator'
import Actor from '@/components/Actor'
import Login from '@/components/Login'
import Director from '@/components/Director'
import Home from '@/components/Home'
import Speech from '@/components/Speech'


Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [{
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/director/login',
      name: 'directorLogin',
      component: Login,
    },
    {
      path: '/actor/login',
      name: 'actorLogin',
      component: Login,
    },
    {
      path: '/actor',
      name: 'actor',
      component: Actor,
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/director',
      name: 'director',
      component: Director,
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/spectator',
      name: 'spectator',
      component: Spectator,
    },
    {
      path: '/test',
      name: 'speech',
      component: Speech,
    },

  ],
})

router.beforeEach((to, from, next) => {
  //es wird geprueft ob die To-Route ein Meta requires Auth
  //gesetzt hat.
  if (to.matched.some(record => record.meta.requiresAuth)) {
    //falls im lokalen Speicher der Token gesetzt ist
    //ist der User eingeloggt und die geplante Route
    //wird fortgesetzt
    if (localStorage.getItem('user-token')) {
      next()
      return
    }
    //falls kein Token gesetzt ist und der User als naechsten
    //die actor-Route aufrufen will, wird er erst aufgefordert
    //sich einzuloggen
    if (to.name == "actor") {
      next('/actor/login')
    }
    //das selbe gilt für den Director
    if (to.name == "director") {
      next('/director/login')
    }
    //wenn kein Meta-Eintrag vorhanden ist, wird die Route wie
    //geplant aufgelöst
  } else {
    next()
  }
})
export default router;