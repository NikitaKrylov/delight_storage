// scroll-to-comments
const postInfoActive__com = document.querySelector('.comment-btn')
postInfoActive__com.addEventListener('click', function (e) {
    document.querySelector('.post-info-comments').scrollIntoView({
        behavior: "smooth",
        block: "start",
    });
})

const authorSubscribe = document.querySelector('.subscribe-btn')
    authorSubscribe.addEventListener('click', function (e) {
    const sub_url = $(authorSubscribe).attr('data-href')
    $.ajax({
        type: "GET",
        url: sub_url,
        dataType: "json",
        success: function(response) {
            if (response.has_sub == false){
                authorSubscribe.classList.remove('_active');
                authorSubscribe.querySelector(".subscribe-btn__text").textContent = "подписаться";
            }
            else if (response.has_sub == true){
                authorSubscribe.classList.add('_active');
                authorSubscribe.querySelector(".subscribe-btn__text").textContent = "отписаться";
            }
        }
    });

})

// кнопка сортировки коментарием
const sortBtn = $('.comments-form-sorting')
const sortlist = $('.comments-form-sorting__sortlist')
const sort = $('.comments-form-sorting__sort-btn')
const animSpeed = 150
sort.on("click", function () {
    if (!sort.hasClass('_active')) {
        sortlist.animate({
            height: 'show',
            opacity: 1,
        }, animSpeed).slideDown(animSpeed);
        sort.addClass("_active");
        sortlist.attr("aria-hidden", "false");
    } else {
        sortlist.animate({
            height: 'hide',
            opacity: 0,
        }, animSpeed).slideUp(animSpeed);
        sort.removeClass("_active");
        sortlist.attr("aria-hidden", "true");
    }
});
// при клике на пустое место
$(document).on('click', function (e) {
    if (!e.target.closest('.comments-form-sorting')) {
        sortlist.animate({
            height: 'hide',
            opacity: 0,
        }, animSpeed).slideUp(animSpeed);
        sort.removeClass("_active");
        sortlist.attr("aria-hidden", "true");
    }
    // if (!sort.is(e.target) && sortlist.has(e.target).length === 0 && sort.hasClass("_active")) {
    //     sortlist.animate({
    //         height: 'hide',
    //         opacity: 0,
    //     }, animSpeed).slideUp(animSpeed);
    //     sort.removeClass("_active");
    //     sortlist.attr("aria-hidden", "true");
    // }
});

// answer-button / жалобы-на комы
$(function() {
    document.querySelector('.comments-list').addEventListener('click', function(e) {
        let currentButton = e.target;
        if (currentButton.closest(".answer-button")) {
            if (!currentButton.classList.contains("_active")) {
                $(".answer-button").text('ответить').removeClass("_active");
                $('.comment-reply').prop("hidden", true);
                $('.comments-form__input-comment').val('');
                
                $(currentButton).addClass("_active");
                currentButton.textContent = 'отмена';
                setTimeout(() => currentButton.closest('.comment__body').querySelector('.comment-reply__input > textarea').focus(), 100);
                var commentboxId= $(currentButton).attr('data-commentbox');
                $('#'+commentboxId).prop("hidden", false);

            } else {
                $(".answer-button").text('ответить').removeClass("_active");
                $('.comment-reply').prop("hidden", true);
                $('.comments-form__input-comment').val('');
            }
        }

        if (currentButton.closest(".comment__control-btn")) {
            let complaintBtn = currentButton.closest(".comment__control-btn")
            const complaints = complaintBtn.parentNode.querySelector('.comment__control-dropdown')

            if (!complaintBtn.classList.contains("_active")) {
                $('.comment__control-dropdown').animate({
                    height: 'hide',
                    opacity: 0,
                }, animSpeed).slideUp(animSpeed);
                $(".comment__control-btn").removeClass("_active");
                $('.comment__control-dropdown').prop("hidden", true);
                $(complaints).animate({
                    height: 'show',
                    opacity: 1,
                }, animSpeed).slideDown(animSpeed);
                $(complaintBtn).addClass("_active");
                $(complaints).prop("hidden", false);
            } else {
                $(complaints).animate({
                    height: 'hide',
                    opacity: 0,
                }, animSpeed).slideUp(animSpeed);
                $(".comment__control-btn").removeClass("_active");
                $('.comment__control-dropdown').prop("hidden", true);
            }

            // при клике на пустое место
            $(document).on('click', function (e) {
                if (!e.target.closest('.comment__control')) {
                    $(".comment__control-btn").removeClass("_active");
                    $('.comment__control-dropdown').prop("hidden", true);
                    $('.comment__control-dropdown').animate({
                        height: 'hide',
                        opacity: 0,
                    }, animSpeed).slideUp(animSpeed);
                }
            });
        }
    });
});

