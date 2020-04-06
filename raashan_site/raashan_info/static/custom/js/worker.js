//function to initialize select2
function initializeSelect2(selectElementObj) {
    selectElementObj.select2({
        placeholder: 'Select your Organization',
        tags: true,
    });
}

$(document).ready(function() {
    //onload: initialize select2
    $(".organization-select").each(function() {
        initializeSelect2($(this));
    });
});
