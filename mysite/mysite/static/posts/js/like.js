function setText(block, update){
    block.textContent = parseInt(block.textContent) + update;

}
// AJAX CALL
document.querySelector('.page').addEventListener('click', function(e) { 
    let currentButton = e.target.closest(".like-btn"); 
    if (currentButton) { 
        let like_url = $(currentButton).attr('data-href');
        let like_count = currentButton.querySelector(".like-cont__likes-number");
//        let view_count = e.target.closest('.cover-item-gallery__LC').querySelector('.gallery__numcom');
        $.ajax({ 
            type: "GET", 
            url: like_url, 
            data: {'operation':'like_submit','csrfmiddlewaretoken': '{{ csrf_token }}'}, 
            dataType: "json", 
            success: function(response) { 
                selector = document.getElementsByName(response.content_id);

                console.log(response)

                if (response.liked != null){
                    if (response.liked){
                        currentButton.classList.add('_active');
                        setText(like_count, 1);
                    } else if (!response.liked){
                        currentButton.classList.remove('_active');
                        setText(like_count, -1);
                    }
                }

//                if (response.add_view) {
//                    setText(view_count, 1);
//                }
            } 
        })
    } 
})
