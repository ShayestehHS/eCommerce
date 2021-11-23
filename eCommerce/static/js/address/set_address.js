$(document).on('submit', '#list_address', function (event) {
    const form = $(this).closest('form');

    event.preventDefault();
    const modal = $('#modal_list');
    $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                modal.find('.modal-body').html(data);
                modal.modal('show');
                $(this).trigger('submit');
            }
        }
    )
});asdfasfda