/* ---------------------------------------------------------------------
   
------------------------------------------------------------------------ */

function collapseFolders() {
    $('.myFolderLi > ul').css('display', 'none');
}
        
function myFolderLiClicked(id) {
    if ($("#" + id).css("display") == "none") {
        $("#" + id).css("display", "block");
    }
    else {
        $("#" + id).css("display", "none");
    }
}