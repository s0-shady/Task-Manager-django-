/**
 * TAS-2: Table sorting functionality using REST API
 */

function initTableSorting(tableId, apiUrl) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const headers = table.querySelectorAll('th.sortable');
    let currentSort = { field: null, order: 'asc' };
    
    headers.forEach(header => {
        header.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            
            // Toggle sort order if clicking the same column
            if (currentSort.field === sortField) {
                currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.field = sortField;
                currentSort.order = 'asc';
            }
            
            // Update sort icons
            updateSortIcons(table, sortField, currentSort.order);
            
            // Fetch sorted data from API
            fetchSortedData(table, apiUrl, sortField, currentSort.order);
        });
    });
}

function updateSortIcons(table, activeField, order) {
    const headers = table.querySelectorAll('th.sortable');
    
    headers.forEach(header => {
        const icon = header.querySelector('.sort-icon');
        if (header.dataset.sort === activeField) {
            icon.textContent = order === 'asc' ? '▲' : '▼';
        } else {
            icon.textContent = '';
        }
    });
}

async function fetchSortedData(table, apiUrl, sortBy, sortOrder) {
    const tbody = table.querySelector('tbody');
    tbody.classList.add('loading');
    
    try {
        const url = `${apiUrl}?sort_by=${sortBy}&sort_order=${sortOrder}`;
        const response = await fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Determine if this is completed or uncompleted table
        const isCompleted = table.id === 'completed-tasks-table';
        
        // Update table with new data
        updateTableBody(tbody, data.tasks, isCompleted);
        
    } catch (error) {
        console.error('Error fetching sorted data:', error);
    } finally {
        tbody.classList.remove('loading');
    }
}

function updateTableBody(tbody, tasks, isCompleted) {
    if (tasks.length === 0) {
        const emptyText = isCompleted ? 'No completed tasks.' : 'No uncompleted tasks.';
        tbody.innerHTML = `<tr><td colspan="6">${emptyText}</td></tr>`;
        return;
    }
    
    tbody.innerHTML = tasks.map(task => {
        const completionDate = task.completion_date ? task.completion_date : '-';
        
        // Build action buttons based on completion status
        let actionButtons = `
            <a href="/task/${task.id}/" class="btn btn-small btn-secondary">Details</a>
            <a href="/task/${task.id}/edit/" class="btn btn-small">Edit</a>
            <a href="/task/${task.id}/delete/" class="btn btn-small btn-danger">Delete</a>
        `;
        
        if (isCompleted) {
            actionButtons += `<a href="/task/${task.id}/restore/" class="btn btn-small btn-warning">Restore</a>`;
        } else {
            actionButtons += `<a href="/task/${task.id}/complete/" class="btn btn-small btn-success">Complete</a>`;
        }
        
        return `
            <tr data-task-id="${task.id}">
                <td>${task.id}</td>
                <td>${escapeHtml(task.title)}</td>
                <td>${task.date_added}</td>
                <td>${escapeHtml(task.priority.name)}</td>
                <td>${completionDate}</td>
                <td>${actionButtons}</td>
            </tr>
        `;
    }).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
