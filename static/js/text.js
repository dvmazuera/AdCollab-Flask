function completed(result){
    if (result["info_message"] == "True"){
        number ='(' + result["number"].slice(0, 3) + ')' + result["number"].slice(3, 6) + '-' + result["number"].slice(6,)
        alert("Message will be sent to " + number +" before street cleaning");
    }else{
        $(location).attr('href', '/user_info')
    }
}



function sendText(evt){
    evt.preventDefault();


    var cleaningtime = $('#cleaningtime').val();
    var message = {
        "cleaningtime": cleaningtime
    };

    $.post('/send_text.json', message, completed);
}


$('#send_text').on('submit', sendText);