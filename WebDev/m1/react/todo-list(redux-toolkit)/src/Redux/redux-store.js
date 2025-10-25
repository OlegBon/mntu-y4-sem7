import { configureStore } from "@reduxjs/toolkit";
import tasksSlice from "./TodoListSlice";

const store = configureStore({
    reducer: {
        tasks: tasksSlice,
    },
});

export default store;