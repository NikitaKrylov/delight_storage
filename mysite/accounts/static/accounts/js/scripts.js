// var backgrounds = [
//     "url(/static/accounts/images/backgrounds/bg1.jpg) 50% no-repeat",
//     "url(/static/accounts/images/backgrounds/bg2.jpg) 50% no-repeat",
//     "url(/static/accounts/images/backgrounds/bg3.webp) 50% no-repeat",
//     "url(/static/accounts/images/backgrounds/bg4.jpg) 50% no-repeat",
//     "url(/static/accounts/images/backgrounds/bg5.jpg) 50% no-repeat",
//     "url(/static/accounts/images/backgrounds/bg7.jpg) 50% no-repeat",
//     "url(/static/accounts/images/backgrounds/bg9.jpg) 50% no-repeat",
// ];
// var regContainer = document.querySelector('.reg-container')
// regContainer.style.background = backgrounds[Math.floor(Math.random() * (backgrounds.length))];
// regContainer.style.backgroundSize = 'cover'


// анимация инпута
const
    placeholders = document.querySelectorAll('.reg-menu__placeholder-text'),
    inputs = document.querySelectorAll('.reg-menu__input');

placeholders.forEach(function (el, i) {
    let value = el.innerText,
        html = '';

    console.log(value)
    for (let w of value) {
        // if (!value) {
        //     value = '&nbsp;';
        // }

        if (w == ' ') {
            w = '&nbsp;'
        }

        html += `<span class="letter">${w}</span>`;
    }
    el.innerHTML = html;
});

inputs.forEach(function (el) {
    let parent = el.parentNode;
    el.addEventListener('focus', function () {
        parent.classList.add('filled');
        placeholderAnimationIn(parent, true);
    }, false);
    el.addEventListener('blur', function () {
        if (el.value.length) return;
        parent.classList.remove('filled');
        placeholderAnimationIn(parent, false);
    }, false);
});

function placeholderAnimationIn(parent, action) {
    let act = (action) ? 'add' : 'remove';
    let letters = parent.querySelectorAll('.letter');
    letters = [].slice.call(letters, 0);
    if (!action) letters = letters.reverse();
    letters.forEach(function (el, i) {
        setTimeout(function () {
            let contains = parent.classList.contains('filled');
            if ((action && !contains) || (!action && contains)) return;
            el.classList[act]('_active');
        }, (50 * i));
    });
}

// document.body.classList.add('document-loaded');

function funonload() {
    document.body.classList.add('document-loaded');
} 
window.onload = funonload;
