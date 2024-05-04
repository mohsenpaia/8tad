/* Webarch Admin Dashboard 
 /* This JS is only for DEMO Purposes - Extract the code that you need
 -----------------------------------------------------------------*/
$(document).ready(function () {
        //Iconic form validation sample
    $('#admin-campaign-edit-form > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            name: {
                minlength: 2,
                required: true
            },
            landing_page_url: {
                required: true,
                url: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });

    //Iconic form validation sample
    $('#publisher-website-form > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            title: {
                minlength: 2,
                required: true
            },
            url: {
                required: true,
                url: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });



    $('#publisher-blocked-website > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            url: {
                required: true,
                url: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });


    $('#advertiser-blocked-website > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            url: {
                required: true,
                url: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });

    $('#advertiser-campaign-step-two > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            name: {
                minlength: 2,
                required: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });


        $('#advertiser-campaign-step-four > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            title: {
                minlength: 2,
                required: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });

    $('#advertiser-campaign-step-five > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            landing_page_url: {
                required: true,
                url: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });

    $('#banner-size-form > form').validate({
        errorElement: 'span',
        errorClass: 'error',
        focusInvalid: false,
        ignore: "",
        rules: {
            width: {
                number: true,
                maxlength: 4,
                required: true
            },
            height: {
                number: true,
                maxlength: 4,
                required: true
            }
        },

        invalidHandler: function (event, validator) {
            //display error alert on form submit
        },

        errorPlacement: function (error, element) { // render error placement for each input type
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass('fa fa-check').addClass('fa fa-exclamation');
            parent.removeClass('success-control').addClass('error-control');
        },

        highlight: function (element) { // hightlight error inputs
            var parent = $(element).parent();
            parent.removeClass('success-control').addClass('error-control');
        },

        unhighlight: function (element) { // revert the change done by hightlight

        },

        success: function (label, element) {
            var icon = $(element).parent('.input-with-icon').children('i');
            var parent = $(element).parent('.input-with-icon');
            icon.removeClass("fa fa-exclamation").addClass('fa fa-check');
            parent.removeClass('error-control').addClass('success-control');
        },

        submitHandler: function (form) {
            form.submit();
        }
    });

});	
