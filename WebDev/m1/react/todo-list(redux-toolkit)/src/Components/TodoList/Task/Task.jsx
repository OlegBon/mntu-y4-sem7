import { useDispatch } from "react-redux";
import "./Task.css";
import { ChangeTaskState, DeleteTask } from "../../../Redux/TodoListSlice";

const Task = ({ task }) => {
  let dispatch = useDispatch();

  const ChangeActiveHandler = (task) => {
    dispatch(ChangeTaskState(task.id));
  };

  const RemoveTodoHandler = (taskId) => {
    dispatch(DeleteTask(taskId));
  };

  return (
    <div
      key={task.id}
      className={task.completed ? "Task TaskCompleted" : "Task"}
      onClick={() => ChangeActiveHandler(task)}
    >
      <input
        type="checkbox"
        onClick={() => ChangeActiveHandler(task)}
        checked={task.completed}
      />
      <p className={task.completed ? "completed" : ""}>{task.text}</p>
      <button onClick={() => RemoveTodoHandler(task.id)} className="RemoveBtn">
        Видалити задачу
      </button>
    </div>
  );
};

export default Task;
