/**
 * Task item component
 * References: Task T239, Spec §X
 */
import { useState } from 'react';

interface TaskItemProps {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  onToggle: (id: number) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  loading?: boolean;
}

export default function TaskItem({ id, title, description, completed, onToggle, onEdit, onDelete, loading = false }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);
  const [editDescription, setEditDescription] = useState(description || '');

  const handleSaveEdit = () => {
    // In a real application, you would call an API to update the task
    // For now, we'll just call the onEdit callback
    onEdit(id);
    setIsEditing(false);
  };

  return (
    <div className={`bg-white shadow overflow-hidden sm:rounded-lg mb-4 ${completed ? 'opacity-70' : ''}`}>
      {isEditing ? (
        <div className="px-4 py-5 sm:px-6">
          <div className="mb-4">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              required
            />
          </div>
          <div className="mb-4">
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              rows={3}
            />
          </div>
          <div className="flex space-x-3">
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={() => setIsEditing(false)}
              className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="px-4 py-5 sm:px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={completed}
                onChange={() => onToggle(id)}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <div className="ml-3">
                <h3 className={`text-lg leading-6 font-medium ${completed ? 'line-through' : ''}`}>
                  {title}
                </h3>
                {description && (
                  <p className="mt-1 max-w-2xl text-sm text-gray-500">
                    {description}
                  </p>
                )}
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(id)}
                className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-white bg-red-600 shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </div>
          </div>
          <div className="mt-2 flex items-center">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
              {completed ? 'Completed' : 'Pending'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}