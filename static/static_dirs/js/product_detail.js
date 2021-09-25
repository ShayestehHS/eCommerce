$(document).on('submit', 'form #form_rmv_add', function (event) {
                alert('AJAX')
    event.preventDefault();
    const form = $(this).closest('form');

    $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                const form_button = form.find('add_rmv');
                form_button.toggleClass("btn-success btn-danger");
                if (data.added) {
                    form_button.val('Remove from cart')
                } else if (data.removed) {
                    form_button.val('Add to cart')
                }
                $(this).trigger('submit');
            }
        }
    )
});