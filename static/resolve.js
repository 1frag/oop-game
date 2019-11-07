let planets = [];
let cur_id = 0;
let total = {};
let code, url, result = null, selecter;

$(document).ready(function() {
    code = document.getElementById("code").innerText;
    selecter = document.getElementById("selecter");
    url = "/conflict/resolve/" + code + "/";
    let storage = document.getElementById("planets");
    planets = eval(storage.innerText);
    $('#input').prop('value', 'Заполнить далее');
    nextValue();
});

function prepare() {
    if (planets[cur_id] === undefined) {
        return false;
    } else {
        return planets[cur_id];
    }
}

jQuery.postJSON = function(url, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        response = eval('(' + response + ')');
        if (callback) callback(response);
    }, error: function(response) {
        console.log("ERROR:", response);
    }});
};

function nextValue() {
    if(result)
        total[result[0]] = selecter.value;
    result = prepare();
    cur_id++;
    console.log(cur_id);
    if (result === false) {
        console.log('the end');
        let input = document.querySelector('#input');
        input.innerText = 'Все планеты распределены, ' +
            'нажмите для отправки результатов на сервер';
        input.onclick = function() {
            $.postJSON(url, total, function (response) {
                alert(response.result);
            });
        }
    } else {
        console.log(result);
        let value = result[0] + ". (сейчас у " + result[1] + ")";
        $('#cap-pl').prop('innerText', value);
    }
}
