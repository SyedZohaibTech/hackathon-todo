/**
 * Task list component
 * References: Task T240, Spec §X
 */
import TaskItem from './TaskItem';

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
}

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: number) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  loading?: boolean;
}

export default function TaskList({ tasks, onToggle, onEdit, onDelete, loading = false }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          <li>
            <div className="px-4 py-4 sm:px-6">
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-500">No tasks yet. Add your first task!</p>
              </div>
            </div>
          </li>
        </ul>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-gray-200">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            id={task.id}
            title={task.title}
            description={task.description}
            completed={task.completed}
            onToggle={onToggle}
            onEdit={onEdit}
            onDelete={onDelete}
            loading={loading}
          />
        ))}
      </ul>
    </div>
  );
}