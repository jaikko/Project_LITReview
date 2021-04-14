$(document).ready(function() {



    // Disable button
    $("#btn_registered").prop("disabled", true);

    // Get the modal
    var modal = $('#modal');

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Ckeck input form

    $('#register_form input').keyup(function() {
        var pass = $("#id_password").val();
        var repass = $('#id_rePassword').val();
        var username = $('#id_username').val();
        var red = "#A90F0F";
        var green = "#18560C";
        var count = 0;

        if (username.length >= 3) {
            $(".underline_user").css("border-bottom-color", green);


        } else {
            $(".underline_user").css("border-bottom-color", red);
            count += 1;
        }

        if (pass == repass & pass.length > 1) {
            $(".underline_pwd").css("border-bottom-color", green);
        } else {
            $(".underline_pwd").css("border-bottom-color", red);
            count += 1;
        }

        if (count == 0) {
            $("#btn_registered").prop("disabled", false)
        } else {
            $("#btn_registered").prop("disabled", true)
        }

    });

    //Timer for message
    if ($('.messages').css('display') == 'block') {
        $('.messages').fadeIn('slow', function() {
            $('.messages').delay(4000).fadeOut();
        });
    }



});
