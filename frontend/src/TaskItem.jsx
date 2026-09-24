function TaskItem({
    task,
    categories,
    tags,
    handleEditTask,
    handleDeleteTask,
}) {
    return (
        <div className="task-card">
            <h3>{task.title}</h3>

            <p>{task.description}</p>

            <p>
                <strong>Status:</strong>{" "}
                <span className={`status-badge status-${task.status.toLowerCase()}`}>
                    {task.status
                        .replace("_", " ")
                        .toLowerCase()
                        .replace(/\b\w/g, (letter) => letter.toUpperCase())}
                </span>
            </p>

            <p>
                <strong>Priority:</strong>{" "}
                <span
                    className={`priority-badge priority-${task.priority.toLowerCase()}`}
                >
                    {task.priority}
                </span>
            </p>

            <p>
                <strong>Category:</strong>{" "}
                {task.category
                    ? categories.find(
                        (category) => category.id === task.category
                    )?.name || "Unknown"
                    : "None"}
            </p>

            <p>
                <strong>Tags:</strong>{" "}
                {task.tags && task.tags.length > 0
                    ? task.tags
                        .map(
                            (tagId) =>
                                tags.find((tag) => tag.id === tagId)?.name
                        )
                        .filter(Boolean)
                        .join(", ")
                    : "None"}
            </p>

            <div className="task-actions">
                <button
                    className="edit-button"
                    onClick={() => handleEditTask(task)}
                >
                    Edit
                </button>

                <button
                    className="delete-button"
                    onClick={() => handleDeleteTask(task.id)}
                >
                    Delete
                </button>
            </div>

        </div>
    );
}

export default TaskItem;