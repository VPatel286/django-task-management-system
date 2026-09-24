function TaskForm({
    title,
    setTitle,
    description,
    setDescription,
    priority,
    setPriority,
    status,
    setStatus,
    category,
    setCategory,
    categories,
    tags,
    selectedTags,
    handleTagChange,
    handleSubmit,
    editingTaskId,
    isSavingTask,
}) {
    return (
        <>
            <h2>{editingTaskId ? "Edit Task" : "Create Task"}</h2>

            <form className="task-form" onSubmit={handleSubmit}>
                <div>
                    <input
                        type="text"
                        placeholder="Task title"
                        value={title}
                        onChange={(event) => setTitle(event.target.value)}
                    />
                </div>

                <div>
                    <textarea
                        placeholder="Task description"
                        value={description}
                        onChange={(event) =>
                            setDescription(event.target.value)
                        }
                    />
                </div>

                <div>
                    <label>Priority: </label>

                    <select
                        value={priority}
                        onChange={(event) =>
                            setPriority(event.target.value)
                        }
                    >
                        <option value="LOW">Low</option>
                        <option value="MEDIUM">Medium</option>
                        <option value="HIGH">High</option>
                        <option value="URGENT">Urgent</option>
                    </select>
                </div>

                <div>
                    <label>Status: </label>

                    <select
                        value={status}
                        onChange={(event) =>
                            setStatus(event.target.value)
                        }
                    >
                        <option value="TODO">To Do</option>
                        <option value="IN_PROGRESS">In Progress</option>
                        <option value="COMPLETED">Completed</option>
                        <option value="CANCELLED">Cancelled</option>
                    </select>
                </div>

                <div>
                    <label>Category: </label>

                    <select
                        value={category}
                        onChange={(event) =>
                            setCategory(event.target.value)
                        }
                    >
                        <option value="">No Category</option>

                        {categories.map((categoryItem) => (
                            <option
                                key={categoryItem.id}
                                value={categoryItem.id}
                            >
                                {categoryItem.name}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label>Tags:</label>

                    {tags.length === 0 ? (
                        <p>No tags found.</p>
                    ) : (
                        <div className="tags-container">
                            {tags.map((tag) => (
                                <label
                                    key={tag.id}
                                    className="tag-option"
                                >
                                    <input
                                        type="checkbox"
                                        value={tag.id}
                                        checked={selectedTags.includes(tag.id)}
                                        onChange={() => handleTagChange(tag.id)}
                                    />
                                    {tag.name}
                                </label>
                            ))}
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={isSavingTask}
                >
                    {isSavingTask
                        ? editingTaskId
                            ? "Updating..."
                            : "Creating..."
                        : editingTaskId
                            ? "Update Task"
                            : "Create Task"}
                </button>
            </form>
        </>
    );
}

export default TaskForm;