
/* ---------------------------------------------------------------------
   COMMON FUNCTIONS
------------------------------------------------------------------------ */

function getHtmlSnippet(requestUrl) {

    var responseText = $.ajax({url: requestUrl, async: false}).responseText;
    
    return responseText;
}

function getJsonObjext(requestUrl) {

    var responseText = $.ajax({url: requestUrl, async: false}).responseText;
    
    var unescapedResponseText = responseText.replace(/&quot;/g, '"');

    var responseObject = eval("(" + unescapedResponseText + ")");
    
    return responseObject;
}

function toggleSpanDisplay(id) {
    
    if ($("#" +id).css("display") == "none") {
        $("#" +id).css("display", "block");
    }
    else {
        $("#" +id).css("display", "none");
    }
}

/* ---------------------------------------------------------------------
    COOKIE HANDLING    
------------------------------------------------------------------------ */

function keys(obj) {
    var keys = [];

    for(var key in obj) {
        if(obj.hasOwnProperty(key)) {
            keys.push(key);
        }
    }

    return keys;
}

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

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */
