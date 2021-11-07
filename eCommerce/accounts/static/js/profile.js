$(document).on('click', '#btn_user_detail', function (e) {
    const modal = $('#modal_user_detail');

    $.ajax({
            type: 'GET',
            url: $(this).data('url_update_detail'),
            success: function (data) {
                console.log(data)
                modal.find('.modal-body').html(data);
                modal.modal('show');
            }
        }
    )
})

$(document).on('submit', '#form_user_detail', function (event) {
    const form = $(this).closest('form');

    event.preventDefault();
    const modal = $('#modal_user_detail');
    $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                console.log('Success')
            }
        }
    )
    modal.modal('close');
});