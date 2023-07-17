const inputDates = document.querySelectorAll('#inputDate');
// console.log(inputDate.getAttribute('class'));
const today = new Date();
const formattedDate = today.toISOString().split('T')[0];
inputDates.forEach(input => {
    input.value = formattedDate
})
