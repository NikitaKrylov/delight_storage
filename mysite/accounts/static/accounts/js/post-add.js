autosize($('.textarea-inp'));

function btn(button, closebtn, parent) {
    const btn = $(button);
    const clsbtn = $(closebtn);
    const clsname = $(parent);
    const allcont = $('.wrapper');
  
    clsname.addClass('_active');
    // document.body.classList.add('_lock');
  
    $(document).on('mouseup', function (e) {
      if (!e.target.closest('.search__container')) {
        clsname.removeClass('_active');
        document.body.classList.remove('_lock');
      } else {
        if (clsbtn) {
          clsbtn.click(function (e) {
            clsname.removeClass('_active');
            document.body.classList.remove('_lock');
          });
        };
      };
    });
};

$('.search__input-form').on('click',function(e) {
  btn('.search__input-form','.search__close-btn', '.search');
  setTimeout(() => document.querySelector('.search__input-form').focus(), 100);
  // document.querySelector('.search-input__input').focus()
});


const tagBtn = document.querySelector('.tags-list__tag')
const searchInput = document.querySelector('.search__input-form')
const contTags = document.querySelector('.selected-tags__list')
const listTags = document.querySelector('.tags-list')
let arrayitem = document.querySelectorAll('.tags-list__tag');

// действия при нажатии на кнопку
function valueButton(btn) {
    // let valueinp = btn.querySelector('.three-pos-inp').value;
    let valueinp = btn.querySelector('.three-pos-inp').dataset.state;
    if (valueinp == '0') {
      // btn.querySelector('.three-pos-inp').value = '1';
      btn.querySelector('.three-pos-inp').dataset.state = 1;
    } else if (valueinp == '1') {
      // btn.querySelector('.three-pos-inp').value = '0';
      btn.querySelector('.three-pos-inp').dataset.state = 0;
    }
}


function painButton(btn) {
  // let valueinp = btn.querySelector('.three-pos-inp').value;
  let valueinp = btn.querySelector('.three-pos-inp').dataset.state;
  if (valueinp == '0') {
    btn.classList.remove('_enabled');
    btn.classList.remove('_disabled');
  } else if (valueinp == '1') {
    btn.classList.add('_enabled');
  }
}


function selectedTags(btn) {
    // let valueinp = btn.querySelector('.three-pos-inp').value;
    let valueinp = btn.querySelector('.three-pos-inp').dataset.state;

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
    if (valueinp=='1') {
        $(btn).appendTo($(contTags))
    } else {
        $(btn).appendTo($(listTags))
    }
}


// tagBtn.addEventListener('click', function(e) {
// $('.tags-list__tag').change(function(e) {
$('.tags-list__tag').on('change', function(e) {
  let clickBtn = e.target.closest('.tags-list__tag')

  if (clickBtn) {
    valueButton(clickBtn);
    painButton(clickBtn);
    selectedTags(clickBtn);
    // hide(clickBtn);
    // скрыть кнопку если строка пустая и кнопка пасивна
    // let textInp = searchInput.value.trim().toLowerCase();
    // if (!searchForMatches(clickBtn, textInp)) {
    //   if (clickBtn.querySelector('.three-pos-inp').dataset.state) {
    //     hide(clickBtn);
    //   };
    // };
  };
});

// действия при вводе текста
function searchForMatches(text, textInp) {
  // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
  return !((text.innerText.toLowerCase().search(textInp) == -1) || (textInp == ''));
}


function hide(event) {
  event.classList.remove('_show');
  // $(event).stop(false, true).queue('fx', function() {
  //   $(this).fadeOut(200).dequeue('fx');
  // });
}


function show(event) {
  event.classList.add('_show');
  // $(event).stop(false, true).queue('fx', function() {
  //   $(this).fadeIn(200).dequeue('fx');
  // });
}


function inserMark(string, position, fullLen) {
  return string.slice(0, position) + '<mark>' + string.slice(position, position+fullLen) + '</mark>' + string.slice(position+fullLen);
}


function search(array, textInp) {
  // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
  array.forEach(function(e) {
    // let valueinp = e.querySelector('.three-pos-inp').value;
    let valueinp = e.querySelector('.three-pos-inp').dataset.state;
    if (searchForMatches(e, textInp) && valueinp == '0') {
      // e.getElementsByTagName('span')[0].innerHTML = inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
      show(e);
    } else {
      if (valueinp=='0') {
        hide(e);
      };
      // e.getElementsByTagName('span')[0].innerHTML = e.innerText;
    };
  });
}


