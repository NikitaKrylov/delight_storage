function setText(block, update){
    block.textContent = parseInt(block.textContent) + update
}
// AJAX CALL
$('.cover-item-gallery__likes').click(function(event){
    event.preventDefault()
    var this_ = $(this)
    var like_url = this_.attr('data-href')
    var child = this_.children().children()[0]
    $.ajax({
             type: "GET",
             url: like_url,
             data: {'operation':'like_submit','csrfmiddlewaretoken': '{{ csrf_token }}'},
             dataType: "json",
             success: function(response) {
              selector = document.getElementsByName(response.content_id);
                    if(response.liked==true){
                        setText(child, 1)
                    }
                    else if(response.liked==false){
                      setText(child, -1)
                    }


              }

        });

  })