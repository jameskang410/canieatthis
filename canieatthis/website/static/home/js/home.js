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

//main functions
$(document).ready(function() {
    
    //set focus on textbox
    $("#food-text-box").focus();

    //submit button
    $("#submit-button").button().click(function() {

        $("#submit-button").button('loading');

        //get user input
        var userInput = $("#food-text-box").val();

        //making sure input isn't empty string
        if (userInput) {
            //submit user input to django view using AJAX
            submitQuery(userInput);
        }
        else {
            $("#submit-button").button('reset');
        }

    });

    //if enter is pressed on search box, submit button is clicked
    $("#food-text-box").keypress(function (e) {
        var key = e.which;

        //if enter
        if (key == 13) {
            $("#submit-button").click();
        }
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
            $("#submit-button").button('reset');
            $("#overall-answer").empty();
            $("#overall-answer").append('<h1 id="answer-text">Try again!</h1>')
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
        $("#overall-answer").append('<h1 id="answer-text">Safe to consume!</h1>');
    }
    else if (conclusion === "not safe") {
        $("#overall-answer").append('<h1 id="answer-text">NOT safe to consume!</h1>');
    }
    else {
        $("#overall-answer").append('<h1 id="answer-text">Could not find answer</h1>')
    }

    //FORMATTING RESULTS
    $("#results").empty();
    
    var html = [];

    html.push('<h3>Sources:</h3>');

    var hitsArray = response.hits.hits;

    for (var i = 0; i < hitsArray.length; i++) {

        //source text and source
        html.push('<div class="result">');
        html.push('<blockquote><p id="source-text"><i>"' + hitsArray[i]._source.text + '</i>"</p>' +
        '<footer><a href="' + hitsArray[i]._source.source + '" target="_blank">' + hitsArray[i]._source.source + '</a></footer></blockquote>');

        //"was this helpful" button - usually shows 2 voting buttons; hidden after voting
        html.push('<div class="helpful" id="helpful-' + hitsArray[i]._id + '"><p><small>Was this helpful?</small>' +
        '<span class="helpful-area"><button class="btn btn-xs btn-primary helpful-button" onClick="changeBoost(' + "'" + hitsArray[i]._id + "'" + ', true)">Yes</button></span>' + 
        '<span class="helpful-area"><button class="btn btn-xs btn-primary helpful-button" onClick="changeBoost(' + "'" + hitsArray[i]._id + "'" + ', false)">No</button></p></span></div>');
        html.push('<div class="helpful" id="helpful-thanks-' + hitsArray[i]._id + '" style="display: none;"><p><small>Thanks for your help!</small></div>');        

        //useful for testing
        // html.push('<p class="id">ID: ' + hitsArray[i]._id + '</p>');
        // html.push('<p class="index">INDEX: ' + hitsArray[i]._index + '</p>');
        // html.push('<p class="score">SCORE: ' + hitsArray[i]._score + '</p>');
        // html.push('<p class="boost"> BOOST: ' + hitsArray[i]._source.boost + '</p>');

        html.push('</div>');
    }

    $("#results").append(html.join(''));

    //prob a better way to do this, but maybe not worth time
    //need to move footer from absolute position
    $("#footer-info").css("position", "inherit");
};

//changing boost score based on "was this helpful" input
function changeBoost(e_id, inc_dec_bool) {
    
    var inc_dec;
    if (inc_dec_bool) {
        inc_dec = "yes";
    }
    else {
        inc_dec = "no";
    }

    var url = 'boost/'; 

    $.ajax({
        type: "POST",
        url: url,
        data: {
            e_id : e_id,
            inc_dec_bool : inc_dec
        },
        success: function(response) {
            // console.log(response);
        },
        error: function (xhr, textStatus, thrownError){
            console.log("error");
        }
    });

    $("#helpful-" + e_id).hide();
    $("#helpful-thanks-" + e_id).show();

};