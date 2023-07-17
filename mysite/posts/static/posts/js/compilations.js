new Swiper(".compilations__slider", {
	// loop: true,
	loopedSlides: 1,
	spaceBetween: 20,
	// freeMode: true,
	slidesPerView: 1,
	watchOverflow: true,
	grabCursor: true,
	speed: 300,

	scrollbar: {
		el: ".swiper-scrollbar",
		draggable: true,
	},

	breakpoints: {
		700: {
			slidesPerView: "auto",
		},
	},
});
