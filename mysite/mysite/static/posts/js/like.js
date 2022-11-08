function setText(block, update){
    block.textContent = parseInt(block.textContent) + update
}
// AJAX CALL
$('.like-btn').click(function(event){
    event.preventDefault()
    var like_url = $(this).attr('data-href')
    var child = $(this).children().children()[0]
    $.ajax({
             type: "GET",
             url: like_url,
             data: {'operation':'like_submit','csrfmiddlewaretoken': '{{ csrf_token }}'},
             dataType: "json",
             success: function(response) {
              selector = document.getElementsByName(response.content_id);
                    if (response.liked==true){
                        setText(child, 1)
                    }
                    else if (response.liked==false){
                      setText(child, -1)
                    }
              }
        });
  })