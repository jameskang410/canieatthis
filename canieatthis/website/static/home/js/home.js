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

//useful for making a 'loading' 
var buttonAsThis;

//main functions
$(document).ready(function() {

    //submit button
    $("#submit-button").button().click(function() {

        buttonAsThis = this;
        $("#submit-button").button('loading');

        //get user input
        var userInput = $("#food-text-box").val();

        //submit user input to django view using AJAX
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
            //visualizeResults() could involve e-mailing which lags
            //button should lose 'loading...' state only AFTER everything (including e-mailing) is complete
            $.get(visualizeResults(response)).done( function() {
                $("#submit-button").button('reset');
            });
        },
        error: function (xhr, textStatus, thrownError){
            console.log("error")
        }

    });
};

//visualize results and conclusion
//involves possibly e-mailing (could cause lag)
function visualizeResults(response) {
    
    //FORMATTING CONCLUSION
    $("#overall-answer").empty();

    var conclusion = response.conclusion;

    if (conclusion === "safe") {
        $("#overall-answer").append('<h3 id="answer-text">Safe to consume!</h3>');
    }
    else if (conclusion === "not safe") {
        $("#overall-answer").append('<h3 id="answer-text">NOT safe to consume!</h3>');
    }
    else {
        $("#overall-answer").append('<h3 id="answer-text">Could not find answer</h3>')
    }

    //FORMATTING RESULTS
    $("#results").empty();

    var hitsArray = response.hits.hits;

    for (var i = 0; i < hitsArray.length; i++) {

        //source text and source
        $("#results").append('<div class=result>');
        $("#results").append('<blockquote><p id="source-text">' + hitsArray[i]._source.text + '</p>' +
        '<footer><a href="' + hitsArray[i]._source.source + '">' + hitsArray[i]._source.source + '</footer></blockquote>');

        //"was this helpful" button - usually shows 2 voting buttons; hidden after voting
        $("#results").append('<div class="helpful" id="helpful-' + hitsArray[i]._id + '"><p><small>Was this helpful?</small>' +
        '<button class="btn btn-xs btn-primary helpful-button" onClick="changeBoost(' + "'" + hitsArray[i]._id + "'" + ', true)">Yes</button>' + 
        '<button class="btn btn-xs btn-primary helpful-button" onClick="changeBoost(' + "'" + hitsArray[i]._id + "'" + ', false)">No</button></p></div>');
        $("#results").append('<div class="helpful" id="helpful-thanks-' + hitsArray[i]._id + '"><p><small>Thanks for your help!</small>');        

        //useful for testing
        // $("#results").append('<p class="id">ID: ' + hitsArray[i]._id + '</p>');
        // $("#results").append('<p class="index">INDEX: ' + hitsArray[i]._index + '</p>');
        // $("#results").append('<p class="score">SCORE: ' + hitsArray[i]._score + '</p>');
        // $("#results").append('<p class="boost"> BOOST: ' + hitsArray[i]._source.boost + '</p>');

        $("#results").append('</div>');
    }
};

//changing boost score based on "was this helpful" input
function changeBoost(id, inc_dec_bool) {
    
    var inc_dec;
    if (inc_dec_bool) {
        inc_dec = "yes";
    }
    else {
        inc_dec = "no";
    }

    var url = 'boost/' + inc_dec + '/' + id; 

    $.ajax({
        url: url,
        data: {
        },
        success: function(response) {
            console.log(response);
        },
        error: function (xhr, textStatus, thrownError){
            console.log("error");
        }
    });

    $("#helpful-" + id).hide();
    $("#helpful-thanks-" + id).show();

};