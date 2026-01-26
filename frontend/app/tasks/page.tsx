'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import taskService from '@/services/taskService';
import { Task } from '@/types/task';

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    setStats({
      total: tasks.length,
      completed: tasks.filter(task => task.completed).length,
      pending: tasks.filter(task => !task.completed).length
    });
  }, [tasks]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await taskService.getTasks();
      setTasks(tasksData);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      alert('Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    try {
      const newTask = await taskService.createTask(title, description);
      setTasks([newTask, ...tasks]); // Add to top of list
    } catch (error) {
      console.error('Error creating task:', error);
      alert('Failed to create task');
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      const updatedTask = await taskService.toggleTaskCompletion(id);
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (error) {
      console.error('Error toggling task:', error);
      alert('Failed to update task');
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskService.deleteTask(id);
        setTasks(tasks.filter(task => task.id !== id));
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task');
      }
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-center align-center" style={{ minHeight: '400px' }}>
        <div className="spinner"></div>
        <span className="ml-2">Loading tasks...</span>
      </div>
    );
  }

  return (
    <div className="tasks-page">
      <div className="d-flex justify-between align-center mb-4">
        <h1>Task Manager</h1>
        <div className="d-flex gap-4">
          <div className="card" style={{ minWidth: '120px' }}>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: 'var(--primary-color)' }}>{stats.total}</div>
              <div className="text-sm text-muted">Total</div>
            </div>
          </div>
          <div className="card" style={{ minWidth: '120px' }}>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: 'var(--success-color)' }}>{stats.completed}</div>
              <div className="text-sm text-muted">Completed</div>
            </div>
          </div>
          <div className="card" style={{ minWidth: '120px' }}>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: 'var(--warning-color)' }}>{stats.pending}</div>
              <div className="text-sm text-muted">Pending</div>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="card-title">Add New Task</h2>
        <TaskForm onSubmit={handleAddTask} />
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Your Tasks</h2>
        </div>
        <TaskList
          tasks={tasks}
          onTaskToggle={handleToggleTask}
          onTaskDelete={handleDeleteTask}
        />
      </div>
    </div>
  );
};

export default TasksPage;