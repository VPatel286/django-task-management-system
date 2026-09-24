import TaskItem from "./TaskItem";

function TaskList({
    tasks,
    categories,
    tags,
    handleEditTask,
    handleDeleteTask,
    hasFilters,
}) {
    return (
        <>
            <h2>My Tasks</h2>

            {tasks.length === 0 ? (
                <div className="empty-state">
                    <h3>
                        {hasFilters
                            ? "No matching tasks"
                            : "No tasks yet"}
                    </h3>

                    <p>
                        {hasFilters
                            ? "Try changing your search or filters."
                            : "Create your first task to get started."}
                    </p>
                </div>
            ) : (
                tasks.map((task) => (
                    <TaskItem
                        key={task.id}
                        task={task}
                        categories={categories}
                        tags={tags}
                        handleEditTask={handleEditTask}
                        handleDeleteTask={handleDeleteTask}
                    />
                ))
            )}
        </>
    );
}

export default TaskList;