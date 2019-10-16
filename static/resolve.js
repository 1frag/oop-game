let sharing_data = [];
let cur_id = 0;
let total = {};
let code, url, result, selecter;

$(document).ready(function() {
    code = document.getElementById("code").innerText;
    selecter = document.getElementById("selecter");
    url = "/conflict/resolve/" + code + "/";
    let storage = document.getElementById("planets");
    sharing_data = eval(storage.innerText);
    alert(sharing_data.length);
    nextValue();
});

function prepare() {
    if (sharing_data[cur_id] === undefined) {
        return false;
    } else {
        return sharing_data[cur_id];
    }
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        response = eval('(' + response + ')');
        if (callback) callback(response);
    }, error: function(response) {
        console.log("ERROR:", response);
    }});
};

function nextValue() {
    let placeholder = document.getElementById("cap-pl");
    total[result[0]] = selecter.value;
    result = prepare();
    if (result === false) {
        // todo: данные готовы нажмите для перехода
        $.postJSON(url, total, function(response) {
            alert(response.result);
        });
    } else {
        placeholder.innerText = result[0] + ". (сейчас у " + result[1] + ")";
    }
}
