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

// avatar button
let inputs = document.querySelectorAll('.input-file');
Array.prototype.forEach.call(inputs, function (input) {

    let Inp = input.querySelector('.input-file__input')

    Inp.addEventListener('change', function (e) {
        input.classList.add('_active')
        input.querySelector('.input-file__text').innerText = 'Красавчик'
    });
});