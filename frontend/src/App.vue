<template>
  <div class="text-center">
    <div class="py-2 bg-gray-100">
      <form @submit.prevent="gameStart">
        <div class="grid grid-cols-2 text-center">
          <div>
            <h2>Robot</h2>
            <div class="flex gap-2 justify-center mt-2">
              <input v-model="startGame.rx" class="number_input" type="number" min="0" max="9" />
              <input v-model="startGame.ry" class="number_input" type="number" min="0" max="9" />
              <select v-model="startGame.rs" class="select_option" name="" id="">
                <option value="N">N</option>
                <option value="E">E</option>
                <option value="S">S</option>
                <option value="W">W</option>
              </select>
            </div>
          </div>
          <div>
            <h2>Dionausor</h2>
            <div class="flex gap-2 justify-center mt-2">
              <input v-model="startGame.dx" class="number_input" type="number" min="0" max="9" />
              <input v-model="startGame.dy" class="number_input" type="number" min="0" max="9" />
            </div>
          </div>
        </div>
        <input class="me_btn bg-green-100 border-green-300" type="submit" value="Start Game" />
        <input @click="endGames()" v-if="game_id" class="me_btn bg-red-100 border-red-300 ml-2" type="btn" value="End Game" />
      </form>
    </div>
    <hr />
    <div>
      {{startGame}}
      <hr>
      {{game_id}}
      <hr>
      <div class="text-center" v-html="table"></div>
    </div>
  </div>
</template>



<script>
import HelloWorld from "./components/HelloWorld.vue";
import { reactive, ref } from "vue";
import axios from "axios";

export default {
  setup() {
    const game_id = ref('');
    const table = ref([]);
    const startGame = reactive({
      dx: "0",
      dy: "0",
      rx: "0",
      ry: "0",
      rs: "N",
    });
    const gameStart = () => {
      axios
      .post("http://127.0.0.1:8000/games/start/", 
        { 
          grid_dim: 10, 
          robots_count: 1, 
          robots: [
            {"coordinate":[2,2], "direction":"E"}
          ], 
          dinosaurs_count: 1, 
          dinosaurs: [[4,5]], 
        }
      )
      .then(({ data }) => {
        game_id.value = data.game_id;
        getData();
      })
      .catch((error) => {
        console.log(error);
        if(error.response.data.message) {
          // error.value = error.response.data.message[0].messages[0].message;
        }
        // errorText.value = "error";
      });
      };


      const getData = () => {
      axios
      .get("http://127.0.0.1:8000/games/" + game_id.value)
      .then(({ data }) => {
        table.value=data;
      })
      .catch((error) => {
        console.log(error);
        if(error.response.data.message) {
          // error.value = error.response.data.message[0].messages[0].message;
        }
        // errorText.value = "error";
      });
      };


      const endGames = () => {
        axios
        .delete("http://127.0.0.1:8000/games/" + game_id.value)
        .then(({ data }) => {
        table.value=data;
        })
        .catch((error) => {
          console.log(error);
          if(error.response.data.message) {
            // error.value = error.response.data.message[0].messages[0].message;
          }
          // errorText.value = "error";
        });
      }


    
    return {startGame, gameStart, getData, table, game_id, endGames};
  },

};
</script>


<style></style>
