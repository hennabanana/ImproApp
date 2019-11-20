import axios from 'axios'
import game from './game';

const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
  is_director: false,

}

const getters = {
  authStatus: state => state.status,
  isToken: state => {
    if (state.token) {
      return true
    } else {
      return false
    }
  },
}

const actions = {
  AUTH_REQUEST: ({
    commit,
    // dispatch
  }, user) => {
    return new Promise((resolve, reject) => { // Promis wird für die Router redirection genutzt
      commit('AUTH_REQUEST') //Mutation wird aufgerufen
      //Get anfrage an api/login in nutzdaten user
      axios({
          url: 'api/login',
          data: user,
          method: 'POST'
        })
        .then(resp => {
          //token wird aus der antwort genommen
          const token = resp.data.token
          // token wird im lokalen abgespeichert
          localStorage.setItem('user-token', token)
          // token wird in header gesetzt
          axios.defaults.headers.common['Authorization'] = `Token ${token}`
          // mutation success wird aufgreufen
          commit('AUTH_SUCCESS', resp)
          resolve(resp)
        })
        .catch(err => {
          commit('AUTH_ERROR', err)
          //falls die anfrage fehlschlägt wird der localestorrage geleert
          localStorage.removeItem('user-token')
          reject(err)
        })
    })
  },
  AUTH_REGISTER: ({
    commit,
  }, user, password, register_director) => {
    return new Promise((resolve, reject) => {
      commit('AUTH_REQUEST')
      //Postanfrage mit user,password und ob director oder actor
      axios({
          url: 'api/register',
          data: user,
          password,
          register_director,
          method: 'POST'
        })
        .then(resp => {
          resolve(resp)
        })
        .catch(err => {
          commit('AUTH_ERROR', err)
          localStorage.removeItem('user-token')
          reject(err)
        })
    })
  },
  AUTH_LOGOUT: ({
    commit,
  }) => {
    return new Promise((resolve) => {
      commit('AUTH_LOGOUT')
      //lokaler speicher wird geleert
      localStorage.removeItem('user-token')
      // Header-Eintrag wird gelöscht
      delete axios.defaults.headers.common['Authorization']
      resolve()
    })
  },
}

const mutations = {
  //nach den Actions werden hier die Store eigenschaften gelöscht
  AUTH_REQUEST: (state) => {
    state.status = 'loading'
  },
  AUTH_SUCCESS: (state, resp) => {
    state.status = 'success'
    state.token = resp.data.token
    state.is_director = resp.data.is_director
    if (state.is_director) {
      game.state.director = resp.data.director
    } else {
      game.state.actor = resp.data.actor
    }

  },
  AUTH_ERROR: (state) => {
    state.status = 'error'
  },
  AUTH_LOGOUT: (state) => {
    state.status = ''
    state.token = ''
    game.state.director = ''
    game.state.actor = ''
    game.state.spectator = ''
    state.is_director = false
    game.state.game = ''
    state.isToken = false
    //beim Logout wird an den Websocket ein disconnect gesendet
    var message = {
      'type': 'logout',
    }
    if (game.state.tasksock != null) {
      game.state.tasksock.send(JSON.stringify(message));
      game.state.tasksock = null
    }
    if (game.state.actorsock != null) {
      game.state.actorsock.send(JSON.stringify(message));
      game.state.actorsock = null
    }
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}