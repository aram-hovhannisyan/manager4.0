// Calculate the sum of total price column and update the footer cell
function calculateTotalSum(table) {
  const rows = table.querySelectorAll('tbody tr');
  let totalSum = 0;

  rows.forEach(row => {
    const totalPriceCell = row.querySelector('.totalPrice');
    const totalPrice = parseFloat(totalPriceCell.textContent);

    if (!isNaN(totalPrice)) {
      totalSum += totalPrice;
    }
  });

  const totalSumCell = table.querySelector('tfoot td#total-sum');
  totalSumCell.textContent = totalSum;
}

// Loop through each table
tables = document.querySelectorAll('.responsive-table');
tables.forEach(table => {
  calculateTotalSum(table);

  const inputs = table.querySelectorAll('input[type="number"]');
  inputs.forEach(input => {
    input.addEventListener('change', () => {
      const row = input.parentNode.parentNode;
      const inputValue = parseInt(input.value);
      const constantCell = row.cells[2];
      const constantValue = parseInt(constantCell.textContent);
      let result = inputValue * constantValue;
      const resultCell = row.cells[3];

      if (!result) {
        result = 0;
      }

      resultCell.textContent = result;
      calculateTotalSum(table);
    });
  });
});
function sumLastColumn(table) {
  const rows = table.querySelectorAll('tbody tr');
  let sum = 0;

  rows.forEach((row) => {
    const lastCell = row.querySelector('.totalPrice');
    const totalPrice = parseFloat(lastCell.textContent);
    if (!isNaN(totalPrice)) {
      sum += totalPrice;
    }
  });

  return sum;
}