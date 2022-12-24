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
        <input class="me_btn bg-green-100 border-green-300" v-if="!game_id" type="submit" value="Start Game" />
        <input @click="endGames()" v-if="game_id" class="me_btn bg-red-100 border-red-300 ml-2" type="btn" value="End Game" />
      </form>
    </div>
    <hr />
    <div>
      <div class="text-center" v-html="table"></div>
      <div>
        <input @click="gameMove(0)" v-if="game_id" class="me_btn bg-gray-100 border-gray-300 ml-2" type="btn" value="Forward" />
        <input @click="gameMove(1)" v-if="game_id" class="me_btn bg-gray-100 border-gray-300 ml-2" type="btn" value="Backward" />
        <input @click="gameMove(2)" v-if="game_id" class="me_btn bg-gray-100 border-gray-300 ml-2" type="btn" value="Turn Right" />
        <input @click="gameMove(3)" v-if="game_id" class="me_btn bg-gray-100 border-gray-300 ml-2" type="btn" value="Turn Left" />
      </div>
    </div>
  </div>
</template>



<script>
import { reactive, ref } from "vue";
import axios from "axios";

export default {
  setup() {
    const game_id = ref("");
    const table = ref([]);
    const startGame = reactive({
      dx: 9,
      dy: 9,
      rx: 2,
      ry: 2,
      rs: "S",
    });
    const gameStart = async () => {
      await axios
        .post("http://127.0.0.1:8000/games/start/", {
          grid_dim: 10,
          robots_count: 1,
          robots: [{ coordinate: [startGame.rx, startGame.ry], direction: `${startGame.rs}` }],
          dinosaurs_count: 1,
          dinosaurs: [[startGame.dx, startGame.dy]],
        })
        .then(({ data }) => {
          game_id.value = data.game_id;
          getData();
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getData = async () => {
      await axios
        .get("http://127.0.0.1:8000/games/" + game_id.value)
        .then(({ data }) => {
          table.value = data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const gameMove = async (value) => {
      await axios
        .put("http://127.0.0.1:8000/games/" + game_id.value, {
          robot_id: 0,
          command: value,
        })
        .then(({ data }) => {
          console.log(data.new_position);
          console.log(data.new_position.coordinate[0]);
          startGame.rx = data.new_position.coordinate[0];
          startGame.ry = data.new_position.coordinate[1];
          getData();
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const endGames = async () => {
      await axios
        .delete("http://127.0.0.1:8000/games/" + game_id.value)
        .then(({ data }) => {
          table.value = data;
          game_id.value = "";
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return { startGame, gameStart, getData, table, game_id, endGames, gameMove };
  },
};
</script>


<style></style>
