const exportButtons = document.querySelectorAll('[class^="export-Button"]');

exportButtons.forEach((button) => {
  const supplierId = button.className.match(/export-Button(\d+)/)[1];
  button.addEventListener('click', (event) => {
    const table = document.getElementById(supplierId);
    const today = new Date().toISOString().split('T')[0];
    const fileName = prompt("Enter the file name", `table_${today}.xlsx`);
    if (fileName) {
      exportToExcel(table, fileName);
      window.location.reload();
    }
  });
});

// Function to export table content to Excel and trigger download
function exportToExcel(table, fileName) {
  const hiddenColumns = Array.from(table.querySelectorAll('th[colspan="2"]'));
  const rows = table.querySelectorAll('tbody tr');
  const delChilds = [];
  rows.forEach(row => {
    let cols = row.querySelectorAll('td');
    cols.forEach((col, index) => {
      if (index % 2 === 0 && index !== 0) {
        delChilds.push({ col, row });
      }
    });
  });

  delChilds.forEach(value => {
    let delCol = value.col;
    if (delCol.style.display === 'none') {
      let delRow = value.row;
      delRow.removeChild(delCol);
    }
  });

  const wb = XLSX.utils.table_to_book(table);
  const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  const blob = new Blob([wbout], { type: "application/octet-stream" });

  // Check if the browser supports the download attribute
  if (typeof navigator.msSaveBlob !== "undefined") {
    // For IE and Edge browsers
    navigator.msSaveBlob(blob, fileName);
  } else {
    // For other browsers
    const link = document.createElement("a");
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", fileName);
      link.style.visibility = "hidden";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  }
}