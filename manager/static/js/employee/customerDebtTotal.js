let totalSum = 0;
const rows = document.querySelectorAll('#debt');
rows.forEach((row) => {
    const value = parseFloat(row.textContent);
    if (!isNaN(value)) {
    totalSum += value;
    }
});
const totalRow = document.createElement('tr');
totalRow.innerHTML = `
    <td style="color: blue; font-size: 25px; border-top: 2px solid black;">Total</td>
    <td style="color: blue; font-size: 25px; border-top: 2px solid black;">${totalSum} dram</td>
`;
document.querySelector('#debtBody').append(totalRow);