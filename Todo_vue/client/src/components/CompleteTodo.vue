<template>
  <div>Complete To-Do : {{ getNumberCheckedTodo }}</div>
</template>

<script>
export default {
  props: {
    todos: {
      type: Array,
      required: true,
    },
  },
  computed: {
    getNumberCheckedTodo() {
      return this.todos.filter((todo) => todo.checked === true).length;
    },
  },
};
</script>

<style></style>
