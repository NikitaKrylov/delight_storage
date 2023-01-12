// slider gallery
// $(document).ready(function () {
//     let slider = document.querySelector('.slider');
//     if (slider) {
//         $('.slider').slick({
//             dots: true,
//             infinite: true,
//             speed: 100,
//             slidesToShow: 1,
//             cssEase: 'ease',
//             adaptiveHeight: false,
//             draggable: false,
//             touchMove: false,
//             waitForAnimate: false,
//             variableWidth: false,
//             touchThreshold: 7,
//             // appendArrows: $('.arrow-btn'),
//         });
//     };
// })

const body = document.body


if (body.classList.contains('_touch')) {

    // profile-menu
    // $(".header-profile-avatar").on('click', function (e) {
    //     rlMenu('#profile-menu-mobile', '.close-ham-menu-2');
    // });

} else {

    // меню профиля
    $('.header__profile').on('click', function () {
        $(this).toggleClass('_active');
    });

    // $(document).on('click', function (e) {
    //     if (!e.target.closest('.profile-dropdown') && !e.target.closest('.header__profile')) {
    //         $('.header__profile._active').removeClass('_active');
    //     }
    // });
}

function rlMenu(rlmenu, close) {
    // const button = document.querySelector(btn)
    const menu = document.querySelector(rlmenu)
    const closeHamMenu = document.querySelector(close)

    // if (button) {
    //     button.addEventListener("click", function (e) {
    //         menu.classList.toggle('_active');
    //         document.body.classList.toggle('_lock')
    //     });
    // };

    menu.classList.toggle('_active');
    body.classList.toggle('_lock')

    $(document).on('mouseup', function (e) {
        e.preventDefault();

        let s = $(menu)
        if (menu.classList.contains('_active') === true) {
            if (!s.is(e.target) && s.has(e.target).length === 0) {
                s.removeClass('_active');
                body.classList.remove('_lock')
            } else {
                if (closeHamMenu) {
                    closeHamMenu.addEventListener("click", function (e) {
                        e.preventDefault();
                        menu.classList.remove('_active');
                        body.classList.remove('_lock')
                    });
                }
            }
        }
    });
}

// mav-menu
$(".header__mobile-navigation").on('click', function (e) {
    rlMenu('#nav-menu-mobile', '.close-ham-menu')
});

// view-hide-header
let lastScroll = 0;
const defaultOffset = 200;
const header = document.querySelector('.header');
const scrollPosition = () => window.pageYOffset || document.documentElement.scrollTop;
const containHide = () => header.classList.contains('_hide-header');
window.addEventListener('scroll', () => {
    if (scrollPosition() > lastScroll && !containHide() && scrollPosition() > defaultOffset) {
        // scroll down
        header.classList.add('_hide-header');
    } else if (scrollPosition() < lastScroll && containHide()) {
        // scroll up
        header.classList.remove('_hide-header');
    }

    lastScroll = scrollPosition();
});

// показать/скрыть popup(всплывающее окно)
function popupOpen(curentPopup) {
    body.classList.add('_lock')
    curentPopup.classList.add('_active')
    
    curentPopup.addEventListener('click', function (e) {
        if (!e.target.closest('.popup__content')) {
            popupClose(e.target.closest('.popup'))
        }
    });
}

function popupClose(curentPopup) {
    curentPopup.classList.remove('_active')
    body.classList.remove('_lock')

    document.querySelectorAll('.radio__input').forEach(function (e) {
        e.checked = false;
    });
}

const popupLinks = document.querySelectorAll('.popup-link');
if (popupLinks.length > 0) {
    for (let i = 0; i < popupLinks.length; i++) {
        const popupLink = popupLinks[i];
        popupLink.addEventListener("click", function(e) {
            const popupName = popupLink.getAttribute('href').replace('#', '');
            const curentPopup = document.getElementById(popupName);
            
            popupOpen(curentPopup);
            e.preventDefault();
        });
    }
}

const popupCloseIcon = document.querySelectorAll('.close-popup');
if (popupCloseIcon.length > 0) {

    for (let i = 0; i < popupCloseIcon.length; i++) {
        const el = popupCloseIcon[i];
        el.addEventListener("click", function(e) {
            
            popupClose(el.closest('.popup'));
            e.preventDefault();
        });
    }
}

document.addEventListener("keydown", (e) => {
    if (e.code == "Escape") {
        const popupActive = document.querySelector('.popup._active');
        popupClose(popupActive);
    }
});

autosize($('.textarea-autosize'));

// создание всплывающих сообщений
function customAlert(message) {

    // let alertText = $(`<div class="alert">
    //                         <div class="alert__inner">
    //                             <div class="alert__content">
    //                                 ${message}
    //                             </div>
    //                         </div>
    //                     </div>`)

    // $(body).prepend(alertText)

    // if (wait && typeof wait === 'boolean') {
    //     $('.alert__content').prepend($('<div class="alert__close">X</div>'))

    //     $('.alert__close').on('click', () => {
    //         alertText.remove()
    //     })

    //     document.querySelector('.alert').addEventListener('swiped-up', function (e) {
    //         alertText.remove()
    //     })

    // } else {
    //     alertText.delay(2000).slideUp('fast', () => alertText.remove())
    // }

    let baseAlert = $(`<div class="alert">
                            <div class="alert__inner">
                                <div class="alert__content">
                                    ${message}
                                </div>
                            </div>
                        </div>`)

    return baseAlert;

}

function hideAlert(alert, time) {
    alert.css('transform', 'translate(0px, -100%')
    alert.animate({
        'opacity': '0',
    }, time / 100)
}

function messagePopup(message, wait = false, viewTime = 2000) {

    let alertText = customAlert(`<div class="flash-message">
                                    <span>${message}</span>
                                </div>`)

    // alertText.css('transition', `${viewTime / 10000}s`)

    alertText.css('transition', `transform ${viewTime / 10000}s, opacity ${viewTime / 10000}s`)
    // alertText.css('transition', `opacity 10s`)

    $(body).prepend(alertText)

    if (wait && typeof wait === 'boolean') {
        $('.alert__content').prepend($('<div class="alert__close"><i class="fa-solid fa-xmark"></i></div>'))

        $('.alert__close').on('click', () => {
            alertText.remove()
        })

        document.querySelector('.alert').addEventListener('swiped-up', function (e) {
            // alertText.css('transform', 'translate(0px, -100%')
            // alertText.animate({
            //     'opacity': '0',
            // }, viewTime / 100)
            hideAlert(alertText, viewTime)
            setTimeout(() => alertText.remove(), viewTime / 10)
        })

    } else {
        // alertText.delay(viewTime).slideUp(viewTime, () => alertText.remove())

        setTimeout(function () {
            // alertText.css('transform', 'translate(0px, -100%')
            // alertText.animate({
            //     'opacity': '0',
            // }, viewTime / 100)
            hideAlert(alertText, viewTime)
            setTimeout(() => alertText.remove(), viewTime / 10)
        }, viewTime)

        // alertText.delay(viewTime).css('transform', 'translate(0px, -100%')
        // alertText.animate({
        //     'opacity': '0',
        // }, viewTime / 1000)

        // setTimeout(() => alertText.remove(), viewTime)
    }
}