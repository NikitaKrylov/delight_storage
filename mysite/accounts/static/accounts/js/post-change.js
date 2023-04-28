const imagesEdLink = document.querySelectorAll(".imageEditingLink");

let reg = /.+(\.jpg|\.jpeg|\.gif)$/i;

for (link of imagesEdLink) {
	const currImg = link.closest(".add-image");
	const currVd = link.closest(".add-video");
	const srcL = link.getAttribute("href").replace("#", "");
	let fileTag;

	if (reg.test(srcL)) {
		fileTag = createImageTag(srcL);
		$(currImg).prepend(createFileCont(fileTag));
		currImg.querySelector(".add-file__btn").textContent = "Другой файл";
	} else {
		fileTag = createVideoTag(srcL);
		$(currVd).prepend(createFileCont(fileTag));
		currVd.querySelector(".add-file__btn").textContent = "Другой файл";
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
