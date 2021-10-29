$('#form-contact').on('submit', function (event) {
    event.preventDefault();
    const form = $(this);
    const submit_btn = form.find('#form-submit');

    $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: form.serialize(),
        beforeSend: function () {
            submit_btn.val('Sending...');
        },
        success: function (data) {
            console.log('Your messages is sent') // ToDo: Show message
        },
        complete: function () {
            setTimeout(function () {
                submit_btn.val('Send another');
            }, 1000);
        },
    })
})