function btn(button, closebtn, parent) {
	const btn = $(button);
	const clsbtn = $(closebtn);
	const clsname = $(parent);
	const allcont = $(".wrapper");

	// clsname.css('visibility', 'visible');

	clsname.addClass("_active");
	// allcont.addClass('_anim-search');
	document.body.classList.add("_lock");

	$(document).on("mouseup", function (e) {
		// let s = $('search-container__wrapper')
		// if (!s.is(e.target) && clsname .has(e.target).length === 0) {
		if (!e.target.closest(".search__container")) {
			clsname.removeClass("_active");
			document.body.classList.remove("_lock");
		} else {
			if (clsbtn) {
				clsbtn.click(function (e) {
					// clsname.css('visibility', 'hidden');
					clsname.removeClass("_active");
					// allcont.removeClass('_anim-search');
					document.body.classList.remove("_lock");
				});
			}
		}
	});
}

let search = $(".search");
let searchBtn = $(".search-button");
let closeSearchBtn = $(".search__close-btn");
let searchInput = $(".search__input-form");
let searchForm = $("#search-form");
let isSearchOpen = false;

searchBtn.on("click", () => {
	isSearchOpen = true;

	menuOverlayOpen(search);
	setTimeout(() => searchInput.focus(), 100);
});

closeSearchBtn.on("click", function (e) {
	if (searchInput.val()) {
		searchInput.val("").focus();
		searchInput.trigger("input");
	} else {
		isSearchOpen = false;
		menuOverlayClose(search);
	}
});

search.on("click", function (e) {
	if (!(e.target.closest(".search__input-container") ?? e.target.closest(".tags-list__tag"))) {
		isSearchOpen = false;
		menuOverlayClose(search);
	}
});

if (!isMobile.any()) {
	document.addEventListener("keydown", (e) => {
		if (e.code == "Escape" && isSearchOpen) {
			menuOverlayClose(search);
		} else if (e.code == "Enter" && isSearchOpen) {
			searchForm.submit();
		}
	});
}

const tagList = document.querySelector(".tags-list");
const tagBtn = document.querySelector(".tags-list__tag");
// const searchInput = document.querySelector(".search__input-form");
// const searchInput = $(".search__input-form");
// let arrayitem = document.querySelectorAll('.tags-list__tag');
let arrayitem = [];

let inputDelay;
searchInput.on("input", function (e) {
	let textInp = searchInput.val().trim().toLowerCase();
	clearTimeout(inputDelay);

	inputDelay = setTimeout(function () {
		$.ajax({
			type: "GET",
			url: urlTag,
			data: { operation: textInp },
			dataType: "json",
			success: function (response) {
				function createTags(nameTag, slugTag) {
					let tag = document.createElement("div");
					tag.className = "tags-list__tag";
					tag.style = "display: none;";
					tag.innerHTML = `
						<input class="tags-list__checkbox hidden-input three-pos-inp" id="id_${slugTag}" name="${slugTag}"
						readonly tabindex="-1" type="number" value="0">
						<span>${nameTag}</span>`;

					return tag;
				}

				if (arrayitem.length !== 0) {
					arrayitem.forEach(function (e) {
						let valueinp = e.querySelector(".three-pos-inp").value;

						if (valueinp === "0") {
							e.remove();
						} else {
							let txtTag = e.getElementsByTagName("span")[0].textContent;
							e.getElementsByTagName("span")[0].innerHTML = txtTag;
							response = response.filter((tag) => tag.name !== txtTag);
						}
					});
				}

				response.forEach((tag, inx) => {
					let newTag = createTags(tag.name, tag.slug);
					tagList.append(newTag);
					show(newTag);
				});

				arrayitem = document.querySelectorAll(".tags-list__tag");
				tagSort(arrayitem);

				arrayitem.forEach(function (e) {
					textInp.split(" ").forEach(function (text) {
						if (searchForMatches(e.innerText, text)) {
							e.getElementsByTagName("span")[0].innerHTML = inserMark(
								e.innerText,
								e.innerText.toLowerCase().indexOf(text),
								text.length,
							);
						}
					});
				});
			},
		});
	}, 200);
});

// действия при нажатии на кнопку
function valueButton(btn) {
	let valueinp = btn.querySelector(".three-pos-inp").value;

	if (valueinp == "0") {
		btn.querySelector(".three-pos-inp").value = "1";
	} else if (valueinp == "1") {
		btn.querySelector(".three-pos-inp").value = "-1";
	} else if (valueinp == "-1") {
		btn.querySelector(".three-pos-inp").value = "0";
	}
}