// жалобы поста
let complaintPostBtn = document.querySelector(".post-complaints__button")
const complaintsPost = complaintPostBtn.parentNode.querySelector('.post-complaints__dropdown')
complaintPostBtn.addEventListener("click", (e) => {
    if (!complaintPostBtn.classList.contains("_active")) {
        $(complaintPostBtn).addClass("_active");
        $(complaintsPost).prop("hidden", false);

        $(complaintsPost).animate({
            height: 'show',
            opacity: 1,
        }, animSpeed).slideDown(animSpeed);        
    } else {
        $(complaintPostBtn).removeClass("_active");
        $(complaintsPost).prop("hidden", true);

        $(complaintsPost).animate({
            height: 'hide',
            opacity: 0,
        }, animSpeed).slideUp(animSpeed); 
    }
});
// при клике на пустое место
$(document).on('click', function (e) {
    if (!e.target.closest(".post-complaints__button")) {
        $(complaintPostBtn).removeClass("_active");
        $(complaintsPost).prop("hidden", true);

        $(complaintsPost).animate({
            height: 'hide',
            opacity: 0,
        }, animSpeed).slideUp(animSpeed); 
    }
});

// input-comment
$(".comments-form__pseudo-form").on('click', function (e) {
    document.querySelector('.comments-form__pseudo-form').remove();
    // document.getElementById('input-comments-form').append(InputNewComment);
    document.getElementById('input-comments-form').querySelector(".comments-form__reply").hidden = false;
    document.querySelector('.comments-form__input-comment').focus();
    autosize($('.textarea-inp'));
});

// sidebar-swiper
const swiper = new Swiper(".image-slider-2", {
    // loop: true,
    loopedSlides: 1,
    spaceBetween: 5,
    slidesPerView: 'auto',
    // touchRatio: 0,
    freeMode: true,
    watchSlidesProgress: true,
    watchOverflow: true,

    speed: 250,
});
// основной слайдер
const swiper2 = new Swiper(".image-slider", {
    // loop: true,
    loopedSlides: 1,
    spaceBetween: 10,
    // freeMode: true,
    slidesPerView: 1,
    // watchOverflow: true,
    grabCursor: true,

    // preloadImages: false,
    // lazy: {
    //     loadOnTransitionStart: true,
    //     loadPrevNext: true,
    // },
    // watchSlidesProgress: true,
    // watchSlidesVisibility: true,

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    keyboard: {
        enabled: true,
        onlyInViewport: true,
        pageUpDown: true,
    },
    thumbs: {
        swiper: swiper,
    },

    speed: 300,

    // для инвалидов 
    a11y: {
        enabled: true,
        prevSlideMessage: 'предыдущий слайд',
        nextSlideMessage: 'следующий слайд',
        firstSlideMessage: 'это первый слайд',
        lastSlideMessage: 'это последний слад',
        paginationBulletMessage: 'перейти к слайду {{index}}',
    }

});

// LightGallery
// const dynamicGallery = document.querySelector(".dynamic-gallery-button");
const popup = lightGallery(document.getElementById("lightgallery"), {
    autoplayFirstVideo: false,
    allowMediaOverlap: true,
    pager: false,
    closeOnTap: true,
    galleryId: "nature",
    selector: '.image-slider__image img',
    plugins: [lgZoom, lgFullscreen, lgRotate, lgHash, lgVideo],
    mobileSettings: {
        controls: false,
        showCloseIcon: true,
        download: true,
        rotate: true,
    }
});
