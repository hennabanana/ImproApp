<template>
 <div class="Login">
         <b-container>
            <b-row align-h="center">
  <b-form>
    <label for="username">Benutzername</label>
    <b-input
      v-model="username"
      class="mb-2 mr-sm-2 mb-sm-0"
      placeholder="Benutzername"
    ></b-input>

    <label for="text-password">Password</label>
    <b-input v-model="password" type="password" id="text-password"></b-input>
    <br>
    <b-form-checkbox id="checkbox-1" v-model="register">Register</b-form-checkbox>
<br>
    <b-button variant="primary" @click="login">Login</b-button>
    <b-button variant="secondary" @click="logout">Logout</b-button>
  </b-form>
  </b-row>
</b-container>
 </div>
 
</template>

<script>
import { mapState} from 'vuex'

export default {
  name: "Login",
  data(){
    return {
      username : "",
      password : "",
      register_actor: false,
      register_director: false,
      register: false
    };
  },
  computed: {
  ...mapState({
     is_director: state => state.login.is_director,
     isToken: state => state.login.isToken
  })
  },
methods: {
 login () {
   const { username, password, register} = this
   //user will sich registrieren?
   if(!register)
   {
    //Login Action wird aufgreufen
    this.$store.dispatch('login/AUTH_REQUEST', { username, password }).then(() => {
      if(this.$route.path.includes('director')){
        //wen director im Pfad steht ist die nächste seite die director seite
        this.$router.push({ name: 'director' })
      }
      else{
        //andernfalls die actor seite
        this.$router.push({ name: 'actor' })
      }
    })
   }
   else
   {
    //bei registrierung wird erst die Register action aufgerufen
    //und im anschluss die Login methode
    var register_director = this.$route.path.includes('director')
    this.$store.dispatch('login/AUTH_REGISTER', { username, password, register_director, }).then(() => {
      this.$store.dispatch('login/AUTH_REQUEST', { username, password }).then(() => {
      if(this.$route.path.includes('director')){
        this.$router.push({ name: 'director' })
      }
      else{
        this.$router.push({ name: 'actor' })
      }
      })})
   }
 },
   logout () {
    this.$store.dispatch('login/AUTH_LOGOUT')
    .then(() => {
      this.$router.push('/')
    })
  }
},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
button {
    margin: 10px;
}

</style>
