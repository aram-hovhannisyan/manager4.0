// Wait for the document to load
document.addEventListener('DOMContentLoaded', function() {
    // Get all the debt table cells
    var debtCells = document.querySelectorAll('tbody td:nth-child(2) a');

    // Variable to store the total debt
    var totalDebt = 0;

    // Iterate over each debt cell
    for (var i = 0; i < debtCells.length; i++) {
        // Get the value of the debt cell and parse it as a float
        var debt = parseFloat(debtCells[i].textContent);

        // Check if the parsed debt is a valid number
        if (!isNaN(debt)) {
        // Add the debt to the total
        totalDebt += debt;
        }
    }

    // Find the "TotalDebt" table cell and update its content with the total debt
    var totalDebtCell = document.getElementById('TotalDebt');
    totalDebtCell.textContent = totalDebt.toFixed(2); // Assuming 2 decimal places
    });