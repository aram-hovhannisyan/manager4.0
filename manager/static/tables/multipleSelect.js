var formSubmitted = false;
    
    document.getElementById('addProductForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission
    
        if (formSubmitted) {
            return; // Do nothing if the form has already been submitted
        }
    
        // Get form inputs
        var productName = document.getElementsByName('productName')[0].value;
        var productPrice = document.getElementsByName('productPrice')[0].value;
        var customerOptions = [...document.getElementsByName('customer')[0].options];
        var selectedCustomers = customerOptions.filter(option => option.selected).map(option => option.value);
        var supplier = document.getElementsByName('supplier')[0].value;
    
        // Create data object
        var data = {
            productName: productName,
            productPrice: productPrice,
            customers: selectedCustomers,
            supplier: supplier
        };
    
        // Convert data to JSON
        var jsonData = JSON.stringify(data);
    
        // Get CSRF token from the form
        var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    
        // Send JSON data to the admin view
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/adminpage/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Redirect or handle the response as needed
                window.location.href = '/adminpage/';
            }
        };
    
        // Send the request
        xhr.send(jsonData);
    
        // Set the flag to indicate that the form has been submitted
        formSubmitted = true;
    });