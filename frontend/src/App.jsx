import { useCallback, useEffect, useState } from "react";
import api, { tokenApi } from "./api/axios";
import TaskForm from "./TaskForm";
import TaskList from "./TaskList";
import Login from "./Login";
import CategoryList from "./CategoryList";
import Register from "./Register";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loginError, setLoginError] = useState("");
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  const [isRegistering, setIsRegistering] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [registerError, setRegisterError] = useState("");
  const [registerSuccess, setRegisterSuccess] = useState("");

  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const [tasks, setTasks] = useState([]);
  const [isLoadingTasks, setIsLoadingTasks] = useState(false);
  const [isSavingTask, setIsSavingTask] = useState(false);
  const [taskError, setTaskError] = useState("");
  const [taskSuccess, setTaskSuccess] = useState("");

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [ordering, setOrdering] = useState("-created_at");

  const [categories, setCategories] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [tags, setTags] = useState([]);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("MEDIUM");
  const [status, setStatus] = useState("TODO");
  const [category, setCategory] = useState("");

  const [editingTaskId, setEditingTaskId] = useState(null);

  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);

  const loadTasks = useCallback(
    async (url = null) => {
      setIsLoadingTasks(true);
      setTaskError("");

      try {
        if (!url) {
          const params = new URLSearchParams();

          if (search) {
            params.append("search", search);
          }

          if (statusFilter) {
            params.append("status", statusFilter);
          }

          if (ordering) {
            params.append("ordering", ordering);
          }

          url = `/tasks/?${params.toString()}`;
        }

        const response = await api.get(url);

        setTasks(response.data.results);
        setNextPage(response.data.next);
        setPreviousPage(response.data.previous);
      } catch (error) {
        console.error(
          "Tasks error:",
          error.response?.data || error
        );

        setTaskError(
          "Unable to load tasks. Please try again."
        );
      } finally {
        setIsLoadingTasks(false);
      }
    },
    [search, statusFilter, ordering]
  );

  const loadDashboardData = async () => {
    setTaskError("");

    try {
      const [
        tasksResponse,
        categoriesResponse,
        tagsResponse,
      ] = await Promise.all([
        api.get("/tasks/?ordering=-created_at"),
        api.get("/categories/"),
        api.get("/tags/"),
      ]);

      setTasks(tasksResponse.data.results);
      setNextPage(tasksResponse.data.next);
      setPreviousPage(tasksResponse.data.previous);

      setCategories(
        categoriesResponse.data.results ||
          categoriesResponse.data
      );

      setTags(
        tagsResponse.data.results ||
          tagsResponse.data
      );
    } catch (error) {
      console.error(
        "Dashboard loading error:",
        error.response?.data || error
      );

      setTaskError(
        "Unable to load dashboard data. Please try again."
      );
    }
  };

  useEffect(() => {
    if (!taskSuccess) {
      return;
    }

    const timer = setTimeout(() => {
      setTaskSuccess("");
    }, 3000);

    return () => clearTimeout(timer);
  }, [taskSuccess]);

  const handleLogin = async (event) => {
    event.preventDefault();

    setLoginError("");
    setIsLoggingIn(true);

    try {
      const response = await tokenApi.post("", {
        username,
        password,
      });

      localStorage.setItem(
        "access_token",
        response.data.access
      );

      localStorage.setItem(
        "refresh_token",
        response.data.refresh
      );

      await loadDashboardData();

      setIsLoggedIn(true);
      setPassword("");
    } catch (error) {
      if (
        error.response &&
        error.response.status === 401
      ) {
        setLoginError(
          "Invalid username or password."
        );
      } else {
        setLoginError(
          "Unable to login. Please try again."
        );
      }
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleRegister = async (event) => {
    event.preventDefault();

    setRegisterError("");
    setRegisterSuccess("");
    setIsRegistering(true);

    try {
      await api.post("/register/", {
        username,
        password,
      });

      setShowRegister(false);
      setPassword("");
      setRegisterError("");
      setRegisterSuccess(
        "Account created successfully. Please log in."
      );
    } catch (error) {
      if (error.response?.data) {
        const data = error.response.data;

        if (data.username) {
          setRegisterError(data.username[0]);
        } else if (data.password) {
          setRegisterError(data.password[0]);
        } else if (data.detail) {
          setRegisterError(data.detail);
        } else {
          setRegisterError(
            "Unable to create account."
          );
        }
      } else {
        setRegisterError(
          "Unable to create account."
        );
      }
    } finally {
      setIsRegistering(false);
    }
  };

  const handleCreateTask = async (event) => {
    event.preventDefault();

    setTaskError("");
    setTaskSuccess("");
    setIsSavingTask(true);

    try {
      if (editingTaskId) {
        await api.patch(
          `/tasks/${editingTaskId}/`,
          {
            title,
            description,
            priority,
            status,
            category: category || null,
            tags: selectedTags,
          }
        );

        setTaskSuccess(
          "Task updated successfully."
        );
      } else {
        await api.post("/tasks/", {
          title,
          description,
          priority,
          status,
          category: category || null,
          completed: false,
          tags: selectedTags,
        });

        setTaskSuccess(
          "Task created successfully."
        );
      }

      setTitle("");
      setDescription("");
      setPriority("MEDIUM");
      setStatus("TODO");
      setEditingTaskId(null);
      setCategory("");
      setSelectedTags([]);

      await loadTasks();
    } catch (error) {
      console.error(
        "Task save error:",
        error.response?.data || error
      );

      setTaskError(
        "Unable to save task. Please try again."
      );
    } finally {
      setIsSavingTask(false);
    }
  };

  const handleEditTask = (task) => {
    setEditingTaskId(task.id);
    setTitle(task.title);
    setDescription(task.description);
    setPriority(task.priority);
    setStatus(task.status);
    setCategory(task.category || "");
    setSelectedTags(task.tags || []);
  };

  const handleTagChange = (tagId) => {
    setSelectedTags((currentTags) =>
      currentTags.includes(tagId)
        ? currentTags.filter(
            (id) => id !== tagId
          )
        : [...currentTags, tagId]
    );
  };

  const handleDeleteTask = async (taskId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this task?"
    );

    if (!confirmed) {
      return;
    }

    try {
      await api.delete(`/tasks/${taskId}/`);

      setTaskSuccess(
        "Task deleted successfully."
      );

      console.log(
        "Task deleted successfully"
      );

      await loadTasks();
    } catch (error) {
      console.error(
        "Delete task error:",
        error.response?.data || error
      );

      setTaskError(
        "Unable to delete task. Please try again."
      );
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    setIsLoggedIn(false);
    setTasks([]);
    setCategories([]);
    setTags([]);
  };

  if (!isLoggedIn) {
    if (showRegister) {
      return (
        <Register
          username={username}
          setUsername={setUsername}
          password={password}
          setPassword={setPassword}
          handleRegister={handleRegister}
          registerError={registerError}
          isRegistering={isRegistering}
          setShowRegister={setShowRegister}
          registerSuccess={registerSuccess}
        />
      );
    }

    return (
      <Login
        username={username}
        setUsername={setUsername}
        password={password}
        setPassword={setPassword}
        handleLogin={handleLogin}
        loginError={loginError}
        isLoggingIn={isLoggingIn}
        setShowRegister={setShowRegister}
      />
    );
  }

  return (
    <div className="app">
      <div className="dashboard">
        <div className="dashboard-header">
          <div>
            <h1>Task Dashboard</h1>

            <p className="welcome-text">
              Welcome, <strong>{username}</strong>
            </p>
          </div>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>

        <hr />

        <div className="section">
          {taskSuccess && (
            <p className="task-success">
              {taskSuccess}
            </p>
          )}

          <TaskForm
            title={title}
            setTitle={setTitle}
            description={description}
            setDescription={setDescription}
            priority={priority}
            setPriority={setPriority}
            status={status}
            setStatus={setStatus}
            category={category}
            setCategory={setCategory}
            categories={categories}
            tags={tags}
            selectedTags={selectedTags}
            handleTagChange={handleTagChange}
            handleSubmit={handleCreateTask}
            editingTaskId={editingTaskId}
            isSavingTask={isSavingTask}
          />
        </div>

        <div className="section">
          <CategoryList
            categories={categories}
          />
        </div>

        <div className="section">
          <h2>Task Filters</h2>

          <div className="task-filters">
            <input
              type="text"
              placeholder="Search tasks..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />

            <select
              value={statusFilter}
              onChange={(event) =>
                setStatusFilter(event.target.value)
              }
            >
              <option value="">
                All Statuses
              </option>

              <option value="TODO">
                To Do
              </option>

              <option value="IN_PROGRESS">
                In Progress
              </option>

              <option value="COMPLETED">
                Completed
              </option>

              <option value="CANCELLED">
                Cancelled
              </option>
            </select>

            <select
              value={ordering}
              onChange={(event) =>
                setOrdering(event.target.value)
              }
            >
              <option value="-created_at">
                Newest First
              </option>

              <option value="created_at">
                Oldest First
              </option>

              <option value="title">
                Title A-Z
              </option>
            </select>

            <button
              className="filter-button"
              onClick={() => loadTasks()}
              disabled={isLoadingTasks}
            >
              {isLoadingTasks
                ? "Loading..."
                : "Apply Filters"}
            </button>
          </div>
        </div>

        <div className="section">
          {isLoadingTasks ? (
            <p className="loading-message">
              Loading tasks...
            </p>
          ) : taskError ? (
            <p className="task-error">
              {taskError}
            </p>
          ) : (
            <TaskList
              tasks={tasks}
              categories={categories}
              tags={tags}
              handleEditTask={handleEditTask}
              handleDeleteTask={handleDeleteTask}
              hasFilters={
                search !== "" ||
                statusFilter !== "" ||
                ordering !== "-created_at"
              }
            />
          )}
        </div>

        <div className="pagination">
          <button
            onClick={() =>
              loadTasks(previousPage)
            }
            disabled={!previousPage}
          >
            Previous
          </button>

          {" "}

          <button
            onClick={() =>
              loadTasks(nextPage)
            }
            disabled={!nextPage}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
