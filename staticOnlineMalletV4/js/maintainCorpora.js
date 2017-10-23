
DEBUG_UI = "";

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function sortFileList(id) {
 
    var idContents = []
 
    $(id + ">span").each(
        function() {
            idContents.push([$(this).attr("textFileName"), $(this).attr("id"), $(this).attr("class"), $(this).html(), $(this).attr("textFileOwner")]);
        }
    );
    
    idContents.sort();
    
    $(id).html("");
    
    for (var a = 0; a < idContents.length; a++) {
        var newHtml = "<span class=\"" + idContents[a][2] + 
                        "\" id=\"" + idContents[a][1] +
                        "\" textFileName=\"" + idContents[a][0] + 
                        "\" textFileOwner=\"" + idContents[a][4] + 
                        "\">" + idContents[a][3] +
                        "</span><br/>";
        $(id).append(newHtml);        
    }
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function handleMaintainCorporaGoButton() {
    
    var inputsAreOkay = true;
    
    var csrftoken = getCookie('csrftoken');
    
    var existingCorpusName = $.trim($("#existingCorpusInput").val());
    var newCorpusName = $.trim($("#newCorpusName").val());
    var notes = $("#notes").val();
    
    if (existingCorpusName > "" && newCorpusName > "") {
        alert("Either select an existing corpus or enter the name of a new one.");
        inputsAreOkay = false;
    }
    
    if (existingCorpusName == "" && newCorpusName == "") {
        alert("Either select an existing corpus or enter the name of a new one.");
        inputsAreOkay = false;
    }
    
    var createNewCorpus = false;
    
    var corpusName = existingCorpusName;
    if (newCorpusName > "") {
        corpusName =  newCorpusName;
        createNewCorpus = true;
    }
    
    if (inputsAreOkay) {
        
        if (createNewCorpus) {
                
            var ajaxForm = new FormData();
            ajaxForm.append("corpusName", corpusName);
            ajaxForm.append("notes", notes);
            ajaxForm.append("csrfmiddlewaretoken", csrftoken);
                
            $.ajax({
                type: "POST",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", csrftoken);
                },
                async: false,
                url: "/onlineMalletV4/createnewcorpus/",
                data: ajaxForm,
                cache: false,
                contentType: false,
                processData: false,
                success: function() {
                    $("#existingCorpusInput").append("<option value=\"" + corpusName + "\" selected>" + corpusName + "</option>");
                },
                error: function() {
                    alert("Corpus creation failed.  Email steve.");
                },
            });
        }
        
        $("#progressDialog").css("display", "block");
        
        var corpusContents = getHtmlSnippet("/onlineMalletV4/getcorpuscontents/?corpusName=" + corpusName);
        var fileList = getHtmlSnippet("/onlineMalletV4/listallfiles/?corpusName=" + corpusName);
        
        $("#corpusHeading").html("Contents of corpus " + corpusName);
        $("#droppableCorpusFiles").html(corpusContents);
        $("#droppableAllFiles").html(fileList);
        
        sortFileList("#droppableCorpusFiles");
        sortFileList("#droppableAllFiles");
        
        $("#fileLists").css("display", "block");
        
        var corpusHeight = $("#droppableCorpusFiles").height();
        var fileListHeight = $("#droppableAllFiles").height();
        var maxHeight = corpusHeight;
        if (fileListHeight > maxHeight) {
            maxHeight = fileListHeight;
        }
        
        $("#progressDialog").css("display", "none");

        $(".fileListEntry").draggable({revert: "invalid"}); 

        $("#droppableCorpusFiles").droppable({
            drop: function( event, ui ) {
                    
                var id = $(ui.draggable).attr("id");
                var classString = $(ui.draggable).attr("class");
                var textFileName = $(ui.draggable).attr("textFileName");
                var textFileOwner = $(ui.draggable).attr("textFileOwner");
                var content = $(ui.draggable).html();
                    
                $("#" + id).next('br').remove();
                $("#" + id).remove();
                
                $("#droppableCorpusFiles").prepend("<span class=\"" + classString + " fileMoved\" id=\"" + id + "\">" + content + "</span><br/>");
                $("#" + id).draggable({ revert: "invalid" }); 
                
                var addResult = getHtmlSnippet("/onlineMalletV4/addtocorpus/?corpusName=" + corpusName + "&textFileName=" + textFileName + "&textFileOwner=" + textFileOwner);
            }
        });
        
        $("#droppableAllFiles").droppable({
            drop: function( event, ui ) {
                    
                var id = $(ui.draggable).attr("id");
                var classString = $(ui.draggable).attr("class");
                var textFileName = $(ui.draggable).attr("textFileName");
                var textFileOwner = $(ui.draggable).attr("textFileOwner");
                var content = $(ui.draggable).html();
                
                $("#" + id).next('br').remove();
                $("#" + id).remove();
                
                $("#droppableAllFiles").prepend("<span class=\"" + classString + " fileMoved\" id=\"" + id + "\">" + content + "</span><br/>");
                $("#" + id).draggable({ revert: "invalid" });
                
                var removeResult = getHtmlSnippet("/onlineMalletV4/removefromcorpus/?corpusName=" + corpusName + "&textFileName=" + textFileName + "&textFileOwner=" + textFileOwner);
            }
        });
    }
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */
