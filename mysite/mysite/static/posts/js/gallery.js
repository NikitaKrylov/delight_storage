// external js: masonry.pkgd.js
// $(document).ready(function () {
jQuery(window).on('load', function(){
    let sizer = '.sizer4';
    let container = $('.gallery');

    container.imagesLoaded(function () {
        container.masonry({
            itemSelector: '.item-masonry',
            // columnWidth: sizer,
            // gutter: 10,
            percentPosition: true,
            transitionDuration: '0',
        });

        const InfinitePagination = new Waypoint.Infinite({
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
                container.imagesLoaded().progress(function() {
                    container.masonry('layout');
                })
            },
        })
    })
})
