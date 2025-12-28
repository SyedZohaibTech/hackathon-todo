/**
 * Dashboard page
 * References: Task T241, Spec §X
 */
'use client';

import { useState, useEffect } from 'react';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';
import { useRouter } from 'next/navigation';
import { isAuthenticated, removeToken } from '@/lib/auth';

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const router = useRouter();

  // Check authentication on page load
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    } else {
      fetchTasks();
    }
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      // In a real application, you would call your backend API here
      // For now, we'll simulate the API call
      const token = localStorage.getItem('token');
      
      const response = await fetch('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setTasks(data.data || []);
      } else {
        if (response.status === 401) {
          // Token expired or invalid, redirect to login
          removeToken();
          router.push('/login');
        } else {
          setError('Failed to load tasks');
        }
      }
    } catch (err) {
      setError('An error occurred while loading tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData: { title: string; description?: string }) => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(taskData),
      });

      if (response.ok) {
        const data = await response.json();
        setTasks([...tasks, data.data]);
        setShowForm(false);
      } else {
        if (response.status === 401) {
          // Token expired or invalid, redirect to login
          removeToken();
          router.push('/login');
        } else {
          setError('Failed to create task');
        }
      }
    } catch (err) {
      setError('An error occurred while creating task');
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTask = async (id: number) => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      // Find the task to toggle
      const taskToToggle = tasks.find(task => task.id === id);
      if (!taskToToggle) return;
      
      // Update the task's completion status
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          completed: !taskToToggle.completed
        }),
      });

      if (response.ok) {
        const updatedTasks = tasks.map(task =>
          task.id === id ? { ...task, completed: !task.completed } : task
        );
        setTasks(updatedTasks);
      } else {
        if (response.status === 401) {
          // Token expired or invalid, redirect to login
          removeToken();
          router.push('/login');
        } else {
          setError('Failed to update task');
        }
      }
    } catch (err) {
      setError('An error occurred while updating task');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditTask = async (id: number) => {
    // In a real application, you would implement the edit functionality
    // For now, we'll just refresh the task list
    fetchTasks();
  };

  const handleDeleteTask = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== id));
      } else {
        if (response.status === 401) {
          // Token expired or invalid, redirect to login
          removeToken();
          router.push('/login');
        } else {
          setError('Failed to delete task');
        }
      }
    } catch (err) {
      setError('An error occurred while deleting task');
      console.error('Error deleting task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    removeToken();
    router.push('/login');
  };

  if (loading && tasks.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-lg text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
          <button
            onClick={handleLogout}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            {error && (
              <div className="rounded-md bg-red-50 p-4 mb-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}
            
            <div className="mb-6">
              <button
                onClick={() => setShowForm(!showForm)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                {showForm ? 'Cancel' : 'Add New Task'}
              </button>
            </div>
            
            {showForm && (
              <div className="mb-6">
                <TaskForm onSubmit={handleCreateTask} loading={loading} />
              </div>
            )}
            
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>
              <TaskList
                tasks={tasks}
                onToggle={handleToggleTask}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
                loading={loading}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}