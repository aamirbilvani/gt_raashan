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

                if (received.worker.organization) {
                    textvalue += "of " + received.worker.organization.name + " ";
                }

                // format the date
                var m = moment(received.date);
                textvalue += "on <b>" + m.format('dddd, MMMM Do YYYY, h:mm:ss a') + "</b>.";

                // set modal content and then show it
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

// The window for the QR Code Scanner
var qrCodeScanner = new Html5Qrcode('qrScanner');

// If QR code is found
const qrCodeSuccessCallback = qrCodeMessage => {
    // If QR code is in the expected format (either 25 or 26 digits), then send it to the main screen
    if ((qrCodeMessage.length == 25 || qrCodeMessage.length == 26) && qrCodeMessage.match('^[0-9]*$')) {
        var cnicNumber = qrCodeMessage.slice(12,25);
        $('#cnic').val(cnicNumber);
        $('#scannerFeedback').text('CNIC found: ' + cnicNumber);
        setTimeout(function() {
            $('#scannerModal').modal('hide');
        }, 1000); 
    }
    // If QR code is not in correct format, show message
    else {   
        $('#scannerFeedback').text('Found: ' + qrCodeMessage + '. Code not read correctly or not a valid CNIC. Please try again.');
        setTimeout(function() {
            $('#scannerFeedback').fadeOut(function() {
                $('#scannerFeedback').text('Scanning...').fadeIn();
            });
        }, 1000);
    }
}

// If QR code not found, this is happening constantly
const qrCodeErrorCallback = message => {    
}

// If video stream becomes unstable for some reason
const videoErrorCallback = message => {
    $('#scannerFeedback').text('Video Error, error = ${message}');
}

// Start the QR Scanner using the given camera
function qrCodeScannerStart(cameraId) {
    qrCodeScanner.start(
        cameraId, 
        {fps: 10},
        qrCodeSuccessCallback,
        qrCodeErrorCallback)
        .catch(videoErrorCallback);
    $('#scannerFeedback').text('Scanning...');
}

// Show the scanner modal
$('#scannerModalShowButton').on('click', function() {
    // start the selected camera, then show the modal
    var cameraId = $('#selectCamera').val();
    qrCodeScannerStart(cameraId);
    $('#scannerModal').modal('show');
})

// on modal hide, stop the camera and destroy the dropdown entries to ensure cleanup.
$('#scannerModal').on('hide.bs.modal', function(e) {
    if (qrCodeScanner) {
        qrCodeScanner.stop().then(ignore => {
        });
    }
});

$(document).ready(function() {
    // First get the list of cameras
    Html5Qrcode.getCameras().then(cameras => {
        // If cameras are found, populate the dropdown
        if (cameras && cameras.length) {
            for (var i = 0; i < cameras.length; i++) {
                var camera = cameras[i];
                var value = camera.id;
                var name = camera.label == null ? value : camera.label;
                if (i == 0) {
                    $("#selectCamera").append(`<option value="${value}" selected>${name}</option>`);
                }
                else {
                    $("#selectCamera").append(`<option value="${value}">${name}</option>`);
                }
            }

            // set the on change event of the dropdown to stop the current camera and start the next camera
            $('#selectCamera').on('change', function() {
                qrCodeScanner.stop().then(ignore => {
                    var cameraId = $('#selectCamera').val();
                    qrCodeScannerStart(cameraId);
                })
            });

            // show the button that pops open the modal
            $('.scanner-modal-button-row').show();
        } else {
            $('#scannerFeedback').text('No cameras found on this device.');
        }
    })
});
