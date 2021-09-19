$(document).ready(function () {
    const toasts = $(".toast");
    let toast, tag;
    for (let i = 0; i < toasts.length; i++) {
        toast = $(toasts[i]);
        tag = toast.attr("data-tags");

        if (tag === 'success') {
            toast.children('.toast-body').css('background-color', 'green');
        } else if (tag === 'error') {
            toast.children('.toast-body').css('background-color', 'red');
        }
    }

    toasts.toast('show');
});