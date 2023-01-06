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

// показать/скрыть popup

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


