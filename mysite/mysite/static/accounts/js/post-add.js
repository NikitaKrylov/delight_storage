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
const contTags = document.querySelector('.selected-tags')
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
    console.log(btn)

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
$('.tags-list__tag').change(function(e) {
  let clickBtn = e.target.closest('.tags-list__tag')
  if (clickBtn) {
    valueButton(clickBtn);
    painButton(clickBtn);
    selectedTags(clickBtn);
    // hide(clickBtn);
    // скрыть кнопку если строка пустая и кнопка пасивна
    let textInp = searchInput.value.trim().toLowerCase();
    if (!searchForMatches(clickBtn, textInp)) {
      if (clickBtn.querySelector('.three-pos-inp').dataset.state) {
        hide(clickBtn);
      };
    };
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
//     painButton(e);
//     let valueinp = e.querySelector('.three-pos-inp').value;
//     if (valueinp != '0') {
//       show(e);
//     }
//   })
// })


// =====================================================