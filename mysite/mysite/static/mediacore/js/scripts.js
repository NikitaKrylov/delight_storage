// slider gallery
$(document).ready(function () {
    $('.slider').slick({
        dots: true,
        infinite: true,
        speed: 100,
        slidesToShow: 1,
        cssEase: 'ease',
        adaptiveHeight: false,
        draggable: false,
        touchMove: false,
        waitForAnimate: false,
        variableWidth: false,
        touchThreshold: 7,
        // appendArrows: $('.arrow-btn'),
    });
})


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

    var sizer = '.sizer4';
    var gutter = '.gutter';
    var container = $('#gallery');

    container.imagesLoaded(function () {
        container.masonry({
            itemSelector: '.item-masonry',
            // columnWidth: sizer,
            percentPosition: true,
            transitionDuration: '0',
            // gutter: gutter,
            
        });
    
        var infinite = new Waypoint.Infinite({
            element: $('.infinite-container')[0],
            container: 'auto',
            items: '.infinite-item',
            more: '.infinite-more-link',
            offset: 'bottom-in-view',
            loadingClass: 'infinite-loading',
            onBeforePageLoad: function() {

            },
            onAfterPageLoad: function() {
                container.masonry('reloadItems');
                container.imagesLoaded().progress( function() {
                    container.masonry('layout');
                });
            },
        });
    });
});



if (document.body.classList.contains('_touch')) {
    // left-menu
    rlMenu('.header__movbile-navigation', '#nav-menu-mobile', '.close-ham-menu')
    // rightmenu
    rlMenu('.header__profile', '#profile-menu-mobile', '.close-ham-menu-2')
    // фильтры paper_mobile
    rlMenu('.btnFilter', '.paper_mobile', '.search-filter__head-2')

} else {
    // меню профиля
    $('.header__profile').on('click', function () {
        $(this).toggleClass('_active');
    });

    $(document).on('mouseup', function (e) { // При нажатии на документ
        let s = $('.header__profile._active'); // берём .block._active
        if (!s.is(e.target) && s.has(e.target).length === 0) {
            // Если нажат не он и не его дочернии И сам он существует
            s.removeClass('_active'); // То удаляем у него класс .active
        }
    });
}


function rlMenu(btn, rlmenu, close) {
    const button = document.querySelector(btn)
    const menu = document.querySelector(rlmenu)
    const closeHamMenu = document.querySelector(close)

    button.addEventListener("click", function (e) {
        menu.classList.toggle('_active');
        document.body.classList.toggle('_lock')
    });

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

function btn(name, clsname) {
    $(document).ready(function () {
        $(name).click(function () {
            $(clsname).addClass('_active');

        });
    });

    $(document).ready(function () {
        $('.search-filter__head').click(function () {
            $(clsname).removeClass('_active');
        });
    });
}


// topics
btn('.search-filter-submenu', '.search-filter-layout')
// tags
btn('.search-filter-submenu-2', '.search-filter-layout-2')





// checkbox
let boxes = document.querySelectorAll('.checkbox');
if (boxes) {
    for (let index = 0; index < boxes.length; index++) {
        const box = boxes[index];
        box.addEventListener("click", function (e) {
            box.classList.toggle('_active');
        });
    }
}


