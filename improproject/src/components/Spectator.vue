<template>
    <div class="spectator">
        <b-container v-if="!spectator.game">
            <b-row align-h="center">
                <b-col md="4">
                    <b-form>
                        <b-form-group label="Geben Sie den Spielnamen, den Sie vom Spielleiter erhalten haben ein:">
    
                            <b-form-input type="text" placeholder="Spielname" v-model="gamename" />
                        </b-form-group>
                        <b-button @click="getGameByName({name:gamename})" :disabled="!gamename">Spiel suchen</b-button>
                        <b-button @click="joinGameAsSpectator({game:game.id})" :disabled="!game">Spiel beitreten</b-button>
                    </b-form>
                </b-col>
            </b-row>
        </b-container>
    
        <b-container v-if="spectator.game">
            <b-row align-h="center">
                <b-col md="6">
                                    <h4>Zuschauer</h4>

                    <b-tabs content-class="mt-3">
                        <b-tab title="Aufgabe erfassen" active>
                            <b-form>
                                                        <b-row class="m-3" align-h="center">
                            <b>Schauspieler:</b>
                            </b-row>
                                <b-row class="m-3" align-h="center">
                                    <b-form-checkbox-group v-for="actor in actors" :key="actor.id" id="checkbox-group-1" v-model="selectedActors" :value="actor">
                                        <b-form-checkbox :value="actor" v-model="selectedActors">{{actor.user.username}}</b-form-checkbox>
                                    </b-form-checkbox-group>
    
                                </b-row>
    
                                <b-row align-h="center">
                                    <b-col xs="8">
                                        <b-form-textarea id="textarea-auto-height" placeholder="Aufgabe" rows="3" max-rows="8" v-model="text"></b-form-textarea>
                                        <b-button @click="addTask({ text: text, actors:selectedActors, writer:currentUser, status:1, game:game })" :disabled="!text">Hinzufügen</b-button>
                                    </b-col>
                                </b-row>
    
                            </b-form>
                        </b-tab>
                        <b-tab title="Überblick Aufgaben">
                            <p v-if="tasks.length === 0">Aktuell keine Aufgaben</p>
                            <div class="task" v-for="task in tasks" :key="task.t_id">
                                <b-card>
                                    <b-card-title>Schauspieler:<br>
                                        <span v-if="task.actors" v-for="(a, index) in task.actors" :key="a.id">
                                            {{a.user.username}}<span v-if="index != Object.keys(task.actors).length - 1">, </span>
                                        </span>
                                    </b-card-title>
                                    <b-card-text>
                                        Aufgabe: {{task.text}}
                                    </b-card-text>
                                    <b-card-text v-if="task.status == 1" style="background-color:#808040; color:#D8FD02;">
                                        Zustand: Offen
                                    </b-card-text>
                                    <b-card-text v-if="task.status == 2" style="background-color:#FFA500; color:#D8FD02;">
                                        Zustand: Wird grade abgespielt
                                    </b-card-text>
                                       <b-card-text v-if="task.status == 3" style="background-color:#4C4C4C; color:#D8FD02;">
                                        Zustand: Abgespielt
                                    </b-card-text>
                                </b-card>
                            </div>
                        </b-tab>

                    </b-tabs>
                </b-col>
            </b-row>
        </b-container>
        <b-button v-if="spectator || spectator != ''" id="logout-button" size="sm" @click="logout">Logout</b-button>

    </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'


export default {
    name: "Spectator",
    data() {
        return {
            gamename: "",
            duration: "",
            text: "",
            selectedActors: [],
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
            currentUser: state => state.game.currentUser,
            spectator: state => state.game.spectator
        }),
        ...mapGetters('game', [
            'getActorNameById',
        ])
    },
    //verwendete Methoden werden definiert
    methods: {...mapActions('game', [
        'deleteTask',
        'readOut',
        'createGame',
        'getGameByName',
        'joinGameAsSpectator'
    ]),
    //Methode addTask wird aufgerufen und entsprechende felder geleert
    addTask(task){
        this.$store.dispatch('game/addTask', task);
        //nachdem die addTask Aktion ausgeführt wird
        //werden Text und angewählten actors zurückgesetzt
        this.text = ''
        this.selectedActors= []
    },
        logout() {
            this.$store.dispatch('login/AUTH_LOGOUT')
                .then(() => {
                    this.$router.push('/')
                })
        }
    },
    //beim neuladen der seite wird der User neu geholt
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
