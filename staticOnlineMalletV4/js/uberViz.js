
/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

SAVE_LAST_TOPIC = '';
LAST_Z_INDEX = 1;

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */


$(document).ready(
    function() {

        console.log('changed version');

        //
        //  GET THE TABLE CONTENTS
        //

        var fileName = $('#uberVizFileName').html();

        var responseText = $.ajax({url: '/onlineMalletV4/getresultsfile/?fileName=' + fileName, async: false}).responseText;

        $('#uberVizContainer').html(responseText);

        //
        //  SET UP TABLE SORTER
        //

        $("#uberVizTable>tbody>tr>td").each(
            function() {
                if ($(this).attr("celltype") == "fileName") {
                    var fileName = $(this).html();
                    $(this).html('<a href="javascript:handleFileClick(\'' + fileName + '\');">' + fileName + '</a>');
                }
                if ($(this).attr("celltype") == "topicPct") {
                    var cellValue = Number($(this).attr("cellvalue")).toFixed(2);
                    $(this).attr("cellvalue", cellValue);
                }
            }
        );

        $('#uberVizTable').tablesorter({sortRestart: true, theme: 'blue'}); 

        $(".header").css('padding-right', '1em');

        //
        //  INITIALIZE INPUT CONTROLS
        //

        $("input[name=numberFormat][value='roundedValues']").prop('checked', true);
        switchTdValues('roundedValues');

        $("input[name=numberFormat]").change(
            function() {
                switchTdValues($(this).val());
            }
        );

        $("input[name=topicNumberSelector]").change(
            function() {
                highlightTopic($(this).val());
            }
        );
    }
);

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function switchTdValues(desiredValue) {

    $("td").each(
        function() {
            var cellType = $(this).attr("celltype");
            if (cellType == "topicPct") {
                    
                $(this).css("background-color", "white");
                $(this).css("color", "black");
                $(this).css("font-weight", "normal");

                if (desiredValue == "numberOfChunks") {
                    $(this).html($(this).attr("chunkcount"));
                }

                if (desiredValue == "roundedValues") {
                    $(this).html($(this).attr("cellvalue")); 
                }

                if (desiredValue == "roundedHideZero") {
                    if ($(this).attr("cellvalue") == '0.00') {
                        $(this).html(''); 
                    }
                    else {
                        $(this).html($(this).attr("cellvalue")); 
                    }
                }
            }
        }
    );
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function handleTopicClick(topicClicked) {

    thisTop = $("#topicWordsLink_" + topicClicked).position().top;
    thisLeft = $("#topicWordsLink_" + topicClicked).position().left;
    
    $("#topicWordsDisplay").html("<div><span class=\"topicWordDisplayHeader\">Topic " + topicClicked + "</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + 
                                                    "<a href=\"javascript:closeTopicWords();\">close</a>" + "</div>" +
                                                    "<p>" + $("#topicWords_" + topicClicked).html() + "</p>");
    $("#topicWordsDisplay").css("display", "block");
    $("#topicWordsDisplay").css("position", "absolute");
    $("#topicWordsDisplay").css("top", (thisTop - 20) + "px");
    $("#topicWordsDisplay").css("left", (thisLeft - 20) + "px");

    LAST_Z_INDEX = LAST_Z_INDEX + 1;
    $("#topicWordsDisplay").css("z-index", LAST_Z_INDEX);
}

function closeTopicWords() {
    $("#topicWordsDisplay").css("display", "none");    
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function handleFileClick(fileName) {
        
    $("#progressDialog").css("display", "block");

    $("#topicSelector").css("display", "inline");

    $("input[name=topicNumberSelector]").each(
        function() {
            $(this).prop("checked", false);

        }
    );

    $('#highlightTextDisplay').html('');

    var fileNameString = $("#fileLocation").html() + fileName.replace('.txt', '.html');

    var responseText = $.ajax({url: '/onlineMalletV4/getresultsfile/?fileName=' + fileNameString, async: false}).responseText;

    $('#highlightTextDisplay').html(responseText);

    var thisTop = -1;
    var thisLeft = -1;

    $("#uberVizTable>tbody>tr>td").each(
        function() {
            if ($(this).attr("cellvalue") == fileName) {

                thisTop = $(this).position().top;
                thisLeft = $(this).position().left;
            }
        }
    );

    $("#textDisplayArea").css("display", "block");
    $("#textDisplayArea").css("position", "absolute");
    $("#textDisplayArea").css("top", (thisTop) + "px");
    $("#textDisplayArea").css("left", (thisLeft) + "px");

    LAST_Z_INDEX = LAST_Z_INDEX + 1;
    $("#textDisplayArea").css("z-index", LAST_Z_INDEX);

    $("#progressDialog").css("display", "none");
}

function closeTextDisplay() {
    $("#textDisplayArea").css("display", "none");
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function highlightTopic(topic) {
        
    $("#progressDialog").css("display", "block");

    if (SAVE_LAST_TOPIC > '') {    
        $(".topic_" + SAVE_LAST_TOPIC).css("color", "#000000");
        $(".topic_" + SAVE_LAST_TOPIC).css("font-weight", "normal");
    }

    $(".topic_" + topic).css("color", "#FF0000");
    $(".topic_" + topic).css("font-weight", "bold");

    SAVE_LAST_TOPIC = topic;

    $("#progressDialog").css("display", "none");
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