searchInput.addEventListener('input', function() {
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


// =====================================================


// добавление/удаление картинок
let cont = document.querySelector('.add-image-container')
let addImgForm = document.querySelectorAll('.add-image')
let imgFormNum = addImgForm.length - 1
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector('#id_images-TOTAL_FORMS')
let imgInp = document.querySelector('.add-image__input')

function formatBytes(bytes, decimals = 2) {
	if (bytes === 0) {
		return '0';
	} else {
		var k = 1024;
		var dm = decimals < 0 ? 0 : decimals;
		var sizes = ['байт', 'КБ', 'МБ', 'ГБ', 'ТБ'];
		var i = Math.floor(Math.log(bytes) / Math.log(k));
    
		return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
	}
}

addButton.addEventListener("click", function (e) {
    e.preventDefault()

    let newForm = addImgForm[0].cloneNode(true)
    let formRegex = RegExp(`images-(\\d){1}-`, 'g')
    imgFormNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `images-${imgFormNum}-`)

    // newForm.querySelector('.images-container').innerHTML = ''
    let imgCont = newForm.querySelector('.images-container')
    if (imgCont) {
      imgCont.remove()
      // imgCont.innerHTML = ''
    }
    
    newForm.querySelector('.add-image__text').textContent = 'Выбрать файл'

    cont.insertBefore(newForm, addButton)
    totalForms.setAttribute('value', `${imgFormNum + 1}`)
});


$('.add-image-container').on('change', '.add-image__input', function (e) {
  const currAddImg = e.target.closest('.add-image')
  let imagesCont;
  let imgName;
  let imgSize;
  let imgWidth;
  let imgHeight;

  if (currAddImg.querySelectorAll('.images-container').length) {
    currAddImg.querySelector('.images-container').remove()
  }
  
  let imgCont = document.createElement('div')
  imgCont.className = 'images-container'
  currAddImg.prepend(imgCont)
  imagesCont = currAddImg.querySelector('.images-container')
    
    // let imgCont = document.createElement('div')
    // imgCont.className = 'images-container'
    // currAddImg.prepend(imgCont)
    
    // const imagesCont = currAddImg.querySelector('.images-container')
    // imagesCont.innerHTML = ''

    const [file] = currAddImg.querySelector('.add-image__input').files

    if (file) {
        let srcLink = URL.createObjectURL(file);

        let imgCont = document.createElement('div');
        imgCont.className = 'images-container__image-item';
        imgCont.innerHTML = '<img class="images-container__image" src=' + srcLink + ' >';
        imagesCont.append(imgCont);


        let imgInfo = document.createElement('div');
        var currImg  = imgCont.getElementsByTagName('img')[0];

        currImg.onload = function() {
          newimg = new Image;
          newimg.src = srcLink
          
          imgName = file.name
          imgSize = formatBytes(file.size, 2)
          imgWidth = newimg.width
          imgHeight = newimg.height
          
          imgInfo.className = 'images-container__image-info image-info';
          imgInfo.innerHTML = `<div class="image-info__item">
                                   <div class="image-info__title title">Имя: </div>
                                   <div class="image-info__value">${imgName}</div>
                               </div>
                               <div class="image-info__item">
                                   <div class="image-info__title title">Размер: </div>
                                   <div class="image-info__value">${imgSize}</div>
                               </div>
                               <div class="image-info__item">
                                  <div class="image-info__title title">Разрешение: </div>
                                  <div class="image-info__value">${imgHeight} x ${imgWidth}</div>
                              </div>`;
        }

        imagesCont.append(imgInfo);

        currAddImg.querySelector('.add-image__text').textContent = 'Другой файл'
    }
})
  

$('.add-image-container').on('click', '.del-btn', function (e) {
  const currAddImg = e.target.closest('.add-image')
  currAddImg.remove()
})


// инициализации календаря

if ($('body').hasClass('_pc')) {
  let todayBtn = {
    content: 'Сегодня',
    className: 'today-btn-picker',
    onClick: (dp) => {
      let date = new Date();
      dp.selectDate(date);
      dp.setViewDate(date);
    }
  }
  
  $('#id_time').attr('type', 'text')
  new AirDatepicker('#id_time', {
    timepicker: true,
    buttons: [todayBtn, 'clear'],
  });
}


// кнопка статуса
$(document).ready(function() {
  document.querySelectorAll(".status-post__item").forEach(function(value, inx) {
    if (value.querySelector(".status-post__input").checked) {
      // $(".status-post__btn").text($(value).text())
      let icon = $('<i class="status-post__icon fa-solid"></i>')
      $(".status-post__btn").text($(value).text()).append(icon)
    }
  })
})

$(".status-post__dropdown").on('click', function (e) {
  if (e.target.closest(".status-post__btn")) {
    $(".status-post__list").stop(false, true).queue('fx', function() {
      $(this).slideToggle('fast').dequeue('fx');
    });

    $(".status-post__icon").toggleClass("_active");

  } else if (e.target.closest(".status-post__item")) {
    let txt = $(e.target).text()
    if (txt) {
      let icon = $('<i class="status-post__icon fa-solid _active"></i>')
      $(".status-post__btn").text(txt).append(icon)
    }
  }
});

$(document).on('click', function(e) {
  if (!e.target.closest('.status-post__dropdown')) {
    $(".status-post__list").hide();
    $(".status-post__icon").removeClass("_active");
	}
});

