function update_table(form_button, data) {
    if ($('.price').length === 1){
        $('#cart_home').html('<h3>Your cart is empty</h3>');
        return null
    }
    const table = form_button.closest("table");
    const subtotal = table.find('.subtotal');
    const total = table.find('.total');

    total.html("$"+format(data.total))
    subtotal.html("$"+format(data.total))
    form_button.closest("tr").remove();
    const abc = table.find('.row-number');
    abc.each(function(index,item){
        $(this).text(index+1);
    });
}

$(document).on('submit', '.form_rmv_add', function (event) {
    event.preventDefault();
    const form = $(this).closest('form');

    $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                const form_button = form.find('.add_rmv');
                form_button.toggleClass("btn-success btn-danger");

                update_table(form_button, data)
                update_navbar(data.cart_items)
                // ToDo: Show message
                $(this).trigger('submit');
            }
        }
    )
});