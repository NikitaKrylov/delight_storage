function setText(block, update){
    block.textContent = parseInt(block.textContent) + update
}
// AJAX CALL
document.querySelector('.page').addEventListener('click', function(e) { 
    let currentButton = e.target.closest(".like-btn"); 
    if (currentButton) { 
        var like_url = $(currentButton).attr('data-href') 
        var child = currentButton.querySelector(".like-cont__likes-number") 
        $.ajax({ 
            type: "GET", 
            url: like_url, 
            data: {'operation':'like_submit','csrfmiddlewaretoken': '{{ csrf_token }}'}, 
            dataType: "json", 
            success: function(response) { 
                selector = document.getElementsByName(response.content_id); 
     
                if (response.liked==true){ 
                    currentButton.classList.add('_active'); 
                    setText(child, 1) 
                } else if (response.liked==false){ 
                    currentButton.classList.remove('_active'); 
                    setText(child, -1) 
                } 
            } 
        }); 
    } 
});
