<template>
    <div id="app">
        <router-link :to="{ name: 'home' }">
            <h1>ImproApp</h1>
        </router-link>
        <router-view/>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: "App",
    data() {
        return {
          loggedin : localStorage.getItem('user-token')
        };
    },
    computed: {
        ...mapState({
            isToken: state => state.login.isToken
        })
    },

};
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
