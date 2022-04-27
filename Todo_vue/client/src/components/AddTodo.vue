<template>
  <div>
    <input
      v-model="inputText"
      type="text"
      @keyup.enter="addTodo"
      placeholder="Type Todo"
      @input="saveInputText"
    />
    <button @click="addTodo">Add</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputText: "",
    };
  },
  methods: {
    addTodo() {
      this.$emit("add-todo", this.inputText);
      this.inputText = "";
    },
    saveInputText(e) {
      this.inputText = e.target.value;
    },
  },
};
</script>

<style></style>
