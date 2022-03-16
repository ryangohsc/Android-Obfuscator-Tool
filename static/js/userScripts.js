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
        error: function() {}
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
    formData.append(obfusFunc_dci.value, obfusFunc_dci.checked);
    formData.append(obfusFunc_dmi.value, obfusFunc_dmi.checked);
    formData.append(obfusFunc_uj.value, obfusFunc_uj.checked);
    formData.append(obfusFunc_ab.value, obfusFunc_ab.checked);
    formData.append(obfusFunc_nop.value, obfusFunc_nop.checked);
    formData.append(obfusFunc_method_rename.value, obfusFunc_method_rename.checked);
    formData.append(obfusFunc_variable_rename.value, obfusFunc_variable_rename.checked);
    formData.append(obfusFunc_ro.value, obfusFunc_ro.checked);
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
            document.getElementById("fileInput").setAttribute("disabled", "")
            document.getElementById("obfuscateButton").setAttribute("disabled", "")
            document.getElementById("obfusFunc_dmi").setAttribute("disabled", "")
            document.getElementById("obfusFunc_uj").setAttribute("disabled", "")
            document.getElementById("obfusFunc_ab").setAttribute("disabled", "")
            document.getElementById("obfusFunc_nop").setAttribute("disabled", "")
            document.getElementById("obfusFunc_method_rename").setAttribute("disabled", "")
            document.getElementById("obfusFunc_variable_rename").setAttribute("disabled", "")
            document.getElementById("obfusFunc_ro").setAttribute("disabled", "")
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
            // document.getElementById("apkExtractWrapper").removeAttribute("hidden");
            // document.getElementById("apkExtractHeader").removeAttribute("hidden");
            document.getElementById("apkExtractSpinnerWrapper").remove();
            // Display output
            // document.getElementById("apkExtractStatus").innerHTML=response;
            //
            // Next step / action
            locateSmali()
        },
        error: function() {}
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
            document.getElementById("smaliFilesFoundBeforeWrapper").removeAttribute("hidden");
            document.getElementById("smaliFilesFoundBeforeHeader").removeAttribute("hidden");
            document.getElementById("fileCompareSpinnerHeader").removeAttribute("hidden");
            document.getElementById("fileCompareSpinner").removeAttribute("hidden");
            // Display output
            $("#smaliFilesFoundBeforeCount").html(response)
            $("#smaliFilesFoundBeforeList").load("../static/tmp/smali.txt");
            //
            // Next step / action
            obfuscate()
        },
        error: function() {}
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
        error: function() {}
    });
}

/**
 * Upon successful obfuscate()
 * Proceed with running comparing files in the background to generate HTML files
 * @REQUEST     - GET
 * @URL         - /comparefile
 * @return      - HTTP 200
 * @OnSuccess   - Load #fileSelectList with options
 *              - Trigger recompile_apk()
 */
function fileCompare(){
    $.ajax({
        url: '/comparefile',
        type: 'POST',
        success: function(response) {
            //
            // Visual updates
            for(key in response){
                if (key != 0){
                    var opt = document.createElement("option")
                    opt.value = key
                    opt.innerHTML = response[key]
                    document.getElementById("fileSelectList").appendChild(opt)
                }
            }
            document.getElementById("fileCompareSpinnerWrapper").remove();
            document.getElementById("fileSelectWrapper").removeAttribute("hidden");
            document.getElementById("fileSelectHeader").removeAttribute("hidden");
            //
            // Next step / action
            recompile_apk()
        },
        error: function() {}
    });
}

/**
 * Handle #fileSelectList option change
 * @PARAM       - Selected value (Array index)
 * @return      - File compare HTML data
 */
 function fileSelect(sel){
    $("#fileCompare").load("../static/tmp/" + sel.value + ".html");
};

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
        error: function() {}
    });
}
