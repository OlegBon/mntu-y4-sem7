import "./TodoList.css";
import { useDispatch, useSelector } from "react-redux";
import Task from "./Task/Task";
import { AddTask, ChangeTaskText, DeleteAll } from "../../Redux/TodoListSlice";

const TodoList = () => {
  const tasks = useSelector((state) => state.tasks.tasks);
  // console.log(tasks);
  const taskText = useSelector((state) => state.tasks.taskText);
  const dispatch = useDispatch();

  const AddTaskHandler = () => {
    dispatch(AddTask());
  };
  const OnChangeHandler = (e) => {
    dispatch(ChangeTaskText(e.target.value));
  };

  const DeleteAllHandler = () => {
    dispatch(DeleteAll());
  };

  return (
    <div className="TodoList">
      <div className="inputPanel">
        <input
          type="text"
          onChange={(e) => OnChangeHandler(e)}
          value={taskText}
        />
        <button onClick={() => AddTaskHandler()}>Додати</button>
        {tasks.length > 0 ? (
          <button onClick={() => DeleteAllHandler()} className="ClearAll">
            Очистити все
          </button>
        ) : (
          <h1>Немає завдань</h1>
        )}
      </div>
      <div>
        {tasks.map((task, index) => (
          <Task key={task.id || index} task={task} />
        ))}
      </div>
    </div>
  );
};

export default TodoList;
