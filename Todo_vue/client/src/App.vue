<template>
  <div>
    <h1>To-Do App</h1>
    <CompleteTodo :todos="todos" />
    <AddTodo @add-todo="addTodo" />
    <hr />
    <TodoList
      :todos="todos"
      @toggle-todo="toggleTodo"
      @delete-todo="deleteTodo"
    />
  </div>
</template>

<script>
import CompleteTodo from "@/components/CompleteTodo.vue";
import AddTodo from "@/components/AddTodo.vue";
import TodoList from "@/components/TodoList.vue";
export default {
  components: {
    CompleteTodo,
    AddTodo,
    TodoList,
  },
  data() {
    return {
      todos: [
        {
          id: 1,
          title: "Study code",
          checked: true,
        },
        {
          id: 2,
          title: "Buy a note",
          checked: false,
        },
      ],
    };
  },
  methods: {
    addTodo(title) {
      let id = 0;
      let todo = {};
      if (this.todos.length === 0) {
        id = 1;
        todo = {
          id,
          title,
          checked: false,
        };
      } else {
        id = this.todos[this.todos.length - 1].id + 1;
        todo = {
          id,
          title,
          checked: false,
        };
      }
      this.todos.push(todo);
      console.log(this.todos);
    },
    toggleTodo({ id, checked }) {
      const idx = this.todos.findIndex((el) => el.id === id);
      this.todos[idx].checked = checked;
      console.log(this.todos);
    },
    deleteTodo(id) {
      const idx = this.todos.findIndex((el) => el.id === id);
      this.todos.splice(idx, 1);
      console.log(this.todos);
    },
  },
};
</script>

<style></style>
