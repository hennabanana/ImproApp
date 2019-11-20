<template>
    <div class="Director">
        <!-- Wenn das Spiel noch nicht gesetzt ist wird dieser Container angezeigt -->
        <b-container v-if="game== ''">
            <b-row align-h="center">
                <b-col md="4">
                    <b-form>
                        <b-form-group label="Geben Sie ein Spielnamen ein und legen Sie eine Dauer fest. Anschließend wählen Sie Spiel erstellen und teilen den Zuschauern und Schauspielern den Spielname mit.">
                            <!-- v-model ist mit der Vue- Variable verbunden-->
                            <b-form-input type="text" placeholder="Spielname" v-model="gamename" />
                            <b-form-input type="number" min="0" max="100" placeholder="Dauer" v-model="duration" />
                        </b-form-group>
                        <!-- wird der Button geklickt, wird die Methode createGame mit mit den Parametern aufgerufen-->
                        <!-- :disabled ist der button wenn entweder der gamename oder die duration leer sind-->
                        <b-button @click="createGame({name: gamename, duration:duration, director:director})" :disabled="!gamename || !duration">Spiel erstellen</b-button>
                    </b-form>
                </b-col>
            </b-row>
        </b-container>
         <!-- Wenn das Spiel gesetzt ist wird dieser Container angezeigt -->
        <b-container v-if="game != ''">
            <b-row align-h="center">
                <b-col md="6">
                    <h4>Spielleiter</h4>
                    <b-tabs content-class="mt-3">
                        <b-tab title="Aufgabe erfassen" active>
                            <b-form>
                            <b-row class="m-3" align-h="center">
                            <b>Schauspieler:</b>
                            </b-row>
                                <b-row class="m-3" align-h="center">
                                    <!-- Es wird über die Liste der Actors itteriert und für jeden Actor eine Checkbox angelegt -->
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
                        <b-tab title="Aufgaben steuern">
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
                                    <b-button v-on:click="readOut(task)" class="btn"> &#9658;</b-button>
                                    <b-button v-on:click="deleteTask(task.id)" class="btn">&#10005;</b-button>
                                </b-card>
                            </div>
                        </b-tab>
    
                    </b-tabs>
                </b-col>
            </b-row>
        </b-container>
        <b-button v-if="director != '' || currentUser || currentUser != ''" id="logout-button" size="sm" @click="logout">Logout</b-button>
    
    </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
export default {
    name: "Director",
    data() {
        return {
            //variablen die nur fuer den HTML Teil
            //genutzt werden
            gamename: "",
            duration: "",
            text: "",
            selectedActors: [],
        };
    },
    computed: {
        //State-Variablen aus dem Store game
        ...mapState({
            //liste aller Tasks
            tasks: state => state.game.tasks, 
            //liste aller Actors
            actors: state => state.game.actors,
            //Director Objekt
            director: state => state.game.director,
            //Game Objekt
            game: state => state.game.game,
            //Objekt des aktuellen Benutzers
            currentUser: state => state.game.currentUser
        }),
        //Getter aus dem Store Game
        ...mapGetters('game', [
            'getActorNameById'
        ])
    },
    //Actionen aus dem Store Game
    methods: { ...mapActions('game', [
            'deleteTask', //Aufgabe loeschen
            'readOut', //Aufgabe vorlesen
            'createGame', //Game erstellen
        ]),
        //ruft Methode addTask auf und bereinig text und selectedActors
        //nach dem die Task hinzugefuegt wurde
        addTask(task) {
            this.$store.dispatch('game/addTask', task);
            this.text = ''
            this.selectedActors = []
        },
        //nach dem Logout aufruf wird die die URL also Home aufgerufen
        logout() {
            this.$store.dispatch('login/AUTH_LOGOUT')
                .then(() => {
                    this.$router.push('/')
                })
        }
    },
    //Methode die beim Laden der Seite aufgerufen wird
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
