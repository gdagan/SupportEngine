document.getElementById('ticketForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const category = document.getElementById('category').value;
    const priority = document.getElementById('priority').value;
    const description = document.getElementById('description').value;
    const attachment = document.getElementById('attachment').files[0];
  
    // Send ticket data to the backend for processing (AJAX request)
    const formData = new FormData();
    formData.append('category', category);
    formData.append('priority', priority);
    formData.append('description', description);
    formData.append('attachment', attachment);
  
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/create_ticket', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        alert('Ticket created successfully!');
        document.getElementById('ticketForm').reset();
      } else {
        alert('Failed to create ticket.');
      }
    };
    xhr.send(formData);
  });
  