function painButton(btn) {
	let valueinp = btn.querySelector(".three-pos-inp").value;

	if (valueinp == "0") {
		btn.classList.remove("_enabled");
		btn.classList.remove("_disabled");
	} else if (valueinp == "1") {
		btn.classList.add("_enabled");
	} else if (valueinp == "-1") {
		btn.classList.remove("_enabled");
		btn.classList.add("_disabled");
	}
}

function tagSort(array) {
	const sortArrayTags = [...array].sort(function (x, y) {
		x = x.querySelector(".three-pos-inp").value;
		y = y.querySelector(".three-pos-inp").value;
		return (!(x == "1" && y == "1") && x == "1") || (x == "-1" && y == "0") ? 1 : -1;
	});
	sortArrayTags.forEach(function (e) {
		// tagBtn.parentNode.prepend(e);
		tagList.prepend(e);
	});
}

$(tagList).on("click", function (e) {
	let clickBtn = e.target.closest(".tags-list__tag");
	if (clickBtn) {
		// setTimeout(() => clickBtn.querySelector(".three-pos-inp").focus(), 100);
		valueButton(clickBtn);
		painButton(clickBtn);

		tagSort(arrayitem);
	}
});

// действия при вводе текста
function searchForMatches(text, textInp) {
	// let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
	// return !(text.innerText.toLowerCase().search(textInp) == -1 || textInp == "");
	return text.toLowerCase().includes(textInp.toLowerCase()) || textInp == "";
}

function hide(event) {
	event.classList.remove("_show");
	$(event)
		.stop(false, true)
		.queue("fx", function () {
			$(this).fadeOut(200).dequeue("fx");
		});
}

function show(event) {
	event.classList.add("_show");
	$(event)
		.stop(false, true)
		.queue("fx", function () {
			$(this).fadeIn(300).dequeue("fx");
		});
}

function inserMark(string, position, fullLen) {
	return (
		string.slice(0, position) +
		"<mark>" +
		string.slice(position, position + fullLen) +
		"</mark>" +
		string.slice(position + fullLen)
	);
}

// кнопка показа всех тегов
// document.querySelector(".search__show-all-btn").addEventListener("click", () =>
// 	arrayitem.forEach(function (e) {
// 		show(e);
// 	}),
// );

// кнопка очистки выбранных тегов
document.querySelector(".search__hide-all-btn").addEventListener("click", () => {
	arrayitem = document.querySelectorAll(".tags-list__tag");

	arrayitem.forEach(function (e) {
		let valueinp = e.querySelector(".three-pos-inp").value;
		if (valueinp != "0") {
			e.querySelector(".three-pos-inp").value = "0";
			painButton(e);
		}
	});
});

// кнопка сортировки постов
$(".search-sort").on("click", function (e) {
	// if (e.target.closest(".search-sort__btn")) {
	// 	$(".search-sort__list")
	// 		.stop(false, true)
	// 		.queue("fx", function () {
	// 			$(this).slideToggle("fast").dequeue("fx");
	// 		});
	// } else
	if (e.target.closest(".search-sort__item")) {
		let txt = $(e.target).text();
		if (txt) {
			$(".search-sort__btn").text($(e.target).text());
		}
	}
});

$(document).ready(function () {
	document.querySelectorAll(".search-sort__item").forEach(function (value, inx) {
		if (value.querySelector(".search-sort__input").checked) {
			$(".search-sort__btn").text($(value).text());
		}
	});

	if ($(".search-sort__desc-asc input").prop("checked")) {
		$(".search-sort__desc-asc").attr("tooltip-text", "по убыванию");
	}
});

// сортировка убыванию/возрастанию
$(".search-sort__desc-asc").on("change", function (e) {
	if ($(e.target).prop("checked")) {
		$(e.target.closest(".search-sort__desc-asc"))
			.removeClass("_active")
			.attr("tooltip-text", "по убыванию");
	} else {
		$(e.target.closest(".search-sort__desc-asc"))
			.addClass("_active")
			.attr("tooltip-text", "по возростанию");
	}
});

// $(".search-sort__btn").on('click', function(e) {
//   $(".search-sort__list").slideToggle('fast');
// });

// $(document).on("click", function (e) {
// 	if (!e.target.closest(".search-sort")) {
// 		$(".search-sort__list").hide();
// 	}
// });
