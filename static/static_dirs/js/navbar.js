function update_navbar(cart_items) {
    const navbar_cart = $(".cart_items");

    if (cart_items) {
        navbar_cart.attr("hidden", false);
        navbar_cart.html(cart_items);
    } else {
        navbar_cart.attr("hidden", true);
    }
}

$("#form-search").autocomplete({
    minLength: 2,
    source: function (request, response) {
        const form = $('#form-search');
        const search_btn = form.find("#srch-btn");
        $.ajax({
            url: form.data('ajax-url'),
            type: 'GET',
            data: form.serialize(),
            beforeSend: function () {
                search_btn.html('Searching...');
            },
            success: function (data) {
                console.log(data)
                console.log(data.name)
                response(data);
            },
            complete: function () {
                setTimeout(function(){ search_btn.html('Search'); }, 1000);
            },
        });
    },
    select: function (event, ui) {
        $('#form-search').submit(); // add the value of selected to input
    }
});