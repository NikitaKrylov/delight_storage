// scroll-to-comments
const postInfoActive__com = document.querySelector('.comment-btn')
postInfoActive__com.addEventListener('click', function (e) {
    document.querySelector('.post-info-comments').scrollIntoView({
        behavior: "smooth",
        block: "start",
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

// answer-button
const InputReplyComment = document.createElement('div');
InputReplyComment.classList.add("comment-reply");
InputReplyComment.innerHTML =
    `<form id="reply-reply">
        <div class="comment-reply__input">
            <textarea class="comments-form__input-comment" name="reply-reply" required></textarea>
        </div>
        <div class="comment-reply__controls">
            <div class="comment-reply__send">
                <button class="button-send" type="submit"
                    aria-label="отправить коментарий">Оптравить</button>
            </div>
        </div>
    </form>`

$(".answer-button").on('click', function (e) {
    let currentButton = e.target;
    const parentButton = e.target.parentNode

    if (!currentButton.classList.contains("_active")) {
        currentButton.classList.add("_active");
        currentButton.textContent = 'отмена'
        // const firstlone = template.content.cloneNode(true);
        // parentButton.after(firstlone);
        parentButton.after(InputReplyComment);
        // document.querySelector('.comment-reply__input > div').focus();
        document.querySelector('.comment-reply__input > textarea').focus();

    } else {
        currentButton.classList.remove("_active");
        currentButton.textContent = 'ответить'
        // const clone = document.querySelector('.comment-reply');
        // clone.remove();
        InputReplyComment.remove();
    }

    $(document).on('click', function (e) {
        const commentReply = $('.comment-reply')
        if (!$(currentButton).is(e.target) && $(commentReply).has(e.target).length === 0) {
            currentButton.classList.remove("_active");
            currentButton.textContent = 'ответить'
            commentReply.remove();
        }
    });

    // var textarea = document.querySelector('.comments-form__input-comment');
    // textarea.addEventListener('keydown', function (e) {
    //     console.log('autosize');
    //     setInterval(() => {
    //         e.target.style.height = 'auto';
    //         e.target.style.height = `${e.target.scrollHeight}px`;
    //     }, 0);
    // });
    autosize($('.comments-form__input-comment'));
});

// input-comment
const InputNewComment = document.createElement('div');
InputNewComment.classList.add("comments-form__reply");
InputNewComment.innerHTML =
    `<div class="comments-form__input"
        aria-placeholder="Введите ваш комментарий">
        <textarea class="comments-form__input-comment" name="input-comments-form" required></textarea>
    </div>
    <div class="comments-form__controls">
        <div class="comment-form__send">
            <button class="button-send" type="submit"
                aria-label="отправить коментарий">Оптравить</button>
        </div>
    </div>`

$(".comments-form__pseudo-form").on('click', function (e) {
    // const firstlone = template0.content.cloneNode(true);
    document.querySelector('.comments-form__pseudo-form').remove();
    document.getElementById('input-comments-form').append(InputNewComment);
    // document.querySelector('.comment-form__input > div').focus();
    document.querySelector('.comments-form__input-comment').focus();

    // var textarea = document.querySelector('.comments-form__input-comment');
    // textarea.addEventListener('keydown', function (e) {
    //     console.log('autosize');
    //     setInterval(() => {
    //         e.target.style.height = 'auto';
    //         e.target.style.height = `${e.target.scrollHeight}px`;
    //     }, 0);
    // });
    autosize($('.comments-form__input-comment'));
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
        controls: true,
        showCloseIcon: true,
        download: true,
        rotate: true
    }
});
