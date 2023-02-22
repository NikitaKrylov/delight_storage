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

$(".search-button").on("click", function (e) {
	btn(".search-button", ".search__close-btn", ".search");
	setTimeout(() => document.querySelector(".search__input-form").focus(), 100);
	// document.querySelector('.search-input__input').focus()
});

// // желательно чтобы кнопки имели общий родитель который имеет селетор или id
// function threeBtn(btnName) {
//   let parentBtn = document.querySelector(btnName).parentNode;
//   // let arrayBtn = document.querySelectorAll(btnName)

//   parentBtn.addEventListener('click', function(e) {
//     let tar = e.target.closest(btnName);
//     if (tar) {
//       let valueinp = tar.querySelector('.three-pos-inp').value;
//       if (valueinp == '0') {
//         tar.classList.add('_enabled');
//         tar.querySelector('.three-pos-inp').value = '1';
//         console.log('value 1', tar.querySelector('.three-pos-inp').value)

//       } else if (valueinp == '1') {
//         tar.classList.add('_disabled');
//         tar.classList.remove('_enabled');
//         tar.querySelector('.three-pos-inp').value = '-1';
//         console.log('value -1', tar.querySelector('.three-pos-inp').value)

//       } else if (valueinp == '-1') {
//         tar.classList.remove('_disabled');
//         tar.querySelector('.three-pos-inp').value = '0';
//         console.log('value 0', tar.querySelector('.three-pos-inp').value)
//       }
//     };
//   });
// };
// threeBtn('.tags-list__tag');

const tagList = document.querySelector(".tags-list");
const tagBtn = document.querySelector(".tags-list__tag");
const searchInput = document.querySelector(".search__input-form");
// let arrayitem = document.querySelectorAll('.tags-list__tag');
let arrayitem = [];

$(searchInput).on("input", function () {
	let textInp = $(".search__input-form").val().toLowerCase();

	$.ajax({
		type: "GET",
		url: urlTag,
		data: { operation: textInp },
		dataType: "json",
		success: function (response) {
			let selectTags = [];

			// удаление старых тегво кроме выбранных
			if (arrayitem.length !== 0) {
				arrayitem.forEach(function (e) {
					let valueinp = e.querySelector(".three-pos-inp").value;

					if (valueinp == "0") {
						e.remove();
					} else {
						let txtTag = e.getElementsByTagName("span")[0].textContent;
						e.getElementsByTagName("span")[0].innerHTML = txtTag;
						selectTags.push(txtTag);
					}
				});
			}

			// удаление дубликатов выбранныех тегов
			let res = response["tags"].filter(function (e) {
				let inxTag = selectTags.indexOf(e["name"]);
				return !(inxTag in selectTags);
			});

			// создание, добавление и отображение новых тегов
			res.forEach(function (e) {
				let name = e["name"];
				let slug = e["slug"];

				let tag = document.createElement("div");
				tag.className = "tags-list__tag";
				tag.style = "display: none;";
				tag.innerHTML = `
					<input class="tags-list__checkbox hidden-input three-pos-inp" id="id_${slug}" name="${slug}"
					readonly tabindex="-1" type="number" value="0">
					<span>${name}</span>`;

				tagList.append(tag);

				// tag.getElementsByTagName("span")[0].innerHTML = inserMark(
				// 	name,
				// 	name.toLowerCase().search(textInp),
				// 	textInp.length,
				// );
				show(tag);
			});

			arrayitem = document.querySelectorAll(".tags-list__tag");
			arrayitem.forEach(function (e) {
				e.getElementsByTagName("span")[0].innerHTML = inserMark(
					e.innerText,
					e.innerText.toLowerCase().search(textInp),
					textInp.length,
				);
			});
		},
	});
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
		setTimeout(() => clickBtn.querySelector(".three-pos-inp").focus(), 100);
		valueButton(clickBtn);
		painButton(clickBtn);

		tagSort(arrayitem);
	}
});

// tagBtn.parentNode.addEventListener('click', function(e) {
//   let clickBtn = e.target.closest('.tags-list__tag')
//   if (clickBtn) {
//     setTimeout(() => clickBtn.querySelector('.three-pos-inp').focus(), 100);
//     valueButton(clickBtn);
//     painButton(clickBtn);

//     tagSort(arrayitem);
//   };
// });

// действия при вводе текста
// function searchForMatches(text, textInp) {
//   // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
//   return !((text.innerText.toLowerCase().search(textInp) == -1) || (textInp == ''));
// }

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

// function search(array, textInp) {
//   // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
//   array.forEach(function(e) {
//     let valueinp = e.querySelector('.three-pos-inp').value;
//     if (searchForMatches(e, textInp)) {
//       e.getElementsByTagName('span')[0].innerHTML = inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
//       show(e);
//     } else {
//       if (valueinp=='0') {
//         hide(e);
//       };
//       e.getElementsByTagName('span')[0].innerHTML = e.innerText;
//     };
//   });
// }

// searchInput.addEventListener('input', function() {
//   let textInp = searchInput.value.trim().toLowerCase();
//   search(arrayitem, textInp);
// });

// // действия при загрузке страницы
// // $(document).ready(function() {
// //   arrayitem.forEach(function(e) {
// //     painButton(e);
// //     let valueinp = e.querySelector('.three-pos-inp').value;
// //     if (valueinp != '0') {
// //       show(e);
// //     }
// //   })
// //   tagSort(arrayitem);
// // })

// =====================================================

document.querySelector(".search__show-all-btn").addEventListener("click", () =>
	arrayitem.forEach(function (e) {
		show(e);
	}),
);

document.querySelector(".search__hide-all-btn").addEventListener("click", () =>
	arrayitem.forEach(function (e) {
		let valueinp = e.querySelector(".three-pos-inp").value;
		if (valueinp != "0") {
			e.querySelector(".three-pos-inp").value = "0";
			painButton(e);
		}
	}),
);

$(".search-sort").on("click", function (e) {
	if (e.target.closest(".search-sort__btn")) {
		$(".search-sort__list")
			.stop(false, true)
			.queue("fx", function () {
				$(this).slideToggle("fast").dequeue("fx");
			});
	} else if (e.target.closest(".search-sort__item")) {
		let txt = $(e.target).text();
		if (txt) {
			$(".search-sort__btn").text($(e.target).text());
		}
	}
});

$(".search-sort__desc-asc").on("change", function (e) {
	$(e.target.closest(".search-sort__desc-asc")).toggleClass("_active");
});

// $(".search-sort__btn").on('click', function(e) {
//   $(".search-sort__list").slideToggle('fast');
// });

$(document).on("click", function (e) {
	if (!e.target.closest(".search-sort")) {
		$(".search-sort__list").hide();
	}
});
