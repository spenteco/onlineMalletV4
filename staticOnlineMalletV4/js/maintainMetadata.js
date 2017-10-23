
/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function disableNewDetail() {

    $(".newMetadataType").each(
        function() {
            var corpusM = $(this).attr('corpusm');
            var metaDataIndex = $(this).attr('corpusmetadataindex');
            disableFileInputs(corpusM, metaDataIndex);
        }
    );
}

function disableFileInputs(corpusM, metaDataIndex) {

    $('.metadataTypeDetail').each(
        function() {
            if ($(this).attr('metadataindex') == metaDataIndex && $(this).attr('corpusm') == corpusM) {
                $(this).attr('disabled', true);   
            }
        }
    );
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function handleNewMetadataType(folderM) {

  var newMetadataType = $('#newMetadataType_' + folderM).val();
  var corpusMetadataIndex = $('#newMetadataType_' + folderM).attr('corpusmetadataindex');
  var corpusM = $('#newMetadataType_' + folderM).attr('corpusM');

  $('#newMetadataType_' + folderM).parent().html('<span class="metadataTypeHeader" corpusmetadataindex="' + corpusMetadataIndex + '" corpusm="' + corpusM + '">' + newMetadataType + '</span>');  

  $('.metadataTypeDetail').each(
      function() {
        if ($(this).attr('metadataindex') == corpusMetadataIndex && $(this).attr('corpusm') == folderM) {
          $(this).attr('disabled', false);   
        }
      }
    );
}

/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function handleMetadataTypeDetail(folderM, fileN, metadataIndex) {
    
    console.log('handleMetadataTypeDetail', folderM, fileN, metadataIndex);

  var fileName = $("#file_" + fileN).html();
  var metadataType = '';
  var metadataValue = '';
  var corpusName = '';

  $('.metadataTypeHeader').each(
    function() {
        if ($(this).attr('corpusmetadataindex') == metadataIndex && $(this).attr('corpusm') == folderM) {
          metadataType = $(this).html();
        }
    }
  );

  $('.metadataTypeDetail').each(
    function() {
        if ($(this).attr('metadataindex') == metadataIndex && $(this).attr('filen') == fileN) {
          metadataValue = $(this).val();
          corpusName = $(this).attr('corpusName');
        }
    }
  );

  $.ajax({url: "/onlineMalletV4/updatemetadata/?data=" + JSON.stringify({'corpusName': corpusName, 'fileName': fileName, 'metadataType': metadataType, 'metadataValue': metadataValue}), async: true});
}
