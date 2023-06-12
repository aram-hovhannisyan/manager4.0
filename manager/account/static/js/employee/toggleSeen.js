// function toggleSeen(debtId) {
//     // Send an AJAX request to the server to toggle the 'seen' field
//     fetch(`/toggle-seen/${debtId}/`)
//       .then(response => response.json())
//       .then(data => {
//         // Handle the response here if needed
//         console.log(data);
  
//         // Update the cell content based on the new 'seen' value
//         const cell = document.getElementById(`changePaymant${debtId}`);
//         cell.textContent = data.seen ? data.debt : data.debt;
//         cell.style.color = data.seen ? 'green' : 'red';
//       })
//       .catch(error => {
//         // Handle the error here if needed
//         console.error(error);
//       });
//   }

function toggleSeen(debtId) {
    // Send an AJAX request to the server to toggle the 'seen' field
    fetch(`/toggle-seen/${debtId}/`)
      .then(response => response.json())
      .then(data => {
        // Handle the response here if needed
        console.log(data);
  
        // Update the cell content based on the new 'seen' value
        const cell = document.getElementById(`changePaymant${debtId}`);
        cell.textContent = data.seen ? `${data.debt} ✓` : `${data.debt}  ✕`;
        cell.style.color = data.seen ? 'green' : 'red';
  
        // Update the last cell of the last row
        const lastRow = document.querySelector('#debtTable tbody tr:last-child');
        const lastCell = lastRow.lastElementChild;
        lastCell.textContent = `${data.payed}(${data.total})`;
      })
      .catch(error => {
        // Handle the error here if needed
        console.error(error);
      });
  }