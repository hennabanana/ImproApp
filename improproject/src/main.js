import Vue from 'vue'
import App from '@/App.vue'
import axios from 'axios'


import store from '@/store'
import router from '@/router'
import Login from '@/components/Login'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);

Vue.config.productionTip = false

//Vue.use(VueRouter)
const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token}`
}
const vue = new Vue({
  router,
  store,
  render: h => h(App),
  components: {
    'Login': Login,
  }
})

vue.$mount('#app')