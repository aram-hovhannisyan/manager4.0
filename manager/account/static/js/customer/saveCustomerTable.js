// Function to find the closest ancestor element with a given selector
function closest(element, selector) {
  while (element && !element.matches(selector)) {
    element = element.parentElement;
  }
  return element;
}

// Function to get the value of a cookie by name
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return '';
}

// Function to save table data and send a request
function saveTableData() {
  // Get the parent table element
  const table = this.closest('table');

  // Get the table body and rows
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');

  // Create an array to hold the row data
  const rowData = [];

  // Variable to hold the total sum
  let totalSum = 0;

  // Iterate over each row
  rows.forEach(row => {
    // Get the values from the row cells
    const productName = row.querySelector('.productName').textContent.trim();
    const productCount = row.querySelector('.countInput').value.trim();
    const productPrice = row.querySelector('.productPrice').textContent.trim();
    const totalPrice = row.querySelector('.totalPrice').textContent.trim();

    // Create an object with the row data and push it to the array
    rowData.push({ productName, productCount, productPrice, totalPrice });

    // Calculate the total sum
    totalSum += parseInt(totalPrice);
  });

  // Create the data object to send in the request
  const data = {
    data: rowData,
    'total-sum': totalSum, // Round the total sum to 2 decimal places
    table_name: 'Table' + `${Math.random()}`.substring(2,10)
  };

  // Make a POST request to save the data
  fetch('save-table-data/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data),
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response here if needed
      console.log(data);
    })
    .catch(error => {
      // Handle the error here if needed
      console.error(error);
    });
}

// Add event listener to submit buttons
const submitButtons = document.querySelectorAll('[class^=saveTable]');
submitButtons.forEach(button => {
  button.addEventListener('click', saveTableData);
});