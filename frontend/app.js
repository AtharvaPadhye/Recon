const API_BASE = 'http://localhost:8000/v1';
let editingId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadCases();
    document.getElementById('case-form').addEventListener('submit', submitCase);
});

function loadCases() {
    fetch(`${API_BASE}/cases`)
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => {
                    throw new Error(err.detail || 'Failed to load cases');
                });
            }
            return res.json();
        })
        .then(data => {
            const tbody = document.querySelector('#cases-table tbody');
            tbody.innerHTML = '';
            data.forEach(c => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${c.id}</td>
                    <td>${c.title}</td>
                    <td>${c.location.lat}</td>
                    <td>${c.location.lon}</td>
                    <td>${c.initial_event_id}</td>
                    <td>
                        <button onclick="startEdit('${c.id}')">Edit</button>
                        <button onclick="deleteCase('${c.id}')">Delete</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(err => alert(err));
}

function submitCase(e) {
    e.preventDefault();
    const body = {
        title: document.getElementById('title').value,
        location: {
            lat: parseFloat(document.getElementById('lat').value),
            lon: parseFloat(document.getElementById('lon').value)
        },
        initial_event_id: document.getElementById('initial_event_id').value
    };

    const url = editingId ? `${API_BASE}/cases/${editingId}` : `${API_BASE}/cases`;
    const method = editingId ? 'PUT' : 'POST';

    fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw new Error(err.detail); });
        }
        return res.json();
    })
    .then(() => {
        document.getElementById('case-form').reset();
        editingId = null;
        loadCases();
    })
    .catch(err => alert(err));
}

function startEdit(id) {
    fetch(`${API_BASE}/cases/${id}`)
        .then(res => res.json())
        .then(c => {
            document.getElementById('title').value = c.title;
            document.getElementById('lat').value = c.location.lat;
            document.getElementById('lon').value = c.location.lon;
            document.getElementById('initial_event_id').value = c.initial_event_id;
            editingId = id;
        });
}

function deleteCase(id) {
    fetch(`${API_BASE}/cases/${id}`, { method: 'DELETE' })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => {
                    throw new Error(err.detail || 'Failed to delete case');
                });
            }
        })
        .then(() => loadCases())
        .catch(err => alert(err));
}
