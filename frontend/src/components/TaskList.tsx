import React from 'react';
import { Task } from '../types/task';

interface TaskListProps {
  tasks: Task[];
  onTaskToggle: (id: string) => void;
  onTaskDelete: (id: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskToggle, onTaskDelete }) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center p-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '1rem', color: 'var(--gray-400)' }}>
          <path d="M12 2v20M5 5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5Z"/>
        </svg>
        <h3>No tasks yet</h3>
        <p className="text-muted">Add a new task to get started!</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      <div className="d-flex justify-between align-center mb-3">
        <div className="text-muted">{tasks.length} task{tasks.length !== 1 ? 's' : ''}</div>
        <div className="text-muted">
          {tasks.filter(t => t.completed).length} completed
        </div>
      </div>

      <div>
        {tasks.map((task) => (
          <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
            <div className="task-content">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onTaskToggle(task.id)}
                className="task-checkbox"
              />
              <div>
                <div className={`task-title ${task.completed ? 'completed' : ''}`}>
                  {task.title}
                </div>
                {task.description && (
                  <div className="task-description">{task.description}</div>
                )}
                {task.createdAt && (
                  <div className="text-xs text-muted mt-1">
                    Created: {new Date(task.createdAt).toLocaleDateString()}
                  </div>
                )}
              </div>
            </div>
            <div className="task-actions">
              <button
                onClick={() => onTaskDelete(task.id)}
                className="delete-btn"
                title="Delete task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskList;