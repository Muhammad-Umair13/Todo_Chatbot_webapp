# Quickstart Guide: Todo Console Application

## Installation

### Prerequisites
- Python 3.13 or higher
- pip (comes with Python)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd todo_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -e .
```

### Run the Application

```bash
# Run the interactive menu
python todo_apps/main.py

# Or using UV
uv run main.py
```

---

## Usage Tutorial

The application provides a fully interactive menu system. When you run the application, you'll see:

```
╔════════════════════════════════════════════╗
║          📝 TODO APP - MAIN MENU          ║
╚════════════════════════════════════════════╝

1. ➕ Add New Task
2. 👀 View Tasks
3. ✅ Mark Task Complete
4. 🗑️  Delete Task
5. ✏️  Update Task
6. 🔄 Exit

Choose an option (1-6):
```

### Adding Tasks

1. Select option `1` from the main menu
2. Enter task title when prompted
3. Optionally add description, priority, tags, and due date
4. Your task is created!

### Viewing Tasks

1. Select option `2` from the main menu
2. Choose filter options (All, Completed, Pending)
3. Select sorting preferences
4. View your tasks with colors and priority indicators

### Completing Tasks

1. Select option `3` from the main menu
2. Enter the task ID to mark as complete
3. Task status is updated!

### Updating Tasks

1. Select option `5` from the main menu
2. Enter the task ID to update
3. Modify title, description, priority, tags, or due date as needed

### Deleting Tasks

1. Select option `4` from the main menu
2. Enter the task ID to delete
3. Task is removed from your list

---

## Common Workflows

### Daily Task Management

1. Run the application: `python todo_apps/main.py`
2. Add your daily tasks using the interactive wizard
3. View tasks to see what's pending
4. Mark tasks as complete as you finish them
5. Use the statistics menu to track your progress

### Features

- **Priority Levels**: Set tasks as high, medium, or low priority
- **Tags**: Organize tasks with custom tags
- **Due Dates**: Set deadlines using natural language (e.g., "tomorrow", "next monday")
- **Search & Filter**: Find tasks by keywords, tags, or status
- **Statistics**: View completion rates and task summaries

---

## Error Handling Examples

### Invalid Task ID

```bash
todo complete 999
```

Output:
```
Error: Task 999 not found.
```

### Empty Title

```bash
todo add ""
```

Output:
```
Error: Title cannot be empty.
```

### Title Too Long

```bash
todo add "A" * 201
```

Output:
```
Error: Title must be 200 characters or less.
```

---

## Best Practices

### Task Naming
- Use clear, concise titles
- Keep titles action-oriented (e.g., "Review PR" not "PR review")
- Add descriptions for complex tasks

### Managing Large Lists
- Use `todo list --pending` to focus on active work
- Delete obsolete tasks regularly
- Break large tasks into smaller ones

### Session Management
- Remember: tasks persist only during the session
- Data is lost when the application closes
- For persistence, wait for Phase 2+

---

## Project Structure

```
todo_app/
├── src/
│   ├── models/
│   │   └── task.py          # Task dataclass
│   ├── services/
│   │   └── task_service.py  # Business logic
│   ├── cli/
│   │   ├── parser.py        # argparse setup
│   │   └── commands.py      # Command handlers
│   └── main.py              # Entry point
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── pyproject.toml
└── README.md
```

---

## Next Steps

After this quickstart:

1. **Run Tests**: `pytest tests/ -v`
2. **View Coverage**: `pytest --cov=src tests/`
3. **Explore Code**: Review `src/` directory structure
4. **Start Implementing**: Run `/sp.tasks` to generate task list

---

## Troubleshooting

### "todo: command not found"
Ensure the virtual environment is activated:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### "Python version not supported"
Install Python 3.13+ from [python.org](https://www.python.org/downloads/)

### Module not found errors
Reinstall dependencies:
```bash
pip install -e .
```
