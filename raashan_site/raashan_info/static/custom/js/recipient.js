// Add a function to activate the validity styling of all forms on submission
(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

// method to check the CNIC using an API call
$('#checkCNIC').click(function() {
    // first check if the form is valid
    var form = document.getElementsByClassName('recipient-form')[0];
    if (!form.checkValidity()) {
        form.classList.add('was-validated');    
    } else {
        // disable the button and add a spinner and loading status
        $('#checkCNIC').attr('disabled', true);
        $('#checkCNIC').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Checking...');

        // call the API using the CNIC value
        var cnic = $('#cnic').val()
        $.getJSON('/api/received?cnic=' + cnic, function(data) {
            // if result is returned format it and then populate the modal accordingly
            if (data.length > 0) {
                var received = data[0];
                
                var textvalue = ""
                if (received.recipient.name) {
                    textvalue += received.recipient.name + " with CNIC: ";
                }
                else {
                    textvalue += "Recipient with CNIC: ";
                }

                // format the CNIC with dashes
                textvalue += received.recipient.cnic.slice(0, 5) + "-" + received.recipient.cnic.slice(5, 12) + "-" + received.recipient.cnic.slice(12) + " ";

                textvalue += "last received raashan from ";

                if (received.worker.user.first_name) {
                    textvalue += received.worker.user.first_name + " " + received.worker.user.last_name + " ";
                }
                else {
                    textvalue += received.worker.user.username + " ";
                }

                textvalue += "of " + received.worker.organization.name + " ";

                var m = moment(received.date);
                textvalue += "on <b>" + m.format('dddd, MMMM Do YYYY, h:mm:ss a') + "</b>.";

                $('#recipientModalLabel').text('Recipient Found');
                $('#recipientModalContent').html(textvalue);
                $('#recipientModal').modal('show');

                $('#checkCNIC').attr('disabled', false);
                $('#checkCNIC').html('Check CNIC');
            }
            // else just populate the modal without a result
            else {
                $('#recipientModalLabel').text('Not Found');
                $('#recipientModalContent').text('Recipient with CNIC: ' + cnic + ' was not found.');
                $('#recipientModal').modal('show');

                $('#checkCNIC').attr('disabled', false);
                $('#checkCNIC').html('Check CNIC');
            }
        });
    }
});

