import { createSlice } from "@reduxjs/toolkit";

const tasksSlice = createSlice({
    name: "tasks",
    initialState: {
        tasks: [],
        taskText: ''
    },
    reducers: {
        ChangeTaskText: (state, action) => {
            state.taskText = action.payload;
        },
        AddTask: (state, action) => {
            const newTask = {
                id: Date.now(),
                text: state.taskText,
                completed: false,
            };
            state.tasks.push(newTask);
            state.taskText = '';
        },
        ChangeTaskState: (state, action) => {
            const todo = state.tasks.find((todo) => todo.id === action.payload);
            if (todo) {
                todo.completed = !todo.completed;
            }
        },
        DeleteTask: (state, action) => {
            const index = state.tasks.findIndex((todo) => todo.id === action.payload);
            if (index !== -1) {
                state.tasks.splice(index, 1);
            }
        },
        DeleteAll: (state, action) => {
            state.tasks = [];
        }
    },
});
export const { ChangeTaskText, AddTask, ChangeTaskState, DeleteTask, DeleteAll } = tasksSlice.actions;
export default tasksSlice.reducer;