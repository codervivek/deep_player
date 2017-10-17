function upload_file_func() {
    var params = {
        // Request parameters
        "name": "file_name1",
        "privacy": "Public",
        "videoUrl": "http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4"
    };
  
    $.ajax({
        url: "https://videobreakdown.azure-api.net/Breakdowns/Api/Partner/Breakdowns?" + $.param(params),
        beforeSend: function(xhrObj){
            // Request headers
            xhrObj.setRequestHeader("Content-Type","multipart/form-data");
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key","8eec2a625b584342b4adde9c7ea87c6a");
        },
        type: "POST",
        // Request body
        data: "",
    })
    .done(function(data) {
        alert("success");
    })
    .fail(function() {
        alert("error");
    });
    // console.log("aas")
};
