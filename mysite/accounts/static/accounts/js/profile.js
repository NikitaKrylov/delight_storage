// $('#user_profile_form').on('submit', function (event) {
//     event.preventDefault();

//     $.ajax({
//         url: $(this).attr('action'),
//         type: $(this).attr('method'),
//         data: {
//             username: $('#id_username').val(),
//             email: $('#id_email').val(),
//             avatar: $('#id_avatar').val(),
//             birth_date: $('#id_birth_date').val(),
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//         },

//         success: function (json) {
//         },
//     });

// });

// инициализации календаря
if (body.classList.contains("_pc")) {
	$("#id_birth_date").attr("type", "text");
	new AirDatepicker("#id_birth_date");
}
