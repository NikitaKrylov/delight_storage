const imagesEdLink = document.querySelectorAll(".imageEditingLink");

let reg = /.+(\.jpg|\.jpeg|\.gif)$/i;

function createFile(file, link) {
	fileTag = createVideoTag(link);
	$(file).prepend(createFileCont(fileTag));
	file.querySelector(".add-file__btn").textContent = "Другой файл";
	addDelBtn(file);
}

for (link of imagesEdLink) {
	const currImg = link.closest(".add-image");
	const currVd = link.closest(".add-video");
	const srcL = link.getAttribute("href").replace("#", "");
	let fileTag;

	if (reg.test(srcL)) {
		// fileTag = createImageTag(srcL);
		// $(currImg).prepend(createFileCont(fileTag));
		// currImg.querySelector(".add-file__btn").textContent = "Другой файл";
		createFile(currImg, srcL);
	} else {
		// fileTag = createVideoTag(srcL);
		// $(currVd).prepend(createFileCont(fileTag));
		// currVd.querySelector(".add-file__btn").textContent = "Другой файл";
		createFile(currVd, srcL);
	}
}

// $(currFile).prepend(imageCont);


for (tag of $(".tags-list__tag")) {
	if (tag.querySelector(".tags-list__checkbox").checked) {
		console.log(tag)
		valueButton(tag);
		selectedTags(tag);
		show(tag);
	}
}
