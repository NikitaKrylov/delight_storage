autosize($(".textarea-inp"));

function btn(button, closebtn, parent) {
	const btn = $(button);
	const clsbtn = $(closebtn);
	const clsname = $(parent);
	const allcont = $(".wrapper");

	clsname.addClass("_active");
	// document.body.classList.add('_lock');

	$(document).on("mouseup", function (e) {
		if (!e.target.closest(".search__container")) {
			clsname.removeClass("_active");
			document.body.classList.remove("_lock");
		} else {
			if (clsbtn) {
				clsbtn.click(function (e) {
					clsname.removeClass("_active");
					document.body.classList.remove("_lock");
				});
			}
		}
	});
}

// поиск и пвыбор тегов
$(".search__input-form").on("click", function (e) {
	btn(".search__input-form", ".search__close-btn", ".search");
	setTimeout(() => document.querySelector(".search__input-form").focus(), 100);
	// document.querySelector('.search-input__input').focus()
});

const tagBtn = document.querySelector(".tags-list__tag");
const searchInput = document.querySelector(".search__input-form");
const contTags = document.querySelector(".selected-tags__list");
const listTags = document.querySelector(".tags-list");
let arrayitem = document.querySelectorAll(".tags-list__tag");

// arrayitem.forEach((e) => {
// 	mtag.push(Number(e.querySelector(".tags-list__checkbox").value))
// })

// действия при нажатии на кнопку

function valueButton(btn) {
	// let valueinp = btn.querySelector('.three-pos-inp').value;
	let btninp = btn.querySelector(".three-pos-inp");
	let valueinp = btninp.dataset.state;

	if (valueinp == "0") {
		// btn.querySelector('.three-pos-inp').value = '1';
		btninp.dataset.state = 1;
		btninp.checked = true;
	} else if (valueinp == "1") {
		// btn.querySelector('.three-pos-inp').value = '0';
		btninp.dataset.state = 0;
		btninp.checked = false;
	}
}

function painButton(btn) {
	// let valueinp = btn.querySelector('.three-pos-inp').value;
	let valueinp = btn.querySelector(".three-pos-inp").dataset.state;
	if (valueinp == "0") {
		btn.classList.remove("_enabled");
		btn.classList.remove("_disabled");
	} else if (valueinp == "1") {
		btn.classList.add("_enabled");
	}
}

function selectedTags(btn) {
	// let valueinp = btn.querySelector('.three-pos-inp').value;
	let valueinp = btn.querySelector(".three-pos-inp").dataset.state;

	// 	const elementDiv = document.createElement("span");
	// 	elementDiv.classList.add('selected-tags__tag');
	// 	elementDiv.innerHTML =
	// 				`${btn.innerText} <button class="selected-tags__btn" type="button" title="Удалить"><i class="fa-solid fa-xmark"></i></button>`
	// 	contTags.append(elementDiv)

	// 	const delTagBtn = document.querySelector('.selected-tags')
	// 	delTagBtn.addEventListener('click', function(e) {
	// 		let clickBtn = e.target.closest('.selected-tags__btn')
	// 		if (clickBtn) {
	// 			valueButton(clickBtn);
	// 			painButton(clickBtn);
	// 		}
	// 	});

	if (valueinp == "1") {
		$(btn).appendTo($(contTags));
	} else {
		$(btn).appendTo($(listTags));
	}
}

// tagBtn.addEventListener('click', function(e) {
// $('.tags-list__tag').change(function(e) {
$(document).on("change", ".tags-list__tag", function (e) {
	let clickBtn = e.target.closest(".tags-list__tag");

	if (clickBtn) {
		valueButton(clickBtn);
		// painButton(clickBtn);
		selectedTags(clickBtn);
		// hide(clickBtn);
		// скрыть кнопку если строка пустая и кнопка пасивна
		// let textInp = searchInput.value.trim().toLowerCase();
		// if (!searchForMatches(clickBtn, textInp)) {
		//   if (clickBtn.querySelector('.three-pos-inp').dataset.state) {
		//     hide(clickBtn);
		//   };
		// };
	}
});

// действия при вводе текста

