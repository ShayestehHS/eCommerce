function format(number, decimal_place = 2) {
    return Number(number).toFixed(decimal_place)
}

// If js is disabled => Do not show the main-div(body)
$(function () {
    $("#main-div").attr('hidden', false);
});

// Change cursor on AJAX call
$(document).ajaxStart(function () {
    $('body').css({'cursor': 'wait'})
});
$(document).ajaxComplete(function () {
    $('body').css({'cursor': 'default'})
});
