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


if (document.body.classList.contains('_touch')) {

    // profile-menu
    $(".header-profile-avatar").on('click', function (e) {
        rlMenu('#profile-menu-mobile', '.close-ham-menu-2');
    });

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
    document.body.classList.toggle('_lock')

    $(document).on('mouseup', function (e) {
        let s = $(menu)

        if (menu.classList.contains('_active') === true) {
            if (!s.is(e.target) && s.has(e.target).length === 0) {
                s.removeClass('_active');
                document.body.classList.remove('_lock')
            } else {
                if (closeHamMenu) {
                    closeHamMenu.addEventListener("click", function (e) {
                        menu.classList.remove('_active');
                        document.body.classList.remove('_lock')
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
