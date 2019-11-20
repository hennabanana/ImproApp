import api from '@/services/api'
//wird aktuell nicht mehr verwendet, Logik befindet sich im game module
const state = {
  tasks: [],
  actors: [],
  synth: window.speechSynthesis,
  speech: new window.SpeechSynthesisUtterance()

}

const getters = {
  tasks: state => {
    return state.tasks
  },
  actors: state => {
    return state.actors
  },
  getActorNameById: state => id => {
    return (state.actors.find(actor => actor.a_id === id) || {}).name || null
  },
  getTaskById: state => id => {
    return (state.tasks.find(task => task.t_id === id)) || null
  },
  synth: state => {
    return state.synth
  },
  speech: state => {
    return state.greetingSpeech
  },
}

const actions = {
  getActors({
    commit
  }) {
    api.get(`actors/`)
      .then(response => {
        commit('setActors', response.data)
      })
  },
  getTasks({
    commit
  }) {
    api.get(`tasks/`)
      .then(response => {
        commit('setTasks', response.data)
      })
  },
  addTask({
    commit
  }, task) {
    api.post(`tasks/`, task)
      .then(response => {
        commit('addTask', response.data)
      })
  },


  deleteTask({
    commit
  }, taskId) {
    api.delete(`tasks/${taskId}`)
    commit('deleteTask', taskId)
  },
  readOut({
    commit
  }, task) {
    state.speech.text = task.text
    //german languages
    let voiceList = state.synth.getVoices()
    state.speech.voice = voiceList[0]
    //set german languages to Synth
    state.synth.speak(state.speech)
    //PUT TO SERVE
    task.status = 2
    api.put(`tasks/${task.t_id}/`, task)
      .then(response => {
        commit('readOut', response.data)
      })
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
  deleteTask(state, taskId) {
    state.tasks = state.tasks.filter(obj => obj.t_id !== taskId)
  },
  readOut(state, task) {
    const item = state.tasks.find(t => t.t_id === task.t_id)
    Object.assign(item, task)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}