function searchForMatches(text, textInp) {
	// let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
	return text.toLowerCase().includes(textInp.toLowerCase()) || textInp == "";
}

function hide(event) {
	event.classList.remove("_show");
	// $(event).stop(false, true).queue('fx', function() {
	//   $(this).fadeOut(200).dequeue('fx');
	// });
}

function show(event) {
	event.classList.add("_show");
	// $(event).stop(false, true).queue('fx', function() {
	//   $(this).fadeIn(200).dequeue('fx');
	// });
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

function search(array, textInp) {
	// let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
	array.forEach((e) => {
		// let valueinp = e.querySelector('.three-pos-inp').value;
		let valueinp = e.querySelector(".three-pos-inp").dataset.state;

		for (let text of textInp.split(" ")) {
			if (searchForMatches(e.innerText, text) && valueinp == "0") {
				// e.getElementsByTagName('span')[0].innerHTML = inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
				show(e);
				return;
			} else {
				if (valueinp == "0") {
					hide(e);
				}
				// e.getElementsByTagName('span')[0].innerHTML = e.innerText;
			}
		}
	});
}

searchInput.addEventListener("input", function () {
	let textInp = searchInput.value.trim().toLowerCase();
	search(arrayitem, textInp);
});

// действия при загрузке страницы
// $(document).ready(function() {
//   arrayitem.forEach(function(e) {
//     // painButton(e);
//     let valueinp = e.querySelector('.three-pos-inp').dataset.state;
//     if (valueinp != '0') {
//       // show(e);
//       valueButton(e);
//       selectedTags(e);
//     }
//   })
// })

// создание пользолвательских тегов
$("#tag_creation_form").on("submit", function (event) {
	event.preventDefault();

	$.ajax({
		url: $(this).data("url"),
		type: $(this).attr("method"),
		data: {
			csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
			name: $("#id_name").val(),
		},

		success: function (json) {
			let maxValInp = $(".tags-list__tag").length;

			let newtag = $(`
				<div class="tags-list__tag _show">
					<label for="id_tags_${maxValInp}">
						<input checked class="tags-list__checkbox hidden-input three-pos-inp" data-state="1"
						id="id_tags_${maxValInp}" name="tags" tabindex="-1" type="checkbox" value="${json.id}">
						${json.name.charAt(0).toUpperCase() + json.name.slice(1)}
					</label>
				</div>
			`);

			$(".selected-tags__list").append(newtag);

			$.modal.close();
		},

		error: function (response) {
			$("#addtags-window")
				.find(".errorlist")
				.html(`<li>${response.responseJSON["errors"][0]}</li>`);
		},
	});
});

//добавление выбранных тегов
$.each($(".tags-list__tag"), function (inx, val) {
	if (val.querySelector(".tags-list__checkbox").checked) {
		valueButton(val);
		selectedTags(val);
		show(val);
	}
});

// =====================================================

// функции работы с файлами

function addFileField(name, container, countForm) {
	$(container).append(
		$(`
			<div class="add-file add-${name}">
				<!-- files-container -->

				<input id="id_${name}s-${countForm}-id" name="${name}s-${countForm}-id"
					 type="hidden">
				<input id="id_${name}s-${countForm}-post" name="${name}s-${countForm}-post"
					 type="hidden">

				<div class="add-file__controls">
					<label class="add-file__control add-file-btn-cont">

						<input ${name === "image" ? "accept = image/*" : ""}
							class="add-file__input hidden-input" 
							id="id_${name}s-${countForm}-file" name="${name}s-${countForm}-file"
							type="file">

						<span class="add-file__btn button">Выбрать файл</span>
					</label>
				</div>
			</div>
		`),
	);
}

function formatBytes(bytes, decimals = 2) {
	if (bytes === 0) {
		return "0";
	} else {
		var k = 1024;
		var dm = decimals < 0 ? 0 : decimals;
		var sizes = ["байт", "КБ", "МБ", "ГБ", "ТБ"];
		var i = Math.floor(Math.log(bytes) / Math.log(k));

		return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
	}
}

// function addFileField(name, container, form, countForm, addBtn) {
// 	let totalForms = document.querySelector(`#id_${name}s-TOTAL_FORMS`);

// 	console.log(form[0], "cloning");

// 	let newForm = form[0].cloneNode(true);
// 	let formRegex = RegExp(`${name}s-(\\d){1}-`, "g");

// 	newForm.innerHTML = newForm.innerHTML.replace(formRegex, `${name}s-${countForm}-`);

// 	console.log(newForm, "newform");

// 	if (newForm.querySelectorAll(".files-container").length) {
// 		newForm.querySelector(".add-file__btn").textContent = "Выбрать файл";
// 		newForm.querySelector(".files-container").remove();
// 		newForm.querySelector(".del-btn").remove();
// 		newForm.querySelector(".fileEditingLink").remove();
// 	}

// 	$(container).append(newForm);
// 	totalForms.setAttribute("value", `${countForm + 1}`);
// }

function createFileCont(file) {
	return $(`
    	<div class="files-container">
     		<div class="files-container__file-box">
        		${file}
      		</div>
    	</div>
  	`);
}

function createFileInfo(file, width, height) {
	let fileName = file.name;
	let fileSize = formatBytes(file.size, 2);
	let fileWidth = width;
	let fileHeight = height;

	return $(`
    <div class="files-container__file-info file-info">
      <div class="file-info__item">
        <div class="file-info__title title">Имя: </div>
        <div class="file-info__value">${fileName}</div>
      </div>
      <div class="file-info__item">
        <div class="file-info__title title">Размер: </div>
        <div class="file-info__value">${fileSize}</div>
      </div>
      <div class="file-info__item">
        <div class="file-info__title title">Разрешение: </div>
        <div class="file-info__value">${fileHeight} x ${fileWidth}</div>
      </div>
    </div>
  `);
}

function addDelBtn(currFile) {
	$(currFile.querySelector(".add-file-btn-cont")).after(
		$(`
			<span class="add-file__control del-btn button">
				Удалить
			</span>
		`),
	);
}

// фото
let cont = document.querySelector(".add-image-container");
let addImgForm = document.querySelectorAll(".add-image");
let imgFormNum = addImgForm.length - 1;

// добавление полей фото
// addButton.addEventListener("click", function (e) {
//     e.preventDefault()

//     let newForm = addImgForm[0].cloneNode(true);
//     let formRegex = RegExp(`images-(\\d){1}-`, 'g');
//     imgFormNum += 1;
//     newForm.innerHTML = newForm.innerHTML.replace(formRegex, `images-${imgFormNum}-`);

//     if (newForm.querySelectorAll('.files-container').length) {
//       newForm.querySelector('.add-file__btn').textContent = 'Выбрать файл';
//       newForm.querySelector('.files-container').remove();
//     }

//     cont.insertBefore(newForm, addButton)
//     totalForms.setAttribute('value', `${imgFormNum + 1}`)
// });

// addButton.addEventListener("click", function (e) {
// 	e.preventDefault();
// 	addFileField("image", cont, addImgForm, (imgFormNum += 1), addButton);
// });

function isImage(file) {
	return file.type.split("/")[0] === "image";
}

function createImageTag(imgLink) {
	return `<img class="files-container__file" src="${imgLink}">`;
}

$(".add-image-container").on("change", ".add-file__input", function (e) {
	const currFile = e.target.closest(".add-image");
	const [file] = currFile.querySelector(".add-file__input").files;

	if (file && isImage(file)) {
		if (currFile.querySelectorAll(".files-container").length) {
			currFile.querySelector(".files-container").remove();
			currFile.querySelector(".del-btn").remove();
		} else {
			addFileField("image", cont, (imgFormNum += 1));
		}

		document.querySelector("#id_images-TOTAL_FORMS").setAttribute("value", `${imgFormNum + 1}`);

		let imageCont = createFileCont(createImageTag(URL.createObjectURL(file)));
		$(currFile).prepend(imageCont);

		$(imageCont)
			.find("img")
			.on("load", () =>
				imageCont.append(createFileInfo(file, this.naturalWidth, this.naturalHeight)),
			);

		currFile.querySelector(".add-file__btn").textContent = "Другой файл";

		addDelBtn(currFile);
	} else {
		iziToast.info({
			title: "Выберите изображение",
		});
	}
});

$(".add-image-container").on("click", ".del-btn", (e) => e.target.closest(".add-image").remove());

// видео
let contVd = document.querySelector(".add-video-container");
let addVdForm = document.querySelectorAll(".add-video");
let vdFormNum = addVdForm.length - 1;

// добавление полей видео
// addVdButton.addEventListener("click", function (e) {
// 	e.preventDefault();
// 	addFileField("video", contVd, addVdForm, (vdFormNum += 1), addVdButton);
// });

function isVideo(file) {
	return file.type.split("/")[0] === "video";
}

function createVideoTag(videoLink) {
	return `<video class="files-container__file" width=100% height="100%" src="${videoLink}" controls></video>`;
}

$(".add-video-container").on("change", ".add-file__input", function (e) {
	const currFile = e.target.closest(".add-video");
	const [file] = currFile.querySelector(".add-file__input").files;

	if (file && isVideo(file)) {
		if (currFile.querySelectorAll(".files-container").length) {
			currFile.querySelector(".files-container").remove();
			currFile.querySelector(".del-btn").remove();
		} else {
			addFileField("video", contVd, (vdFormNum += 1));
		}

		document.querySelector("#id_videos-TOTAL_FORMS").setAttribute("value", `${vdFormNum + 1}`);

		let videoCont = createFileCont(createVideoTag(URL.createObjectURL(file)));
		$(currFile).prepend(videoCont);

		$(videoCont)
			.find("video")
			.on("loadeddata", () =>
				videoCont.append(createFileInfo(file, this.videoWidth, this.videoHeight)),
			);

		currFile.querySelector(".add-file__btn").textContent = "Другой файл";

		addDelBtn(currFile);
	} else {
		iziToast.info({
			title: "Выберите видео",
		});
	}
});

$(".add-video-container").on("click", ".del-btn", (e) => e.target.closest(".add-video").remove());

// инициализации календаря
if ($("body").hasClass("_pc")) {
	let todayBtn = {
		content: "Сегодня",
		className: "today-btn-picker",

		onClick: (dp) => {
			let date = new Date();
			dp.selectDate(date);
			dp.setViewDate(date);
		},
	};

	$(".input-calendar").attr("type", "text");

	new AirDatepicker(".input-calendar", {
		timepicker: true,
		buttons: [todayBtn, "clear"],
	});
}

// кнопка статуса
$(document).ready(function () {
	document.querySelectorAll(".status-post__item").forEach(function (value, inx) {
		if (value.querySelector(".status-post__input").checked) {
			// $(".status-post__btn").text($(value).text())
			let icon = $('<i class="status-post__icon fa-solid"></i>');
			$(".status-post__btn").text($(value).text()).append(icon);
		}
	});
});

$(".status-post__dropdown").on("click", function (e) {
	if (e.target.closest(".status-post__btn")) {
		$(".status-post__list")
			.stop(false, true)
			.queue("fx", function () {
				$(this).slideToggle("fast").dequeue("fx");
			});

		$(".status-post__icon").toggleClass("_active");
	} else if (e.target.closest(".status-post__item")) {
		let txt = $(e.target).text();
		if (txt) {
			let icon = $('<i class="status-post__icon fa-solid _active"></i>');
			$(".status-post__btn").text(txt).append(icon);
		}
	}
});

$(document).on("click", function (e) {
	if (!e.target.closest(".status-post__dropdown")) {
		$(".status-post__list").hide();
		$(".status-post__icon").removeClass("_active");
	}
});

// окно добавления тегов
$("a[data-modal='#addtags-window']").on("click", function (e) {
	$($(this).data("modal")).modal(baseSettingsModal);
	return false;
});

$("#addtags-window").on($.modal.OPEN, function (event, modal) {
	$(".input-user-tags").focus();
});

$("#addtags-window").on($.modal.CLOSE, function (event, modal) {
	$("#addtags-window").find(".errorlist").html("");
	$(".input-user-tags").val("");
});
