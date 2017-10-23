
SAVED_EVENT = '';

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

$(document).ready(
    function() {

        //
        //  GET THE TABLE CONTENTS
        //

        var fileName = $('#heatMapFileName').html();

        var responseText = $.ajax({url: '/onlineMalletV4/getresultsfile/?fileName=' + fileName, async: false}).responseText;

        $('#heatmapContainer').html(responseText);

        $(".heatmapCell").mouseover(
            function(e) {

                SAVED_EVENT = e;

                var x = e.pageX + 10;
                var y = e.pageY + 10;

                $("#heatmapTooltip").css("display", "inline");
                $("#heatmapTooltip").css("position", "absolute");
                $("#heatmapTooltip").css("top", y + "px");
                $("#heatmapTooltip").css("left", x + "px");
                $("#heatmapTooltip").html($(this).attr("textA") + "<br/>" + $(this).attr("textB") + "<br/>distance " + $(this).attr("distance") + "<br/>deviation " + $(this).attr("deviation"));
            }
        );

        $(".heatmapCell").mouseout(
            function(e) {
                $("#heatmapTooltip").css("display", "none");
            }
        );
    }
);

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

