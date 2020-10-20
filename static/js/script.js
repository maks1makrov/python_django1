function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$("document").ready(function(){

    /*$('html.auth span.comment_like').mouseenter(function(){
        $(this).addClass('blue')
    });
    $('html.auth span.comment_like').mouseleave(function(){
        $(this).removeClass('blue')
    });*/
    $('html.auth span.comment_like').on("click", function(){
        let cl_id = $(this).attr("id");
        let object_comment = this
        $.ajax({
            url:'/shop/add_like_ajax',
            data: {"cl_id": cl_id, 'csrfmiddlewaretoken': csrftoken},
            method: "post",
            success: function(data){
                $(object_comment).html(` likes: ${data["count_like"]}` )
                if(data["flag"]){
                    $(object_comment).attr("class", "comment_like fa fa-star checked")
                    $(object_comment).next().append(`<span class="col">${data["user"]}</span>`)
                }else{
                    $(object_comment).attr("class", "comment_like fa")
                    for(var i=0; i < $(object_comment).next().children().length; i++){
                        item = $(object_comment).next().children()[i];
                        if($(item).html() == data["user"]){
                            item.remove();
                            break
                        }
                    }
                }
                console.log(data)
            }
        });
    console.log('hello click')
    });

    $('span.book_rate').on("click", function(){
        let arr = $(this).attr("id").split("-");
        let book_id = arr[1];
        let book_rate = arr[2];
        let obj = this
        $.ajax({
            url:'/shop/add_book_rate_ajax/',
            data: {"book_id": book_id,"book_rate": book_rate, 'csrfmiddlewaretoken': csrftoken},
            method: "post",
            success: function(data){
                let rate = $(obj).parent()
                let children = $(rate).children()
                let text = children[0]
                $(text).html(`Rate: ${data['cached_rate']}`);
                for(let i=1; i <= 10; i++){
                    if(data["rate"] >= i-1){
                        $(children[i]).attr('class', 'book_rate fa fa-star checked')
                    }else{
                        $(children[i]).attr('class', 'book_rate fa fa-star')
                    }

                }
                if(data['flag']){
                    $(rate).append(`<span>${data['user']}</span>`)
                }
            console.log(data, text)
            }


        })
    });

    $("button.delete_comment").on("click", function () {
        let id = $(this).attr('id').split('-')[1];
        let obj = this;
        console.log(id)
        $.ajax({
            url: `/shop/delete_comment_ajax/${id}`,
            method: 'delete',
            headers: {"X-CSRFToken": csrftoken},
            success: function (data) {
                $(obj).parent().remove();
                console.log(data)
            }
        })
    });
});
//    $("a.add_new_book").on(click, function(){
//        let arr = $(this).parent().children()
//        let title = $(arr[0]).val();
//        let text = $(arr[1]).val();
//        let genre = $(arr[4]).val();
//        $('modal').modal('toggle')
//        let close = $(this).parent().parent().children()[1]
//        $.ajax({
//        url:'/shop/add_new_book_ajax',
//            data: {
//            'csrfmiddlewaretoken': csrftoken,
//            'title': title,
//            'text': text,
//            "genre": genre,
//
//            },
//            method: "post",
//            success: function(data)
//
//        )}
//        console.log(title, text, selector)
//    }
//
//    )}
//
//


//});


//$('document').ready(function(){
//    $("span.rate_like").on('click', function({
//        let cr_id = $(this).attr('id');
//        console.log(cr_id)
//    }));
//});

//
//    $('document').ready(function(){
//        $("span.rate_like").on('click', function({
//        console.log("hello");
//        }));
//    });


//$("document").ready(function(){
//    $('span.rate_like').on("click", function(){
//        let r_id = $(this).attr("id");
//        $.ajax({
//            url:'/shop/add_rate_ajax',
//            data: {"r_id": r_id, 'csrfmiddlewaretoken': csrftoken},
//            method: "post",
//            success: function(data){
//                $(object_comment).html(` likes: ${data["count_like"]}` )
//
//    console.log('hello'+cl_id)
//    });
//
//});
