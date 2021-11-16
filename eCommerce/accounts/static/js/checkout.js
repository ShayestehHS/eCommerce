function address_list_success(data, modal) {
    modal.find('.modal-body').html(data);
    modal.modal('show');
}

function address_use_success(data, modal) {
    modal.modal('hide');
    if (data.status === 1) {
        window.location.href = $("#finalization_url").val();
    }
}

// Every form on submit
$(document).on('submit', 'form', function (event) {
    const form = $(this).closest('form');

    event.preventDefault();
    const modal = $('#modal_list');
    alert(modal)
    console.log(modal);
    $.ajax({
            type: form.attr('method'),
            url: form.attr('action_url'),
            data: form.serialize(),
            success: function (data) {
                const form_id = form.attr('id');
                if (form_id === 'list_address') {
                    address_list_success(data, modal);
                } else if (form_id === 'use_address') {
                    address_use_success(data, modal)
                }
                $(this).trigger('submit');
            }
        }
    )
});