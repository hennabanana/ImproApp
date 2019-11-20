import api from '@/services/api'
import ReconnectingWebsocket from 'reconnecting-websocket'

import axios from 'axios'


const state = {
  tasks: [],
  actors: [],
  users: [],
  game: '',
  status: '',
  director: '',
  actor: '',
  spectator: '',
  currentUser: '',
  tasksock: null,
  actorsock: null,
  ausgabe: ''
}
//Definition der Getters
const getters = {
  users: state => {
    return state.users
  },
  tasks: state => {
    return state.tasks
  },
  actors: state => {
    return state.actors
  },
  //Getter um anhand der id den User zu bekommen
  getActorNameById: state => id => {
    return (state.users.find(user => user.id === id) || {}).username || null
  },
  //Getter um eine Task anhand der id zu bekommen
  getTaskById: state => id => {
    return (state.tasks.find(task => task.id === id)) || null
  },
  synth: state => {
    return state.synth
  },
  speech: state => {
    return state.greetingSpeech
  },
  game: state => {
    return state.game
  },
  director: state => {
    return state.director
  },
  actor: state => {
    return state.actor
  },
  spectator: state => {
    return state.spectator
  },
  currentUser: state => {
    return state.currentUser
  },
  ausgabe: state => {
    return state.ausgabe
  }
}

const actions = {
  //Alle Actors eines Spieles werden geholt
  getActors({
    commit,
    dispatch
  }) {
    api.get(`actors/game/${state.game.id}`)
      .then(response => {
        commit('setActors', response.data)
        //Wenn die Actor da sind, werden die Tasks geholt
        dispatch('getTasks')
      })
  },
  //Alle Tasks werden geholt
  getTasks({
    commit,
    dispatch
  }) {
    api.get(`tasks/game/${state.game.id}`)
      .then(response => {
        commit('setTasks', response.data)
        // wenn der director oder spectator gesetzt ist und der socket noch nicht
        //initialisiert wurde, wird die websocket action aufgerufen
        if (state.director || state.spectator && state.tasksock == null) {
          dispatch('websocket')
        }
      })
  },
  //die Action wird meistens beim neuladen der Seite aufgerufen
  getUserByToken({
    commit,
    dispatch
  }) {
    //der token wird aus dem lokalen speicher geholt
    var token = localStorage.getItem('user-token')
    //es wird geprüft ob der token leer ist
    if (token != null) {
      //eine Post-anfrage mit dem Token wird gestellt
      api.post('/getUserByToken', {
          token: token
        })
        //es wird auf die Antwort gewartet
        .then(response => {
          //commit ruft die Mutation setUser auf
          //und setzt den Benutzer aus den Daten der Antwort
          commit('setUser', response.data)
          //wenn der director oder der spectator gefüllt sind
          if (state.director || state.spectator) {
            //und das game gefüllt ist
            if (state.game != '') {
              //wird die Action get Actors aufgerufen
              dispatch('getActors')
            }
          }
          //falls der actor gesetzt wurde
          //wird für den Actor die Action
          //websocketActor aufgerufen
          if (state.actor) {
            dispatch('websocketActor')
          }
        })
    }
  },
  //das gameobjekt wird anhand des gamename geholt
  getGameByName({
    commit,
  }, game) {
    api.get(`games/${game.name}`)
      .then(response => {
        commit('setGame', response.data)
      })
  },
  //dem Actor wird das Spiel gesetzt
  joinGameAsActor({
    commit,
    dispatch
  }, actor) {
    api.put(`actors/${state.actor.id}/`, actor)
      .then(response => {
        commit('setActor', response.data)
        // websocket action wird aufgerufen und 
        //websocket des Actors wird initial

        dispatch('websocketActor')
      })
  },
  //spectator joint dem spiel 
  joinGameAsSpectator({
    commit,
    dispatch
  }, gameid) {
    api.post(`createSpectator`, gameid)
      .then(resp => {
        const token = resp.data.token
        localStorage.setItem('user-token', token) // store the token in localstorage
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        commit('setSpectator', resp.data)
        dispatch('getUserByToken')
      })
  },
  //Afugabe wird hinzugefügt
  addTask({
    commit
  }, task) {
    api.post(`tasks/`, task)
      .then(response => {
        commit('addTask', response.data)
        //websocket wir benachrichtigt dass eine Nachricht 
        //hinzugefügt wurde
        var message = {
          'type': 'create.task',
        }
        state.tasksock.send(JSON.stringify(message));
      })
  },
  //Spiel wir erstellt
  createGame({
    commit
  }, game) {
    api.post(`games/`, game)
      .then(response => {
        commit('addGame', response.data)
      })
  },
  //aufgabe wurde gelöscht
  deleteTask({
    commit
  }, taskId) {
    api.delete(`tasks/${taskId}`)
    commit('deleteTask', taskId)
    //websocket wird benachrichtigt dass aufgabe gelöscht werden soll
    var message = {
      'type': 'update.task',
    }
    state.tasksock.send(JSON.stringify(message));
  },
  //nachricht soll vorgelesen werden
  readOut({
    commit //Ohne das Commit gehts nicht
  }, task) {
    var message = {
      'type': 'readout.task',
      'task': task
    }
    //Socket wird benachritchit dass Actor nachricht vorgelesen
    //werden soll
    state.tasksock.send(JSON.stringify(message));
    task.status = 3
    api.put(`tasks/${task.id}/`, task)
      .then(response => {
        commit('readOut', response.data)
      })
  },
  //websocket wird initialisiert
  websocket({
    dispatch
  }) {
    //state.tasksock = new ReconnectingWebsocket('ws://192.168.178.22:8000/ws/');
    //state.tasksock = new ReconnectingWebsocket('ws://192.168.178.22:8000/ws/');
    state.tasksock = new ReconnectingWebsocket('ws://192.168.178.22:8000/ws/');
    //state.tasksock.onmessage = function (task) {
    state.tasksock.onmessage = function (typejson) {
      //Json wird geparsed
      var type_data = JSON.parse(typejson.data);
      //Typ der nachricht wird geprüft
      if (type_data.update == 'task') {
        //die Methode getTasks() wird ausgeführt und die neuen
        //tasks werden geholt
        dispatch('getTasks')
      }
      if (type_data.update == 'actor') {
        //die Methode getActors() wird ausgeführt und die neuen
        //Actors werden geholt
        dispatch('getActors')
      }
    };
  },
  websocketActor({
    commit,
  }) {
    //state.actorsock = new ReconnectingWebsocket('ws://192.168.178.22:8000/ws/' + state.actor.user.id);
    //state.actorsock = new ReconnectingWebsocket('ws://192.168.178.22:8000/ws/' + state.actor.user.id);
    state.actorsock = new ReconnectingWebsocket('ws://192.168.178.22:8000/ws/' + state.actor.user.id);

    //onmessage wird aufgerufen wenn der Actor über den Websocket
    //eine nachricht bekommt
    state.actorsock.onmessage = function (taskjson) {
      //Json wird geparsed
      var task_data = JSON.parse(taskjson.data);
      //task wird rausgeholt
      var task = task_data.task
      //speechSynthesis eigenschaft vom Window object geholt
      var speechSynthesis = window.speechSynthesis
      //SpeechSynthesisUtterance wird erstellt
      var SpeechSynthesisUtterance = new window.SpeechSynthesisUtterance()
      //der Task.text wird dem SpeechSynthesisUtterance hinzugefügt
      SpeechSynthesisUtterance.text = task.text
      //eine Deutsche verständliche stimme wird ausgewähl
      let voice = speechSynthesis.getVoices().filter(function (voice) {
        return voice.name == "anna";
      })[0];
      //Die stimme wir dem SpeechSynthesisUtterance gesetz
      SpeechSynthesisUtterance.voice = voice
      //der text wird am Client vorgelesen
      speechSynthesis.speak(SpeechSynthesisUtterance)
    };
  }
}

