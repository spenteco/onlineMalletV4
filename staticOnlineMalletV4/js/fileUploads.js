
/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

MYFILEGIZMO = {
    "files": {},
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */

function removeFile(fileName) {

    console.log("removeFile", fileName);

    $(".fileUploadList").each(
        function() {
            if ($(this).attr("filename") == fileName) {
                $(this).remove();
            }
        }
    );
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */

function buildFileList() {
                
    $("#fileUploadList").html("");
    
    var fileNames = keys(MYFILEGIZMO["files"]).sort();
    
    for (var a = 0; a < fileNames.length; a++) {
        
        var htmlLine = "<div class=\"fileUploadList\" id=\"fileUploadList_" + a + "\" fileName=\"" + fileNames[a] + "\" index=\"" + a + "\">" + 
                            "<span class=\"fileListFileName\">" +  fileNames[a] + "</span>" +
                            "<span class=\"fileListFileType\">" +  MYFILEGIZMO["files"][fileNames[a]]["fileType"] + "</span>" +
                            "<span class=\"fileListFileSize\">" +  MYFILEGIZMO["files"][fileNames[a]]["fileSize"] + "</span>" +
                            "<span><button class=\"fileButton\" type=\"button\" id=\"removeButton_" + a + "\" onclick=\"javascript:removeFile('" + fileNames[a] + "');\">Remove</button></span>" +
                            "<span  class=\"fileListStatus\" id=\"fileUploadStatus_" + a + "\"></span>" +
                            "</div>";
                            
        $("#fileUploadList").append(htmlLine);
    }
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */

function saveSelectedFiles(event) {
    
    var files = event.target.files;
    
    for (var a = 0; a < files.length; a++) {
        
        var fileExists = false;
        
        $(".existingFile").each(
            function() {
                
                if ($(this).attr("textFileName") == files[a].name && $(this).attr("textFileOwner") == $("#fileUploadUser").html()) {
                    fileExists = true; 
                }
                
                if ($(this).attr("stopwordFileName") == files[a].name && $(this).attr("stopwordFileOwner") == $("#fileUploadUser").html()) {
                    fileExists = true; 
                }
            }
        );
        
        console.log('files[a]', files[a]);

        if (files[a].type == 'text/plain' || files[a].type == 'application/zip' || files[a].type == 'application/gzip') {

            var okayToOverwrite = true;
            
            //if (fileExists == true) {
            //    okayToOverwrite = confirm("File " + files[a].name + " exists.  Click OK to overwrite");
            //}
            
            if (fileExists == false || okayToOverwrite == true) {
            
                MYFILEGIZMO["files"][files[a].name] = {"fileObject": files[a], "fileType": files[a].type, "fileExists": fileExists, "fileSize": files[a].size, "fileUploaded": false};
            }
        }
        else {
            alert("Sorry, but it isn't possible to upload " + files[a].name + ".\n\nWe accept only plain text files (type text/plain) or zip files (types application/zip or application/gzip).\n\nYour file " + files[a].name + " is type " + files[a].type + ".");
        }
    }
    
    buildFileList();
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */

function handleCorpusUploads() {
    
    var inputsAreOkay = true;
    
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
    
    var corpusName = existingCorpusName;
    if (newCorpusName > "") {
        corpusName =  newCorpusName;
    }
    
    if (inputsAreOkay) {
		
		var files = $(".fileUploadList");
		
		var a = 0;
		
		function file_uploadLoop_b() {
			
			var d = new Date().getTime();
            
			var fileName = $(files[a]).attr("fileName");
			var index = $(files[a]).attr("index");
			var csrftoken = getCookie('csrftoken');
			
			//console.log('looping file_uploadLoop_b a', a, 'd', d, fileName);
			
			var ajaxForm = new FormData();
			ajaxForm.append("corpusName", corpusName);
			ajaxForm.append("notes", notes);
			ajaxForm.append("fileExists", MYFILEGIZMO["files"][fileName]["fileExists"]);
			ajaxForm.append("uploadedFile", MYFILEGIZMO["files"][fileName]["fileObject"]);
			ajaxForm.append("csrfmiddlewaretoken", csrftoken)
			
			$.ajax({
				type: "POST",
				beforeSend: function (request) {
					request.setRequestHeader("X-File-Name", fileName);
					request.setRequestHeader("X-File-Size", MYFILEGIZMO["files"][fileName]["fileSize"]);
					request.setRequestHeader("X-File-Type", MYFILEGIZMO["files"][fileName]["fileType"]);
					request.setRequestHeader("X-CSRFToken", csrftoken);
				},
				async: false,
				url: "/onlineMalletV4/uploadcorpusfiles/",
				data: ajaxForm,
				cache: false,
				contentType: false,
				processData: false,
				success: function() {
					$("#fileUploadStatus_" + index).html("Uploaded"); 
					$("#removeButton_" + index).attr("disabled", "disabled");
				},
				error: function() {
					$("#fileUploadStatus_" + index).html("Failed"); 
				},
			});
			
			setTimeout(
				function() {
					a = a + 1;
					if (a < files.length) {
						file_uploadLoop_a(); 
					} 
				}, 
				500
			);
		};
		
		function file_uploadLoop_a() {
			
			var d = new Date().getTime();
            
			var fileName = $(files[a]).attr("fileName");
			var index = $(files[a]).attr("index");
			var csrftoken = getCookie('csrftoken');
			
			//console.log('looping file_uploadLoop_a a', a, 'd', d, fileName);
			
			$("#fileUploadStatus_" + index).html("Uploading");
			
			setTimeout(
				function() {
					file_uploadLoop_b(); 
				}, 
				500
			);
		}
		
		file_uploadLoop_a();
	}
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */

function handleStopwordUploads() {
    
    console.log('handleStopwordUploads');
    
    var inputsAreOkay = true;
    
    if (inputsAreOkay) {
    
        $(".fileUploadList").each(
            function() {
            
                var fileName = $(this).attr("fileName");
                var index = $(this).attr("index");
                var csrftoken = getCookie('csrftoken');
                
                $("#fileUploadStatus_" + index).html("Uploading");
                
                var ajaxForm = new FormData();
                ajaxForm.append("descriptiveName", $("#descriptiveName").val());
                ajaxForm.append("notes", $("#notes").val());
                ajaxForm.append("fileExists", MYFILEGIZMO["files"][fileName]["fileExists"]);
                ajaxForm.append("uploadedFile", MYFILEGIZMO["files"][fileName]["fileObject"]);
                ajaxForm.append("csrfmiddlewaretoken", csrftoken)
                
                console.log('posting', 'csrftoken', csrftoken);
                
                $.ajax({
                    type: "POST",
                    beforeSend: function (request) {
                        request.setRequestHeader("X-File-Name", fileName);
                        request.setRequestHeader("X-File-Size", MYFILEGIZMO["files"][fileName]["fileSize"]);
                        request.setRequestHeader("X-File-Type", MYFILEGIZMO["files"][fileName]["fileType"]);
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    async: false,
                    url: "/onlineMalletV4/uploadstopwords/",
                    data: ajaxForm,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function() {
                        $("#fileUploadStatus_" + index).html("Uploaded"); 
                        $("#removeButton_" + index).attr("disabled", "disabled");
                    },
                    error: function() {
                        $("#fileUploadStatus_" + index).html("Failed"); 
                    },
                });
                
            }
        );
    }
}

/* ---------------------------------------------------------------------
    
------------------------------------------------------------------------ */

$(document).ready(
    function() {
        
        $("#fileSelector").change(
            function(event) {
                saveSelectedFiles(event);
            }
        );
        
        $("#fileSubmitCorpus").click(
            function() {
                handleCorpusUploads();
            }
        );
        
        $("#fileSubmitStopwords").click(
            function() {
                handleStopwordUploads();
            }
        );
        
        $("#fileReset").click(
            function() {
                MYFILEGIZMO["files"] = {};
                $("#fileUploadList").html("");
            }
        );
    }
);
