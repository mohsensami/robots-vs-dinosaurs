<template>
  <div class="text-center">
    <div class="py-2 bg-gray-100">
      <form action="">
        <div class="grid grid-cols-2 text-center">
          <div>
            <h2>Robot</h2>
            <div class="flex gap-2 justify-center mt-2">
              <input class="number_input" type="number" min="0" max="9" value="0" />
              <input class="number_input" type="number" min="0" max="9" value="0" />
              <select class="select_option" name="" id="">
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
              <input class="number_input" type="number" min="0" max="9" value="0" />
              <input class="number_input" type="number" min="0" max="9" value="0" />
            </div>
          </div>
        </div>
        <input class="me_btn" type="button" value="Start Game" />
      </form>
    </div>
    <hr />
  </div>
</template>



<script>
import HelloWorld from "./components/HelloWorld.vue";
import { reactive, ref } from "vue";
import axios from "axios";

export default {
  setup() {
    const table = [];
  },
};
</script>


<style></style>
