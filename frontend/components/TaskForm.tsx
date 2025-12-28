/**
 * Task form component
 * References: Task T238, Spec §X
 */
import { useState } from 'react';

interface TaskFormData {
  title: string;
  description?: string;
}

interface TaskFormProps {
  onSubmit: (taskData: TaskFormData) => void;
  loading?: boolean;
  error?: string;
  initialData?: TaskFormData;
  submitText?: string;
}

export default function TaskForm({ onSubmit, loading = false, error, initialData = { title: '', description: '' }, submitText = 'Create Task' }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskFormData>(initialData);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
      <div className="md:grid md:grid-cols-3 md:gap-6">
        <div className="md:col-span-1">
          <h3 className="text-lg font-medium leading-6 text-gray-900">Task Details</h3>
          <p className="mt-1 text-sm text-gray-500">Fill in the details for your task.</p>
        </div>
        <div className="mt-5 md:mt-0 md:col-span-2">
          <form onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-md bg-red-50 p-4 mb-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}
            <div className="grid grid-cols-6 gap-6">
              <div className="col-span-6">
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                  Title *
                </label>
                <input
                  type="text"
                  name="title"
                  id="title"
                  required
                  minLength={1}
                  maxLength={100}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.title}
                  onChange={handleChange}
                />
              </div>

              <div className="col-span-6">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  rows={3}
                  maxLength={500}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.description}
                  onChange={handleChange}
                />
                <p className="mt-2 text-sm text-gray-500">Optional. Max 500 characters.</p>
              </div>
            </div>

            <div className="mt-6">
              <button
                type="submit"
                disabled={loading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Saving...' : submitText}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}