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
    if (!e.target.closest('.search-container__wrapper')) {
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
  btn('.search-button','.search-input__close', '.search-container');
  setTimeout(() => document.querySelector('.search-input__input').focus(), 100);
  // document.querySelector('.search-input__input').focus()
});


// желательно чтобы кнопки имели общий родитель который имеет селетор или id
function threeBtn(btnName) {
  let parentBtn = document.querySelector(btnName).parentNode;
  // let arrayBtn = document.querySelectorAll(btnName)

  parentBtn.addEventListener('click', function(e) {
    let tar = e.target.closest(btnName);
    if (tar) {
      let valueinp = tar.querySelector('.three-pos-inp').value;
      if (valueinp == '0') {
        tar.classList.add('_enabled');
        tar.querySelector('.three-pos-inp').value = '1';
        
      } else if (valueinp == '1') {
        tar.classList.add('_disabled');
        tar.classList.remove('_enabled');
        tar.querySelector('.three-pos-inp').value = '-1';
        
      } else if (valueinp == '-1') {
        tar.classList.remove('_disabled');
        tar.querySelector('.three-pos-inp').value = '0';
      }
    };
  });
};
threeBtn('.tags-list__tag');


class tagSearch {
  constructor(inputName, itemName) {
    this.inputName = inputName;
    this.itemName = itemName;
  };

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
      x = x.querySelector('.three-pos-inp').value;
      y = y.querySelector('.three-pos-inp').value;
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
  };

  search(array, textInp) {
    // let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
    array.forEach(function(e) {
      let valueinp = e.querySelector('.three-pos-inp').value;
      if (this.searchForMatches(e, textInp)) {
        e.getElementsByTagName('span')[0].innerHTML = this.inserMark(e.innerText, e.innerText.toLowerCase().search(textInp), textInp.length);
        this.show(e);
      } else {
        if (valueinp=='0') {
          this.hide(e);
        };
        e.getElementsByTagName('span')[0].innerHTML = e.innerText;
      };
    }.bind(this));
  };

  start() {
    let arrayitem = document.querySelectorAll(this.itemName);
    document.querySelector(this.inputName).focus();
    // console.log(arrayitem.length)

    document.querySelector(this.itemName).parentNode.addEventListener('click', function(e) {
      let clickBtn = e.target.closest(this.itemName)
      if (clickBtn) {
        setTimeout(() => clickBtn.querySelector('.three-pos-inp').focus(), 100);
        let textInp = document.querySelector(this.inputName).value.trim().toLowerCase();
        
        // скрыть кнопку если строка пустая и кнопка пасивна
        if (!this.searchForMatches(clickBtn, textInp)) {
          if (clickBtn.querySelector('.three-pos-inp').value == '0') {
            this.hide(clickBtn);
          };
        };

        this.tagSort(arrayitem);
      };
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

  tagSort(arrayitem);
};


const search = new tagSearch('.search-input__input', '.tags-list__tag');
search.start();

document.querySelectorAll('.tags-list__tag').forEach(function(e) {
  console.log(e.querySelector('.three-pos-inp'))
});