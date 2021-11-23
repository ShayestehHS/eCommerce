$(document).on('submit', '.form_select_address', function (event) {
    event.preventDefault();
    const form = $(this).closest('form');


    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            $('#form_division').html(data);
            const select_address_action = form.attr('action');
            $("#address_form").attr('action', select_address_action);
        }
    });
});