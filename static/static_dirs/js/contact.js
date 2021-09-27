$('#form-contact').on('submit',function (event){
    event.preventDefault();
    const form = $(this);

    $.ajax({
        url:form.attr('action'),
        type:form.attr('method'),
        data:form.serialize(),
        success:function (){
            alert('Your messages is sent') // ToDo: Show message
        }
    })
})