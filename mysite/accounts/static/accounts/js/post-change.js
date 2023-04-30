const imagesEdLink = document.querySelectorAll(".fileEditingLink");

let reg = /.+(\.jpg|\.jpeg|\.gif)$/i;

function createFile(file, fileTag) {
	// fileTag = createVideoTag(link);
	$(file).prepend(createFileCont(fileTag));
	file.querySelector(".add-file__btn").textContent = "Другой файл";
	addDelBtn(file);
}

//добавление имеющихся фото и видео
for (link of imagesEdLink) {
	const currImg = link.closest(".add-image");
	const currVd = link.closest(".add-video");
	// const srcL = link.getAttribute("href").replace("#", "");
	const srcL = link.getAttribute("href");

	if (reg.test(srcL)) {
		// fileTag = createImageTag(srcL);
		// $(currImg).prepend(createFileCont(fileTag));
		// currImg.querySelector(".add-file__btn").textContent = "Другой файл";

		createFile(currImg, createImageTag(srcL));
	} else {
		// fileTag = createVideoTag(srcL);
		// $(currVd).prepend(createFileCont(fileTag));
		// currVd.querySelector(".add-file__btn").textContent = "Другой файл";
		createFile(currVd, createVideoTag(srcL));
	}
}

// $(currFile).prepend(imageCont);

//добавление выбранных тегов
$.each($(".tags-list__tag"), function (inx, val) {
	if (val.querySelector(".tags-list__checkbox").checked) {
		valueButton(val);
		selectedTags(val);
		show(val);
	}
});
