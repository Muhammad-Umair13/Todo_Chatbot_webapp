"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/Header";
import { Container } from "@/components/layout/Container";
import { Card, CardHeader, CardBody, CardFooter } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Alert } from "@/components/ui/Alert";
import { SkeletonList } from "@/components/ui/Skeleton";
import { api, Task } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { taskEvents } from "@/lib/task-events";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  // Fetch tasks from API
  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await api.getTasks();
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setTasks(response.data);
      }
    } catch (err) {
      setError("Failed to load tasks. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, fetchTasks]);

  // Subscribe to task events from chatbot
  useEffect(() => {
    const unsubscribe = taskEvents.subscribe(() => {
      // Refresh tasks when chatbot modifies them
      fetchTasks();
    });
    return unsubscribe;
  }, [fetchTasks]);

  const filteredTasks = tasks.filter((task) => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true;
  });

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setError("Task title is required");
      return;
    }

    setIsLoading(true);

    try {
      const response = await api.createTask({
        title: newTaskTitle.trim(),
        description: newTaskDescription.trim() || "",
      });

      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setTasks((prev) => [response.data!, ...prev]);
        setNewTaskTitle("");
        setNewTaskDescription("");
      }
    } catch (err) {
      setError("Failed to add task. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    console.log('Frontend toggle:', {taskId, userId: user?.id});
    const task = tasks.find((t) => t.id === taskId);
    if (!task) return;

    // Removed optimistic update - will refetch after API

    try {
      const response = await api.toggleTaskComplete(taskId, !task.completed);
      if (response.error) {
        setError(response.error);
      } else {
        // Refetch to sync with server
        fetchTasks();
      }
    } catch (err) {
      fetchTasks();
      setError("Failed to update task. Please try again.");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    console.log('Frontend delete:', {taskId, userId: user?.id});
    setIsLoading(true);

    try {
      const response = await api.deleteTask(taskId);
      if (response.error) {
        setError(response.error);
      } else {
        // Refetch to sync with server (consistent with toggle)
        fetchTasks();
      }
    } catch (err) {
      setError("Failed to delete task. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartEdit = (task: Task) => {
    setEditingTask(task);
  };

  const handleSaveEdit = async () => {
    if (!editingTask || !editingTask.title.trim()) return;

    setIsLoading(true);

    try {
      const response = await api.updateTask(editingTask.id, {
        title: editingTask.title,
        description: editingTask.description || "",
      });

      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setTasks((prev) =>
          prev.map((t) =>
            t.id === editingTask.id
              ? { ...response.data!, updated_at: new Date().toISOString() }
              : t
          )
        );
        setEditingTask(null);
      }
    } catch (err) {
      setError("Failed to update task. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  const taskCounts = {
    all: tasks.length,
    active: tasks.filter((t) => !t.completed).length,
    completed: tasks.filter((t) => t.completed).length,
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-secondary-50">
        <Header />
        <main className="py-8">
          <Container>
            <SkeletonList count={5} />
          </Container>
        </main>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-secondary-50">
      <Header />

      <main className="py-8">
        <Container>
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Add Task Form */}
            <div className="lg:col-span-1">
              <Card variant="bordered" className="sticky top-24">
                <CardHeader>
                  <h2 className="text-lg font-semibold text-secondary-900">
                    Add New Task
                  </h2>
                </CardHeader>
                <form onSubmit={handleAddTask}>
                  <CardBody className="space-y-4">
                    {error && (
                      <Alert variant="error" onClose={() => setError(null)}>
                        {error}
                      </Alert>
                    )}

                    <Input
                      label="Task title"
                      type="text"
                      value={newTaskTitle}
                      onChange={(e) => setNewTaskTitle(e.target.value)}
                      placeholder="What needs to be done?"
                      required
                    />

                    <div>
                      <label
                        htmlFor="description"
                        className="block text-sm font-medium text-secondary-700 mb-1.5"
                      >
                        Description (optional)
                      </label>
                      <textarea
                        id="description"
                        value={newTaskDescription}
                        onChange={(e) => setNewTaskDescription(e.target.value)}
                        placeholder="Add more details..."
                        className="block w-full rounded-lg border border-secondary-300 px-4 py-2.5 text-secondary-900 placeholder:text-secondary-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        rows={3}
                      />
                    </div>
                  </CardBody>
                  <CardFooter>
                    <Button
                      type="submit"
                      className="w-full"
                      isLoading={isLoading}
                    >
                      Add Task
                    </Button>
                  </CardFooter>
                </form>
              </Card>
            </div>

            {/* Task List */}
            <div className="lg:col-span-2">
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-secondary-900 mb-2">
                  My Tasks
                </h1>
                <p className="text-secondary-600">
                  You have {taskCounts.active} task
                  {taskCounts.active !== 1 ? "s" : ""} remaining
                </p>
              </div>

              {/* Filter Tabs */}
              <div className="flex gap-2 mb-6">
                {(["all", "active", "completed"] as const).map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      filter === f
                        ? "bg-primary-100 text-primary-700"
                        : "text-secondary-600 hover:bg-secondary-100"
                    }`}
                  >
                    {f.charAt(0).toUpperCase() + f.slice(1)}
                    <span className="ml-2 px-2 py-0.5 rounded-full text-xs bg-secondary-200 text-secondary-700">
                      {taskCounts[f]}
                    </span>
                  </button>
                ))}
              </div>

              {/* Task Items */}
              {isLoading && tasks.length === 0 ? (
                <SkeletonList count={3} />
              ) : filteredTasks.length === 0 ? (
                <Card variant="bordered">
                  <CardBody className="text-center py-12">
                    <svg
                      className="w-16 h-16 mx-auto text-secondary-300 mb-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                    <h3 className="text-lg font-medium text-secondary-900 mb-1">
                      No tasks yet
                    </h3>
                    <p className="text-secondary-600">
                      Create your first task to get started!
                    </p>
                  </CardBody>
                </Card>
              ) : (
                <div className="space-y-3">
                  {filteredTasks.map((task) => (
                    <Card
                      key={task.id}
                      variant={task.completed ? "default" : "bordered"}
                      className={`transition-all ${
                        task.completed ? "opacity-60" : ""
                      }`}
                    >
                      {editingTask?.id === task.id ? (
                        // Edit Mode
                        <CardBody className="space-y-4">
                          <Input
                            label="Task title"
                            type="text"
                            value={editingTask.title}
                            onChange={(e) =>
                              setEditingTask({
                                ...editingTask,
                                title: e.target.value,
                              })
                            }
                            required
                          />
                          <div>
                            <label
                              htmlFor="edit-description"
                              className="block text-sm font-medium text-secondary-700 mb-1.5"
                            >
                              Description
                            </label>
                            <textarea
                              id="edit-description"
                              value={editingTask.description || ""}
                              onChange={(e) =>
                                setEditingTask({
                                  ...editingTask,
                                  description: e.target.value,
                                })
                              }
                              className="block w-full rounded-lg border border-secondary-300 px-4 py-2.5 text-secondary-900 focus:outline-none focus:ring-2 focus:ring-primary-500"
                              rows={2}
                            />
                          </div>
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              onClick={handleSaveEdit}
                              isLoading={isLoading}
                            >
                              Save
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={handleCancelEdit}
                            >
                              Cancel
                            </Button>
                          </div>
                        </CardBody>
                      ) : (
                        // View Mode
                        <CardBody className="py-4">
                          <div className="flex items-start gap-4">
                            <button
                              onClick={() => handleToggleComplete(task.id)}
                              className={`flex-shrink-0 w-5 h-5 rounded border-2 transition-colors ${
                                task.completed
                                  ? "bg-primary-500 border-primary-500 text-white"
                                  : "border-secondary-300 hover:border-primary-400"
                              }`}
                              aria-label={
                                task.completed
                                  ? "Mark as incomplete"
                                  : "Mark as complete"
                              }
                            >
                              {task.completed && (
                                <svg
                                  className="w-full h-full p-0.5"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={3}
                                    d="M5 13l4 4L19 7"
                                  />
                                </svg>
                              )}
                            </button>

                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <h3
                                  className={`font-medium text-secondary-900 ${
                                    task.completed
                                      ? "line-through text-secondary-500"
                                      : ""
                                  }`}
                                >
                                  {task.title}
                                </h3>
                              </div>
                              {task.description && (
                                <p
                                  className={`text-sm text-secondary-600 ${
                                    task.completed ? "line-through" : ""
                                  }`}
                                >
                                  {task.description}
                                </p>
                              )}
                              <p className="text-xs text-secondary-400 mt-2">
                                Created{" "}
                                {new Date(task.created_at).toLocaleDateString()}
                              </p>
                            </div>

                            <div className="flex items-center gap-2 flex-shrink-0">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleStartEdit(task)}
                                className="text-secondary-500 hover:text-secondary-700"
                              >
                                <svg
                                  className="w-4 h-4"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                                  />
                                </svg>
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteTask(task.id)}
                                className="text-red-500 hover:text-red-700 hover:bg-red-50"
                              >
                                <svg
                                  className="w-4 h-4"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                                  />
                                </svg>
                              </Button>
                            </div>
                          </div>
                        </CardBody>
                      )}
                    </Card>
                  ))}
                </div>
              )}
            </div>
          </div>
        </Container>
      </main>
    </div>
  );
}
