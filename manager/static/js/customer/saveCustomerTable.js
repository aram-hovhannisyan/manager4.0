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
  const date = table.querySelector('#inputDate').value
  // Create an array to hold the row data
  const rowData = [];

  // Variable to hold the total sum
  let totalSum = 0;
  let mySet = new Set();

  // Iterate over each row
  rows.forEach(row => {
    // Get the values from the row cells
    const productName = row.querySelector('.productName').textContent.trim();
    const productCount = row.querySelector('.countInput').value.trim();
    const productPrice = row.querySelector('.productPrice').textContent.trim();
    const totalPrice = row.querySelector('.totalPrice').textContent.trim();
    const sup = row.getAttribute("name")
    
    mySet.add(sup)
    // console.log(mySet);
    // Create an object with the row data and push it to the array
    rowData.push({ 
      productName,
      productCount,
      productPrice, 
      totalPrice,
      supplier: sup,
    });

    // Calculate the total sum
    totalSum += parseInt(totalPrice);
  });
  let data = {}
  if (mySet.size !== 1){
    data = {
      data: rowData,
      'total-sum': totalSum, // Round the total sum to 2 decimal places
      table_name: ['Table' + `${Math.random()}`.substring(2,10), 'Table' + `${Math.random()}`.substring(2,10)],
      'date': date
    };
  } else{
    data = {
      data: rowData,
      'total-sum': totalSum, // Round the total sum to 2 decimal places
      table_name: ['Table' + `${Math.random()}`.substring(2,10)],
      date
  
    };
  }
  // Create the data object to send in the request


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