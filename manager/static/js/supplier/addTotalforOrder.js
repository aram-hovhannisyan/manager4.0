function addTotalColumn(table) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');

    // Create a new header cell for the total column
    const totalHeader = document.createElement('th');
    totalHeader.textContent = 'Ընդ․';
    table.querySelector('thead tr').appendChild(totalHeader);
    totalHeader.title = 'Ընդհանուր'
    // Sum the cell values for each row and add the total to a new cell in each row
    for (let i = 0; i < rows.length; i++) {
      const cells = rows[i].querySelectorAll('td');
      let total = 0;
      for (let j = 1; j < cells.length; j++) {
        total += parseInt(cells[j].textContent, 10);
      }
      const totalCell = document.createElement('td');
      totalCell.textContent = total;
      totalCell.classList.add('totalcolumn-row');
      rows[i].appendChild(totalCell);
    }
  }

  const tables = document.querySelectorAll('table');
  tables.forEach(table => {
    addTotalColumn(table);
  });
