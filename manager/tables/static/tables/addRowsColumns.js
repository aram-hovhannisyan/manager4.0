// Function to add total row at the end of each table
function addTotalRow(table) {
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');

  // Get the number of columns to sum
  const numColumns = rows[0].querySelectorAll('td').length - 1;

  // Create a new row
  const totalRow = document.createElement('tr');
  totalRow.classList.add('total-row');

  // Add the "Total" label to the first column
  const totalLabel = document.createElement('td');
  totalLabel.textContent = 'Ընդհանուր';
  totalRow.appendChild(totalLabel);

  // Sum the values in each column and add them to the row
  for (let i = 0; i < numColumns; i++) {
    let sum = 0;
    for (let j = 0; j < rows.length; j++) {
      const cell = rows[j].querySelectorAll('td')[i+1];
      if (cell.textContent.trim() === '') {
        cell.textContent = '0';
      }
      sum += Number(cell.textContent);
    }
    const totalCell = document.createElement('td');
    totalCell.textContent = sum;
    totalCell.classList.add('total-cell')
    totalRow.appendChild(totalCell);
  }

  // Add the row to the table
  tbody.appendChild(totalRow);
}

// Function to add total column to each table
function addTotalColumn(table) {
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');

  // Create a new header cell for the total column
  const totalHeader = document.querySelector('.total-column');

  // Sum the product counts for each row and add the total to a new cell in each row
  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll('td');
    const sumCells = rows[i].querySelectorAll('td');
    let total = 0;
    let totalSum = 0;
    for (let j = 1; j < cells.length; j += 2) {
      total += parseInt(cells[j].textContent, 10);
      totalSum += parseInt(sumCells[j+1].textContent, 10);
    }
    const totalCell = document.createElement('td');
    const totalSumCell = document.createElement('td');

    totalCell.classList.add('totalcolumn-row');
    totalSumCell.classList.add('totalcolumn-row');

    if (!totalSum) {
      totalSumCell.textContent = '0';
    } else {
      totalSumCell.textContent = totalSum;
    }
    if (!total) {
      totalCell.textContent = '0';
    } else {
      totalCell.textContent = total;
    }
    rows[i].appendChild(totalCell);
    rows[i].appendChild(totalSumCell);
  }
}

// Add total row and total column to each table
const tables = document.querySelectorAll('.big-table');
tables.forEach(table => {
  addTotalRow(table);
  addTotalColumn(table);
});
