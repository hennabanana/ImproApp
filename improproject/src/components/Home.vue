<template>
    <div id="home">
        <b-container>
            <b-row align-h="center">
                <h4>Herzlich Willkommen</h4>
            </b-row>
            <br>
            <b-row align-h="center">
                <p>Wählen Sie Ihre Rolle aus</p>
            </b-row>
            <br>
        </b-container>
        <b-container>
            <b-row align-h="center">
                <b-col>
                    <b-card title="Zuschauer" tag="article" style="max-width: 20rem;" class="mb-2">
                        <b-card-text>
                            Treten Sie dem Spiel als Zuschauer bei und Sie entscheiden was die Schauspieler auf der Bühne tun sollen!
                        </b-card-text>
    
                        <b-button variant="success" :to="{ name: 'spectator' }">Beitreten</b-button>
                    </b-card>
    
                </b-col>
                <b-col>
                    <b-card title="Schauspieler" tag="article" style="max-width: 20rem;" class="mb-2">
                        <b-card-text>
                            Treten Sie dem Spiel als Schauspieler bei. Sie benötigen Kopfhörer um die Aufgaben der Zuschauer vorgelesen zu bekommen!
                        </b-card-text>
    
                        <b-button variant="warning" :to="{ name: 'actor' }">Beitreten</b-button>
                    </b-card>
    
                </b-col>
                <b-col>
                    <b-card title="Spielleiter" tag="article" style="max-width: 20rem;" class="mb-2">
                        <b-card-text>
                            Als Spielleiter erstellen Sie ein Spiel. Zuschauer und Schauspieler können dann dem Spiel beitreten. Sie erhalten von den Zuschauern die Aufgaben und entscheiden wann diese den Schauspielern vorgelesen werden
                        </b-card-text>
    
                        <b-button :to="{ name: 'director' }">Spiel erstellen</b-button>
                    </b-card>
    
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Login from '../components/Login.vue'
export default ({
    name: 'home',

    components: {
        Login
    }
})
</script>

<style scoped>

</style>