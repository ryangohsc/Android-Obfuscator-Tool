/**
 *  On successful page load
 */
$(document).ready(
    cleanup()
)

/**
 *  Folder and workspace cleanup actions
 *  @REQUEST    - GET
 *  @URL        - /cleanup
 *  @return     - HTTP 200
 */
function cleanup(){
    $.ajax({
        url: '/cleanup',
        type: 'GET',
        success: function(response) {
        },
        error: function() {
        }
    });
}

/**
 *  HTML "Obfuscate" button is clicked
 *  @REQUEST    - POST
 *  @URL        - /upload
 *  @data       - User selected .apk file
 *  @return     - HTTP 200
 *  @OnSuccess  - Visual Changes to HTML
 *              - Trigger apkExtract()
 */
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
            //
            // Visual updates
            $("#uploadStatus").load("../static/html/alert_OK.html");
            document.getElementById("obfuscateButton").setAttribute("disabled", "")
            document.getElementById("apkExtractSpinnerHeader").removeAttribute("hidden");
            document.getElementById("apkExtractSpinner").removeAttribute("hidden");
            //
            // Next step / action
            apkExtract()
        },
        error: function() {
            $("#uploadStatus").load("../static/html/alert_fail.html");
        }
    });
}

/**
 * Upon successful upload()
 * Proceed with APK Extraction
 * @REQUEST     - GET
 * @URL         - /extractapk
 * @return      - Extraction log of apktool
 * @OnSuccess   - Visual Changes to HTML
 *              - Trigger locateSmali()
 */
function apkExtract(){
    $.ajax({
        url: '/extractapk',
        type: 'GET',
        success: function(response) {
            //
            // Visual updates
            document.getElementById("apkExtractWrapper").removeAttribute("hidden");
            document.getElementById("apkExtractHeader").removeAttribute("hidden");
            document.getElementById("apkExtractSpinnerWrapper").remove();
            // Display output
            document.getElementById("apkExtractStatus").innerHTML=response;
            //
            // Next step / action
            locateSmali()
        },
        error: function() {
        }
    });
}

/**
 * Upon successful apkExtract()
 * Proceed with locating .smali files
 * @REQUEST     - GET
 * @URL         - /locatesmali
 * @return      - Location of all .smali files in a .txt file
 * @OnSuccess   - Visual Changes to HTML
 */
function locateSmali(){
    $.ajax({
        url: '/locatesmali',
        type: 'GET',
        success: function(response) {
            //
            // Visual updates
            document.getElementById("smaliFilesFoundWrapper").removeAttribute("hidden");
            document.getElementById("smaliFilesFoundHeader").removeAttribute("hidden");
            // Display output
            $("#smaliFilesFoundCount").html(response)
            $("#smaliFilesFoundList").load("../static/tmp/smali.txt");
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

// function fileCompare(){
//     $.ajax({
//         url: '/comparefile',
//         type: 'POST',
//         success: function(response) {
//             document.getElementById("fileCompareHeader").removeAttribute("hidden");
//             $("#fileCompareZone").load("../static/tmp/output.html");
//         },
//         error: function() {
//         }
//     });
// }