function btn(button, closebtn, parent) {
  const btn = $(button)
  const clsbtn = $(closebtn)
  const clsname = $(parent)
  const allcont = $('.wrapper')
  
  clsname.addClass('_active');
  allcont.addClass('_anim-search')
  document.body.classList.add('_lock')

  $(document).on('mouseup', function (e) {
    // let s = $('search-container__wrapper')
    // if (!s.is(e.target) && clsname .has(e.target).length === 0) {
    if (!e.target.closest('.search-container__wrapper')) {
      clsname.removeClass('_active')
      allcont.removeClass('_anim-search')
      document.body.classList.remove('_lock')
    } else {
      if (clsbtn) {
        clsbtn.click(function (e) {
          clsname.removeClass('_active')
          allcont.removeClass('_anim-search')
          document.body.classList.remove('_lock')
        });
      }
    }
  });
}

$('.search-button').click(function() {
  btn('.search-button','.search-input__close', '.search-container')
});

// желательно чтобы кнопки имели общий родитель который имеет селетор или id
function threeBtn(btnName) {
  let parentBtn = document.querySelector(btnName).parentNode
  let arrayBtn = document.querySelectorAll(btnName)
  arrayBtn.forEach(function(e) {
    e.dataset.threePos = 0
  });

  parentBtn.addEventListener('click', function(e) {
    let tar = e.target.closest(btnName)  
    if (tar) {
      let valuebtn = tar.getAttribute("data-three-pos");
      if (valuebtn == '0') {
        // btn.attr('data-three-pos', '1')
        tar.dataset.threePos = 1
      } else if (valuebtn == '1') {
        // btn.attr('data-three-pos', '-1')
        tar.dataset.threePos = -1
      } else if (valuebtn == '-1') {
        // btn.attr('data-three-pos', '0')
        tar.dataset.threePos = 0
      }
    }
  });
}
threeBtn('.tags-list__tag')

// const threePosBtns = document.querySelectorAll('[data-three-pos]')
// threePosBtns.forEach( function(e) {
//   e.dataset.threePos = 0
// });

// $(threePosBtns).on('click', function(e) {
//   let btn = $(e.currentTarget);
//   let valuebtn = btn.attr("data-three-pos");
  
//   if (valuebtn == '0') {
//     btn.attr('data-three-pos', '1')
//   } else if (valuebtn == '1') {
//     btn.attr('data-three-pos', '-1')
//   } else if (valuebtn == '-1') {
//     btn.attr('data-three-pos', '0')
//   }
// });

// document.querySelector('.search-input__input').oninput = function() {
//   search()
// };

class Search {
  constructor(inputName, itemName) {
    this.inputName = inputName;
    this.itemName = itemName;
  }

  hide(event) {
    event.classList.remove('_show');
    $(event).stop(false, true).queue('fx', function() {
      $(this).fadeOut(200).dequeue('fx');
    });
  };

  show(event) {
    event.classList.add('_show');
    $(event).stop(false, true).queue('fx', function() {
      $(this).fadeIn(200).dequeue('fx');
    });
  };

  tagSort(array) {
    const sortArrayTags = [...array].sort(function(x, y) {
      x = x.getAttribute("data-three-pos")
      y = y.getAttribute("data-three-pos")
      return (!(x=='1' && y=='1') && x=='1' || (x=='-1' && y=='0'))? 1: -1
    });
    sortArrayTags.forEach( function (e) {
      document.querySelector(this.itemName).parentNode.prepend(e);
    }.bind(this));
  };

  inserMark(string, position, fullLen) {
    return string.slice(0, position) + '<mark>' + string.slice(position, position+fullLen) + '</mark>' + string.slice(position+fullLen);
  };

  searchForMatches(text, textInp) {
    // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
    return !((text.innerText.toLowerCase().search(textInp) == -1) || (textInp == ''));
  }

  search(array, textInp) {
    // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();

    array.forEach(function(e) {
      let valuebtn = e.getAttribute("data-three-pos");
  
      if (this.searchForMatches(e, textInp)) {
        e.getElementsByTagName('span')[0].innerHTML = this.inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
        this.show(e);
      } else {
        if (valuebtn=='0') {
          this.hide(e);
        };
        e.getElementsByTagName('span')[0].innerHTML = e.innerText;
      };
    }.bind(this));
  };

  start() {
    let arrayitem = document.querySelectorAll(this.itemName);
    // console.log(arrayitem.length)

    document.querySelector(this.itemName).parentNode.addEventListener('click', function(e) {
      if (e.target.closest(this.itemName)) {
        let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
        
        // скрыть кнопку если строка пустая и кнопка пасивна
        if (!this.searchForMatches(e.target.closest(this.itemName), textInp)) {
          if (e.target.closest(this.itemName).getAttribute("data-three-pos") == '0') {
            this.hide(e.target.closest(this.itemName))
          }
        }

        this.tagSort(arrayitem);
      }
    }.bind(this));
    
    document.querySelector(this.inputName).addEventListener('input', function() {
      let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
      this.search(arrayitem, textInp);
    }.bind(this));

    // document.querySelector(this.inputName).addEventListener('focusout', function() {
    //   arrayitem.forEach(function(e) {
    //     e.getElementsByTagName('span')[0].innerHTML = e.innerText;
    //   });
    // });
  };
}

let tagSearch = new Search('.search-input__input', '.tags-list__tag');
tagSearch.start();



