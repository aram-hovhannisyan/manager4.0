const inputDates = document.querySelectorAll('#inputDate');
const today = new Date();
const formattedDate = today.toISOString().split('T')[0];
inputDates.forEach(input => {
    input.value = formattedDate
})