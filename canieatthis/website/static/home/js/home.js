//dealing with CSRF
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//connecting submit button
$(function() {
    $("#submit-button").button().click(function() {
        //get user input
        var userInput = $("#food-text-box").val();

        //submit user input to django view
        submitQuery(userInput);

    });
});

//ajax - connect user input to django view
function submitQuery(food) {
    $.ajax({
        type: "POST",
        data: {
            food: food,
        },
        success: function(response) {
            console.log(response);
        },
        error: function (xhr, textStatus, thrownError){
            console.log("error")
        }

    })
};