console.log("in booking js")



$('#calc-months').on('click', function(evt){ 
    evt.preventDefault();
    console.log("noticed click")

    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();
    var total_amount = total(start_date, end_date);

    $('#rent-price-result').text(total_amount);

})


function total(start_date, end_date) {

     var calendar = { may17:0, june17:1, july17:2, august17:3, september17:4, october17:5,
                november17:6, december17:7, january18:8, february18:9, march18:10 };
                

    if (start_date in calendar){
        var start_value = calendar[start_date];
    }

    if (end_date in calendar){
        var end_value = calendar[end_date];
    }
   
    var totalMonths = end_value - start_value +1;
    var priceListing = parseInt($('#rent-price-result').data("listing-price"));
    var totalPrice = totalMonths * priceListing;
    // console.log(totalPrice)

    return totalPrice;
}


// $('#un-hide')on('click', function(){
//     console.log("hi")
//     $(this).css("display","show");
// });

// function unhide(){
//     console.log("hi")
//     $('#overlay_image').css("display","block");
// }
  


function startDrag(e) {
                // determine event object
                if (!e) {
                    var e = window.event;
                }
                if(e.preventDefault) e.preventDefault();

                // IE uses srcElement, others use target
                targ = e.target ? e.target : e.srcElement;

                if (targ.className != 'dragme') {return};
                // calculate event X, Y coordinates
                    offsetX = e.clientX;
                    offsetY = e.clientY;

                // assign default values for top and left properties
                if(!targ.style.left) { targ.style.left='0px'};
                if (!targ.style.top) { targ.style.top='0px'};

                // calculate integer values for top and left 
                // properties
                coordX = parseInt(targ.style.left);
                coordY = parseInt(targ.style.top);
                drag = true;

                // move div element
                    document.onmousemove=dragDiv;
                return false;
                
            }
            function dragDiv(e) {
                if (!drag) {return};
                if (!e) { var e= window.event};
                // var targ=e.target?e.target:e.srcElement;
                // move div element
                targ.style.left=coordX+e.clientX-offsetX+'px';
                targ.style.top=coordY+e.clientY-offsetY+'px';
                return false;
            }
            function stopDrag() {
                drag=false;
            }
            window.onload = function() {
                document.onmousedown = startDrag;
                document.onmouseup = stopDrag;
            }











// $('#book_listing').on('click', function(evt){ 
//     evt.preventDefault();
//     console.log("noticed booking click")

//     //open modal window saying... This 

//     var start_date = $('#start_date').val();
//     var end_date = $('#end_date').val();
//     var booking_price = $('#rent-price-result').val();
//     var ad_height = $('#ad-height').val();
//     var ad_width = $('#ad-width').val();

//     $('#rent-price-result').text(total_amount);

// })


// $('#show-ajax').on('click',function(){
//     console.log("Show Ajax Click")



















