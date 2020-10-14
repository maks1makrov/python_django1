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
    $('span.comment_like').on("click", function(){
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

});


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
