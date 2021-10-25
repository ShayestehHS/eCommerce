$(document).on('submit', '.form_rmv_add', function (event) {
    event.preventDefault();
    const form = $(this).closest('form');

    $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                const form_button = form.find('.add_rmv');
                form_button.toggleClass("btn-success btn-danger");

                if (form.closest(".cart_table").length) {
                    // Form is located in cart_home page
                    update_table(form_button, data)
                } else if (data.added) {
                    form_button.val('Remove from cart')
                } else if (data.removed) {
                    form_button.val('Add to cart')
                }
                update_navbar(data.cart_items)
                // ToDo: Show message
                $(this).trigger('submit');
            }
        }
    )
});