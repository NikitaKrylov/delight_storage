function btn(button, closebtn, parent) {
  const btn = $(button);
  const clsbtn = $(closebtn);
  const clsname = $(parent);
  const allcont = $('.wrapper');

  // clsname.css('visibility', 'visible');
  
  clsname.addClass('_active');
  // allcont.addClass('_anim-search');
  document.body.classList.add('_lock');

  $(document).on('mouseup', function (e) {
    // let s = $('search-container__wrapper')
    // if (!s.is(e.target) && clsname .has(e.target).length === 0) {
    if (!e.target.closest('.search__container')) {
      clsname.removeClass('_active');
      document.body.classList.remove('_lock');
    } else {
      if (clsbtn) {
        clsbtn.click(function (e) {
          // clsname.css('visibility', 'hidden');
          clsname.removeClass('_active');
          // allcont.removeClass('_anim-search');
          document.body.classList.remove('_lock');
        });
      };
    };
  });
};

$('.search-button').on('click',function(e) {
  btn('.search-button','.search__close-btn', '.search');
  setTimeout(() => document.querySelector('.search__input-form').focus(), 100);
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


// class tagSearch {
//   constructor(inputName, itemName) {
//     this.inputName = inputName;
//     this.itemName = itemName;
//   }

//   hide(event) {
//     event.classList.remove('_show');
//     $(event).stop(false, true).queue('fx', function() {
//       $(this).fadeOut(200).dequeue('fx');
//     });
//   }

//   show(event) {
//     event.classList.add('_show');
//     $(event).stop(false, true).queue('fx', function() {
//       $(this).fadeIn(200).dequeue('fx');
//     });
//   }

//   colorButton(arrayBtn) {
//     arrayBtn.forEach(function(e) {
//       let valueinp = e.querySelector('.three-pos-inp').value;
//       if (valueinp == '0') {
//         e.classList.remove('_enabled');
//         e.classList.remove('_disabled');
        
//       } else if (valueinp == '1') {
//         e.classList.add('_enabled');
//         this.show(e)
        
//       } else if (valueinp == '-1') {
//         e.classList.add('_disabled');
//         this.show(e)
//       }
//     }.bind(this));
//   }

//   tagSort(array) {
//     const sortArrayTags = [...array].sort(function(x, y) {
//       x = x.querySelector('.three-pos-inp').value;
//       y = y.querySelector('.three-pos-inp').value;
//       console.log('-----------------')
//       console.log(x, y)
//       return (!(x=='1' && y=='1') && x=='1' || (x=='-1' && y=='0'))? 1: -1
//     });
//     sortArrayTags.forEach( function (e) {
//       document.querySelector(this.itemName).parentNode.prepend(e);
//     }.bind(this));
//     console.log('-----------------')
//     console.log('sort')
//   }

//   inserMark(string, position, fullLen) {
//     return string.slice(0, position) + '<mark>' + string.slice(position, position+fullLen) + '</mark>' + string.slice(position+fullLen);
//   }

//   searchForMatches(text, textInp) {
//     // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
//     return !((text.innerText.toLowerCase().search(textInp) == -1) || (textInp == ''));
//   }

//   search(array, textInp) {
//     // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
//     array.forEach(function(e) {
//       let valueinp = e.querySelector('.three-pos-inp').value;
//       if (this.searchForMatches(e, textInp)) {
//         e.getElementsByTagName('span')[0].innerHTML = this.inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
//         this.show(e);
//       } else {
//         if (valueinp=='0') {
//           this.hide(e);
//         };
//         e.getElementsByTagName('span')[0].innerHTML = e.innerText;
//       };
//     }.bind(this));
//   }

//   start() {
//     let arrayitem = document.querySelectorAll(this.itemName);
//     document.querySelector(this.inputName).focus();
//     // console.log(arrayitem.length)

//     document.querySelector(this.itemName).parentNode.addEventListener('click', function(e) {
//       let clickBtn = e.target.closest(this.itemName)
//       if (clickBtn) {
//         setTimeout(() => clickBtn.querySelector('.three-pos-inp').focus(), 100);

//         let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
//         // скрыть кнопку если строка пустая и кнопка пасивна
//         if (!this.searchForMatches(clickBtn, textInp)) {
//           if (clickBtn.querySelector('.three-pos-inp').value == '0') {
//             this.hide(clickBtn);
//           };
//         };

//         this.tagSort(arrayitem);
//       };
//     }.bind(this));
    
//     document.querySelector(this.inputName).addEventListener('input', function() {
//       let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
//       this.search(arrayitem, textInp);
//     }.bind(this));

//     // document.querySelector(this.inputName).addEventListener('focusout', function() {
//     //   arrayitem.forEach(function(e) {
//     //     e.getElementsByTagName('span')[0].innerHTML = e.innerText;
//     //   });
//     // });
//     $(document).ready ( function(){
//       this.colorButton(arrayitem);
//      }.bind(this));
//     this.tagSort(arrayitem);
//     console.log('start')
//   }
// }

// const search = new tagSearch('.search-input__input', '.tags-list__tag');
// search.start();
// document.querySelectorAll('.tags-list__tag').forEach(function(e) {
//   console.log(e.querySelector('.three-pos-inp').value,e.classList)
// });

// $(document).ready ( function() {
//   search.start();
//   console.log('reade')
// })











// =========== попытка переделывать получше ===========


const tagBtn = document.querySelector('.tags-list__tag')
const searchInput = document.querySelector('.search__input-form')
let arrayitem = document.querySelectorAll('.tags-list__tag');



// действия при нажатии на кнопку
function valueButton(btn) {
    let valueinp = btn.querySelector('.three-pos-inp').value;
    if (valueinp == '0') {
      btn.querySelector('.three-pos-inp').value = '1';
    } else if (valueinp == '1') {
      btn.querySelector('.three-pos-inp').value = '-1';
    } else if (valueinp == '-1') {
      btn.querySelector('.three-pos-inp').value = '0';
    }
}


function painButton(btn) {
  let valueinp = btn.querySelector('.three-pos-inp').value;
  if (valueinp == '0') {
    btn.classList.remove('_enabled');
    btn.classList.remove('_disabled');
  } else if (valueinp == '1') {
    btn.classList.add('_enabled');
  } else if (valueinp == '-1') {
    btn.classList.add('_disabled');
  }
}


function tagSort(array) {
  const sortArrayTags = [...array].sort(function(x, y) {
    x = x.querySelector('.three-pos-inp').value;
    y = y.querySelector('.three-pos-inp').value;
    return (!(x=='1' && y=='1') && x=='1' || (x=='-1' && y=='0'))? 1: -1
  });
  sortArrayTags.forEach( function (e) {
    tagBtn.parentNode.prepend(e);
  });
}


tagBtn.parentNode.addEventListener('click', function(e) {
  let clickBtn = e.target.closest('.tags-list__tag')
  if (clickBtn) {
    setTimeout(() => clickBtn.querySelector('.three-pos-inp').focus(), 100);
    valueButton(clickBtn);
    painButton(clickBtn);

    // скрыть кнопку если строка пустая и кнопка пасивна
    // let textInp = searchInput.value.trim().toLowerCase();
    // if (!searchForMatches(clickBtn, textInp)) {
    //   if (clickBtn.querySelector('.three-pos-inp').value == '0') {
    //     hide(clickBtn);
    //   };
    // };

    tagSort(arrayitem);
  };
});




// действия при вводе текста
function searchForMatches(text, textInp) {
  // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
  return !((text.innerText.toLowerCase().search(textInp) == -1) || (textInp == ''));
}


function hide(event) {
  event.classList.remove('_show');
  $(event).stop(false, true).queue('fx', function() {
    $(this).fadeOut(200).dequeue('fx');
  });
}


function show(event) {
  event.classList.add('_show');
  $(event).stop(false, true).queue('fx', function() {
    $(this).fadeIn(200).dequeue('fx');
  });
}


function inserMark(string, position, fullLen) {
  return string.slice(0, position) + '<mark>' + string.slice(position, position+fullLen) + '</mark>' + string.slice(position+fullLen);
}


function search(array, textInp) {
  // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
  array.forEach(function(e) {
    let valueinp = e.querySelector('.three-pos-inp').value;
    if (searchForMatches(e, textInp)) {
      e.getElementsByTagName('span')[0].innerHTML = inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
      show(e);
    } else {
      if (valueinp=='0') {
        hide(e);
      };
      e.getElementsByTagName('span')[0].innerHTML = e.innerText;
    };
  });
}


searchInput.addEventListener('input', function() {
  let textInp = searchInput.value.trim().toLowerCase();
  search(arrayitem, textInp);
});




// действия при загрузке страницы
$(document).ready (function() {
  arrayitem.forEach(function(e) {
    painButton(e);
    let valueinp = e.querySelector('.three-pos-inp').value;
    if (valueinp != '0') {
      show(e);
    }
  })
  tagSort(arrayitem);
})


// =====================================================


document.querySelector(".search__show-all-btn").addEventListener("click", () => 
  arrayitem.forEach(function(e) {
    show(e);
  })
);

document.querySelector(".search__hide-all-btn").addEventListener("click", () => 
  arrayitem.forEach(function(e) {
    let valueinp = e.querySelector('.three-pos-inp').value;
    if (valueinp != '0') {
      e.querySelector('.three-pos-inp').value = '0';
      painButton(e);
    }
  })
);




