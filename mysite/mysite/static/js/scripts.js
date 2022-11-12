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

// external js: masonry.pkgd.js
// $(document).ready(function () {
jQuery(window).on('load', function(){
    // jQuery('.item-masonry').hover(
    //     function () {
    //         $(this).find(".cover-item-gallery").fadeIn(200);
    //     },
    //     function () {
    //         $(this).find(".cover-item-gallery").fadeOut(200);
    //     }
    // );
    // jQuery('.gallery__author').hover(
    //     function () {

    //     }
    // );

    let sizer = '.sizer4';
    let container = $('.gallery');

    if (container) {
        container.imagesLoaded(function () {
            container.masonry({
                itemSelector: '.item-masonry',
                // columnWidth: sizer,
                // gutter: 10,
                percentPosition: true,
                transitionDuration: '0.2s',
            })
        });
    }
    // let elem = document.querySelector('#gallery');
    // let msnry = new Masonry(elem, {
    //     itemSelector: '.item-masonry',
    //     columnWidth: sizer,
    //     percentPosition: true,
    //     transitionDuration: '0.2s',
    // });
});


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

    $(document).on('click', function (e) {
        if (!e.target.closest('.profile-dropdown') && !e.target.closest('.header__profile')) {
            $('.header__profile._active').removeClass('_active');
        }
        // let s = $('.header__profile._active');
        // if (!s.is(e.target) && s.has(e.target).length === 0) {
        //     s.removeClass('_active');
        // }
    });
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


// function btn(button, closebtn, clsname) {
//     $(button).click(function () {
//         $(clsname).addClass('_active');
//     });

//     $(closebtn).click(function () {
//         $(clsname).removeClass('_active');
//     });
// }

// like button
$(".like-btn").on('click', function (e) {
    // $('.like-button').toggle('_active');
    e.currentTarget.classList.toggle('_active');
});


$(".checkbox").on('click', function (e) {
    var context = $(e.currentTarget);
    let value = context.children('.dissabled-and-enabled').val();

    if (value === '0') {
        context.children('.dissabled-and-enabled').val('1')
    } else if (value === '1') {
        context.children('.dissabled-and-enabled').val('2')
    } else if (value === '2') {
        context.children('.dissabled-and-enabled').val('0')
    }
});


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
