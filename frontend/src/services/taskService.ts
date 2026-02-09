import { Task } from '../types/task';

// ✅ Base URL ko safe bana diya (no trailing slash issue)
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') ||
  'https://sz453781it-hackathon-todo.hf.space';

class TaskService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');

    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
  }

  // ✅ trailing slash added
  async getTasks(): Promise<Task[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/tasks/`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }

    return response.json();
  }

  // ✅ trailing slash added
  async createTask(title: string, description?: string): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/v1/tasks/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({
        title,
        description,
        completed: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.statusText}`);
    }

    return response.json();
  }

  // ✅ id ke baad slash (FastAPI requirement)
  async updateTask(id: string, updates: Partial<Task>): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/v1/tasks/${id}/`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.statusText}`);
    }

    return response.json();
  }

  // ✅ id ke baad slash
  async deleteTask(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/v1/tasks/${id}/`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.statusText}`);
    }
  }

  // ✅ complete endpoint with trailing slash
  async toggleTaskCompletion(id: string): Promise<Task> {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/tasks/${id}/complete/`,
      {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to toggle task completion: ${response.statusText}`);
    }

    return response.json();
  }
}

export default new TaskService();
