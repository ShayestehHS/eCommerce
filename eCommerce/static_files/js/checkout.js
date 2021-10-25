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

$(document).on('submit', 'form', function (event) {
    const form = $(this).closest('form');
    const bill_ship = form.data('type');
    if (!bill_ship) {
        return;
    }

    event.preventDefault();
    const modal = $('#modal_' + bill_ship);
    $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                const form_id = form.attr('id');
                if (form_id.includes('address_list')) {
                    address_list_success(data, modal);
                } else if (form_id.includes('address_use')) {
                    address_use_success(data, modal)
                }
                $(this).trigger('submit');
            }
        }
    )
});