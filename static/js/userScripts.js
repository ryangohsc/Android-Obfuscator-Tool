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
            // $("#uploadStatus").load("../static/html/alert_OK.html");
            document.getElementById("obfuscateButton").setAttribute("disabled", "")
            document.getElementById("apkExtractSpinnerHeader").removeAttribute("hidden");
            document.getElementById("apkExtractSpinner").removeAttribute("hidden");
            //
            // Next step / action
            apkExtract()
        },
        error: function() {
            // $("#uploadStatus").load("../static/html/alert_fail.html");
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
 *              - Trigger obfuscate()
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
            //
            // Next step / action
            obfuscate()
        },
        error: function() {
        }
    });
}

/**
 * Upon successful locateSmali()
 * Proceed with running obfuscating actions
 * @REQUEST     - GET
 * @URL         - /obfuscate
 * @return      - HTTP 200
 * @OnSuccess   - Trigger fileCompare()
 */
function obfuscate(){
    $.ajax({
        url: '/obfuscate',
        type: 'GET',
        success: function(response) {
            //
            // Next step / action
            fileCompare()
        },
        error: function() {
        }
    });
}

/**
 * Upon successful obfuscate()
 * Proceed with running comparing files in the background
 * @REQUEST     - GET
 * @URL         - /comparefile
 * @return      - HTTP 200
 * @OnSuccess   - Trigger fileCompareLoad()
 */
function fileCompare(){
    $.ajax({
        url: '/comparefile',
        type: 'POST',
        success: function(response) {
            //
            // Next step / action
            fileCompareLoad()
        },
        error: function() {
        }
    });
}

/**
 * Upon successful fileCompare()
 * Proceed with generating and displaying DIFF files
 * @REQUEST     - GET
 * @URL         - /comparefileload
 * @return      - File compare HTML data
 * @OnSuccess   - Load visual response
 */
function fileCompareLoad(){
    $.ajax({
        url: '/comparefileload',
        type: 'POST',
        success: function(response) {
            //
            // Display output
            $("#fileCompareParent").append(response.data);
            //
            // Next step / action
            recompile_apk()
        },
        error: function() {
        }
    });
}

/**
 * Upon successful recompile_apk()
 * Proceed with signing the generated APK
 * @REQUEST     - GET
 * @URL         - /recompileapk
 * @return      - HTTP 200
 * @OnSuccess   - signapk()
 */
function recompile_apk(){
    $.ajax({
        url: '/recompileapk',
        type: 'GET',
        success: function(response) {
            // Next step / action
            // signapk()
        },
        error: function() {
        }
    });
}
