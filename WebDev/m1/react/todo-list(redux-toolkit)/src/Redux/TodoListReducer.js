// const CHANGE_TASK_TEXT = 'CHANGE_TASK_TEXT';
// const ADD_TASK = 'ADD_TASK';
// const DELETE_TASK = 'DELETE_TASK';
// const CHANGE_TASK_STATE = 'CHANGE_TASK_STATE';
// const DELETE_ALL = 'DELETE_ALL';
//
// let initialState = {
//     tasks: [
//         {id: 1, text: 'Complete daily workout', completed: true},
//         {id: 2, text: 'Read two chapters of a book', completed: false},
//         {id: 3, text: 'Update professional LinkedIn profile', completed: true},
//         {id: 4, text: 'Plan healthy meals for the week', completed: false},
//     ],
//     taskText: '',
// }
//
// const TodoListReducer = (state = initialState, action) => {
//     switch (action.type) {
//         case CHANGE_TASK_TEXT:
//             return {
//                 ...state,
//                 taskText: action.payload,
//             }
//         case ADD_TASK:
//             return {
//                 ...state,
//                 tasks: [
//                     ...state.tasks,
//                     {
//                         id: Date.now(),
//                         text: state.taskText,
//                         completed: false,
//                     },
//                 ],
//                 taskText: ''
//             };
//         case DELETE_TASK:
//             return {
//                 ...state,
//                 tasks: state.tasks.filter(todo => todo.id !== action.payload),
//             };
//         case CHANGE_TASK_STATE:
//             return {
//                 ...state,
//                 tasks: state.tasks.map(task =>
//                     task.id === action.payload ? {...task, completed: !task.completed} : task
//                 ),
//             };
//         case DELETE_ALL:
//             return {
//                 ...state,
//                 tasks: []
//             }
//         default:
//             return state
//     }
// }
//
// export const ChangeTaskText = (taskText) => {
//     return {
//         type: CHANGE_TASK_TEXT,
//         payload: taskText
//     }
// }
//
// export const AddTask = () => {
//     return {
//         type: ADD_TASK,
//     }
// }
// export const DeleteTask = (taskId) => {
//     return {
//         type: DELETE_TASK,
//         payload: taskId
//     }
// }
//
// export const ChangeTaskState = (taskId) => {
//     return {
//         type: CHANGE_TASK_STATE,
//         payload: taskId,
//     }
// }
//
// export const DeleteAll = () => {
//     return {
//         type: DELETE_ALL,
//     }
// }
//
// export default TodoListReducer;
//
//
//
//
//
//
//
