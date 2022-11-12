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