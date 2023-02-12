const body = document.body;

if (body.classList.contains('_touch')) {

    // profile-menu
    // $(".header-profile-avatar").on('click', function (e) {
    //     rlMenu('#profile-menu-mobile', '.close-ham-menu-2');
    // });

} else {

    // меню профиля
    // $('.header__profile').on('click', function () {
    //     $(this).toggleClass('_active');
    // });

    // $(document).on('click', function (e) {
    //     if (!e.target.closest('.profile-dropdown') && !e.target.closest('.header__profile')) {
    //         $('.header__profile._active').removeClass('_active');
    //     }
    // });
}

function menuOverlayClose(menu) {
    menu.classList.remove('_active')
    body.classList.remove('_lock')
}

function menuOverlayOpen(menu, content) {
    menu.classList.add('_active');
    body.classList.add('_lock');

    menu.addEventListener('click', function (e) {
        if (!e.target.closest(content)) {
            menuOverlayClose(menu);
        }
    })
}

// function rlMenu(rlmenu, close) {
//     // const button = document.querySelector(btn)
//     const menu = document.querySelector(rlmenu)
//     const closeHamMenu = document.querySelector(close)

//     // if (button) {
//     //     button.addEventListener("click", function (e) {
//     //         menu.classList.toggle('_active');
//     //         document.body.classList.toggle('_lock')
//     //     });
//     // };

//     menu.classList.toggle('_active');
//     body.classList.toggle('_lock')

//     $(document).on('mouseup', function (e) {
//         e.preventDefault();

//         let s = $(menu)
//         if (menu.classList.contains('_active') === true) {
//             if (!s.is(e.target) && s.has(e.target).length === 0) {
//                 s.removeClass('_active');
//                 body.classList.remove('_lock')
//             } else {
//                 if (closeHamMenu) {
//                     closeHamMenu.addEventListener("click", function (e) {
//                         e.preventDefault();
//                         menu.classList.remove('_active');
//                         body.classList.remove('_lock')
//                     });
//                 }
//             }
//         }
//     });
// }

// mav-menu
// $(".header__mobile-navigation").on('click', function () {
//     // rlMenu('.sidebar-mobile', '.sidebar-mobile__btn')

//     menuOverlayOpen('.sidebar-mobile', '.sidebar-mobile__btn')
// });


// кнопка бурегр
const sidebarMobBtn = document.querySelector(".header__mobile-navigation")
if (sidebarMobBtn) {
    sidebarMobBtn.addEventListener('click', function(e) {
        const currBtn = sidebarMobBtn.getAttribute('href').replace('#', '');
        const currSidebar = document.getElementById(currBtn);
    
        menuOverlayOpen(currSidebar, '.sidebar-mobile__inner')
    })
}

const sidebarMobClose = document.querySelectorAll('.sidebar-mobile__btn');
if (sidebarMobClose.length > 0) {
    sidebarMobClose.forEach(function(val, index) {
        const sidebarClose = sidebarMobClose[index];
        sidebarClose.addEventListener("click", function(e) {
            
            menuOverlayClose(sidebarClose.closest('.sidebar-mobile'))
            e.preventDefault();
        });
    })
}


// view-hide-header
let lastScroll = 0;
const defaultOffset = 200;
const header = document.querySelector('.header');

if (header) {
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
}

// показать/скрыть popup(всплывающее окно)
// function popupOpen(curentPopup) {
//     body.classList.add('_lock')
//     curentPopup.classList.add('_active')
    
//     curentPopup.addEventListener('click', function (e) {
//         if (!e.target.closest('.popup__content')) {
//             popupClose(e.target.closest('.popup'))
//         }
//     });
// }

// function popupClose(curentPopup) {
//     curentPopup.classList.remove('_active')
//     body.classList.remove('_lock')

//     document.querySelectorAll('.radio__input').forEach(function (e) {
//         e.checked = false;
//     });
// }

const popupLinks = document.querySelectorAll('.popup-link');
if (popupLinks.length > 0) {
    popupLinks.forEach(function(val, index) {
        const popupLink = popupLinks[index];
        popupLink.addEventListener("click", function(e) {
            const popupName = popupLink.getAttribute('href').replace('#', '');
            const curentPopup = document.getElementById(popupName);
            
            // popupOpen(curentPopup);
            menuOverlayOpen(curentPopup, '.popup__content')
            e.preventDefault();
        });
    })
}

const popupCloseIcon = document.querySelectorAll('.close-popup');
if (popupCloseIcon.length > 0) {
    popupCloseIcon.forEach(function(val, index) {
        const popupClose = popupCloseIcon[index];
        popupClose.addEventListener("click", function(e) {
            
            // popupClose(el.closest('.popup'));
            menuOverlayClose(popupClose.closest('.popup'))
            e.preventDefault();
        });
    })
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
    $(body).prepend(alertText)
    
    // alertText.css('transition', `${viewTime / 10000}s`)
    // alertText.css('transition', `opacity 10s`)
    alertText.css('transition', `transform 0.2s, opacity 0.2s`)
    document.querySelector('.alert').addEventListener('swiped-up', function (e) {
        // alertText.css('transform', 'translate(0px, -100%')
        // alertText.animate({
        //     'opacity': '0',
        // }, viewTime / 100)
        hideAlert(alertText, viewTime)
        setTimeout(() => alertText.remove(), 200)
    })

    if (wait && typeof wait === 'boolean') {
        $('.alert__content').prepend($('<div class="alert__close"><i class="fa-solid fa-xmark"></i></div>'))

        $('.alert__close').on('click', () => {
            alertText.remove()
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