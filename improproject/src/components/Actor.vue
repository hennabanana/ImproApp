<template>
    <div class="actor">
        <b-container>
            <b-row align-h="center">
                <b-col md="4">
                    <b-form v-if="!actor.game">
                        <b-form-group label="Geben Sie den Spielnamen, den Sie vom Spielleiter erhalten haben ein:">
    
                            <b-form-input type="text" placeholder="Spielname" v-model="gamename" />
                        </b-form-group>
                        <b-button class="m-2" @click="getGameByName({name:gamename})" :disabled="!gamename">Spiel suchen</b-button>
                        <b-button class="m-2" @click="joinGameAsActor({user:actor.user, game:game})" :disabled="!game">Spiel beitreten</b-button>
                    </b-form>
                    <br>
                    <div v-if="actor.game">
                        <h4>{{actor.user.username}}, du bist im Spiel: {{actor.game.name}}</h4>
                        <h5>Ziehe deine Kopfhörer an!</h5>
                        <h1>{{ausgabe}}</h1>
                    </div>
                </b-col>
    
            </b-row>
        </b-container>
                <b-button v-if="!actor.game || currentUser || actor || actor != ''" id="logout-button" size="sm" @click="logout">Logout</b-button>
    </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
    name: "Actor",
    data() {
        return {
            gamename: "",
        };
    },
    computed: {
        ...mapState({
            tasks: state => state.game.tasks,
            actors: state => state.game.actors,
            director: state => state.game.director,
            game: state => state.game.game,
            users: state => state.game.users,
            speech: state => state.game.speech,
            actor: state => state.game.actor,
            currentUser: state => state.game.currentUser,
            ausgabe: state => state.game.ausgabe
        }),
        ...mapGetters('game', [
            'getActorNameById'
        ])
    },
    methods: {...mapActions('game', [
        'joinGameAsActor', 'getGameByName',
    ]),
    //logout von der Login Componente wird aufgerufen
    logout() {
            this.$store.dispatch('login/AUTH_LOGOUT')
                .then(() => {
                    this.$router.push('/')
                })
        }
    },

    created() {
        this.$store.dispatch('game/getUserByToken')
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
button {
    margin: 10px;
}
#logout-button {
    position: absolute;
    top: 0;
    right: 0;
}
</style>
