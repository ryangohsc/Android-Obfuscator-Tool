$(document).ready(function(){
    $.ajax({
        url: '/cleanup',
        type: 'POST',
        success: function(response) {
        },
        error: function() {
        }
    });
})

function upload(){
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);
    $.ajax({
        url: '/upload',
        data: formData,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function() {
            $("#uploadStatus").load("../static/html/alert_OK.html");
            fileRead()
        },
        error: function() {
            $("#uploadStatus").load("../static/html/alert_fail.html");
        }
    });
}

function fileRead(){
    $.ajax({
        url: '/readfile',
        type: 'POST',
        success: function(response) {
            document.getElementById("initialCodeHeader").removeAttribute("hidden");
            document.getElementById("initialCode").innerHTML=response;
            smaliModify();
        },
        error: function() {
        }
    });
}

function smaliModify(){
    $.ajax({
        url: '/modifysmali',
        type: 'POST',
        success: function(response) {
            fileCompare();
        },
        error: function() {
        }
    });
}

function fileCompare(){
    $.ajax({
        url: '/comparefile',
        type: 'POST',
        success: function(response) {
            document.getElementById("fileCompareHeader").removeAttribute("hidden");
            $("#fileCompareZone").load("../static/tmp/output.html");
        },
        error: function() {
        }
    });
}