function sendOrder(sup_Id, sup_username) {
  // Create a new XMLHttpRequest object
  let xhr = new XMLHttpRequest();

  // Set up the request
  xhr.open('POST', 'sendorder/');
  xhr.setRequestHeader('Content-Type', 'application/json');

  // Get the CSRF token from the cookie
  let csrftoken = getCookie('csrftoken');

  // Set the CSRF token in the request headers
  xhr.setRequestHeader('X-CSRFToken', csrftoken);

  let data = {
    supplier_id: sup_Id,
    nameOftable: 'Table' + `${Math.random()}`.substring(2,10),
    sup_name: sup_username
  };

  // Convert the data to JSON format
  let jsonData = JSON.stringify(data);

  // Set up the event handler for successful response
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Handle the success response from the server
      console.log('Order sent successfully');
      // Perform any desired actions after a successful request
      window.location.reload()
    }
  };

  // Set up the event handler for errors
  xhr.onerror = function() {
    // Handle any errors that occur during the request
    console.error('Error sending order');
  };

  // Send the request
  xhr.send(jsonData);
  
}

// Helper function to get the CSRF token from the cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Check if the cookie name matches the CSRF cookie name
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
