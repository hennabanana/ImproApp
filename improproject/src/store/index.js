import Vue from 'vue'
import Vuex from 'vuex'
import tasks from './modules/tasks'
import login from './modules/login'
import game from './modules/game'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tasks,
    login,
    game
  },
})