const mutations = {
  setActors(state, actors) {
    state.actors = actors
  },
  setTasks(state, tasks) {
    state.tasks = tasks
  },
  addTask(state, task) {
    state.tasks.push(task)
  },
  addGame(state, game) {
    state.game = game
  },
  setActor(state, data) {
    state.actor = data
  },
  setSpectator(state, data) {
    state.spectator = data.spectator

  },
  deleteTask(state, taskId) {
    state.tasks = state.tasks.filter(obj => obj.id !== taskId)
  },
  readOut(state, task) {

    const item = state.tasks.find(t => t.id === task.id)
    Object.assign(item, task)
  },
  //die Mutations bekommen immer den state übergeben
  //und in data befindet sich die Daten von der Antwort 
  //vom Server
  setUser: (state, data) => {
    //es wird geprueft um welche Rolle es sich handlet
    if (data.group == 'directors') {
      //die Daten werden dementsprechend im State gesetzt
      state.director = data.director
      state.currentUser = data.director.user
      if (data.game) {
        state.game = data.game
      }
    } else if (data.group == 'actors') {
      state.actor = data.actor
      state.currentUser = data.actor.user
      if (data.actor.game) {
        state.game = data.actor.game
      }
    } else if (data.group == 'spectators') {
      state.spectator = data.spectator
      state.currentUser = data.spectator.user
      if (data.spectator.game) {
        state.game = data.spectator.game
      }
    }
  },
  setGame: (state, data) => {
    if (data) {
      state.game = data
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