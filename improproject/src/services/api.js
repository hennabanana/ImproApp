import axios from 'axios'
import Cookies from 'js-cookie'

//http anfrage wird erstellt
export default axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken')
  }
})