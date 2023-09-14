

/// Add event listener to delete buttons
document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('task');
    taskInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            addTask();
        }
    });

    // Add event listener for delete buttons
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-id');
            deleteTask(taskId);
        });
    });
});

function deleteTask(taskId) {
    $.ajax({
        url: '/delete_task',
        type: 'POST',
        data: { id: taskId },
        success: function(data) {
            // Reload the page to reflect the changes
            location.reload();
        },
        error: function(error) {
            console.error('Error deleting task:', error); // Log any errors
        }
    });
}



// Existing code for adding tasks
function addTask() {
    const taskInput = document.getElementById('task');
    const dueDateInput = document.getElementById('due-date');
    const taskText = taskInput.value.trim();
    const dueDate = dueDateInput.value;

    if (taskText !== '') {
        taskInput.value = '';

        $.ajax({
            url: '/add_task',
            type: 'POST',
            data: { task: taskText, due_date: dueDate },
            success: function(data) {
                const taskList = document.getElementById('task-list');
                taskList.innerHTML = '';

                data.tasks.forEach(task => {
                    const li = document.createElement('li');
                    li.textContent = task.task;
                    const dateSpan = document.createElement('span');
                    dateSpan.textContent = task.created_date;
                    dateSpan.classList.add('date');
                    li.appendChild(dateSpan);
                    taskList.appendChild(li);
                });
            }
        });
    }
}
