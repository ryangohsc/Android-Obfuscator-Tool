$(document).ready(
    cleanup()
)

function cleanup(){
    $.ajax({
        url: '/cleanup',
        type: 'POST',
        success: function(response) {
        },
        error: function() {
        }
    });
}

function upload(){
    cleanup()
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
            document.getElementById("obfuscateButton").setAttribute("disabled", "")
            document.getElementById("apkExtractSpinnerHeader").removeAttribute("hidden");
            document.getElementById("apkExtractSpinner").removeAttribute("hidden");
            // document.getElementById("apkExtractSpinner").removeAttribute("hidden");
            apkExtract()
        },
        error: function() {
            $("#uploadStatus").load("../static/html/alert_fail.html");
        }
    });
}

function apkExtract(){
    $.ajax({
        url: '/extractapk',
        type: 'POST',
        success: function(response) {
            document.getElementById("apkExtractWrapper").removeAttribute("hidden");
            document.getElementById("apkExtractHeader").removeAttribute("hidden");
            document.getElementById("apkExtractSpinnerWrapper").remove();
            document.getElementById("apkExtractStatus").innerHTML=response;
        },
        error: function() {
        }
    });
}

// function smaliModify(){
//     $.ajax({
//         url: '/modifysmali',
//         type: 'POST',
//         success: function(response) {
//             fileCompare();
//         },
//         error: function() {
//         }
//     });
// }

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