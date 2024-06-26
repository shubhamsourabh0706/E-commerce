$('#slider1, #slider2, #slider3',).owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1];
    
    
    $.ajax({
        type: "GET",
        url: "/plusCart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
            
        },
        // error: function(xhr, status, error) {
        //     console.error(xhr.responseText);
        //     // Handle error, if needed
        // }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString()
    var eml = this.parentNode.children[1]
    $.ajax({
        type : 'GET',
        url : '/minusCart',
        data : {
            prod_id : id
        },
        success : function(data){
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
            

        }
    })
})
$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString()
    var eml = this

    $.ajax({
        type : 'GET',
        url : '/removeCart',
        data: {
            prod_id : id
        },
        success : function(data){
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            

        }
    })
})
