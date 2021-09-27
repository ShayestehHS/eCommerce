function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

// Check that passwords are matched or not
const password = $('#id_password1');
const conPassword = $('#id_password2');
conPassword.on('input', function () {
    if (password.val() !== conPassword.val()) {
        password.css('box-shadow', '0px 14px 12px -5px #ff3333');
        conPassword.css('box-shadow', '0px 14px 12px -5px #ff3333');
    } else {
        password.css('box-shadow', '0px 14px 12px -5px #44FF36');
        conPassword.css('box-shadow', '0px 14px 12px -5px #44FF36');
    }
})


$(document).ready(function () {
    const emailField = $('#id_email');
    emailField.on('input', function () {
        // Check input is null or not
        if (!$(this).val() === "") {
            emailField.css("box-shadow", "none");
            return null;
        }

        // Check input is valid email address or not
        if (!validateEmail($(this).val())) {
            emailField.css("box-shadow", "none");
            return null;
        }
        alert(emailField.val())
        // Send AJAX
        $.ajax({
            type: 'GET',
            url: $(this).closest('form').data('ajax-url'),
            data: {'email': emailField.val(),},
            success: function (data) {
                alert(data.email_exists)
                if (data.email_exists === true) {
                    emailField.css('box-shadow', '0px 14px 12px -5px #44FF36');
                } else if (data.email_exists === false) {
                    emailField.css('box-shadow', '0px 14px 12px -5px #ff3333');
                }
            }
        })
    })
})