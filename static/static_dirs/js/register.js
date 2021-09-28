function Timeout(fn, interval) {
    const id = setTimeout(fn, interval);
    this.cleared = false;
    this.clear = function () {
        this.cleared = true;
        clearTimeout(id);
    };
}

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
    var ajaxTimeOut = null;
    emailField.on('input', function () {
        const emailValue = emailField.val();
        // Check input is not null
        if (!emailValue === "") {
            emailField.css("box-shadow", "none");
            return null;
        }

        // Check input is valid email address
        if (!validateEmail(emailValue)) {
            emailField.css("box-shadow", "none");
            return null;
        }
        // Check time is out
        if (ajaxTimeOut != null) {
            if (!ajaxTimeOut.cleared) {
                return null
            }
        }

        ajaxTimeOut = new Timeout(function () {
            $.ajax({
                type: 'GET',
                url: emailField.closest('form').data('ajax-url'),
                data: {'email': emailValue,},
                success: function (data) {
                    if (data.email_exists === true) {
                        emailField.css('box-shadow', '0px 14px 12px -5px #44FF36');
                    } else if (data.email_exists === false) {
                        emailField.css('box-shadow', '0px 14px 12px -5px #ff3333');
                    }
                }
            });
            ajaxTimeOut.clear();
        }, 3000);
    })
})