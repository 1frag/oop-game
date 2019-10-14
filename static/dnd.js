counter_for_inner = 15;
counter_for_outer = 15;
$(function () {
    $('.draggable').draggable();
});

jQuery.postJSON = function(url, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        response = eval('(' + response + ')');
        if (callback) callback(response);
    }, error: function(response) {
        console.log("ERROR:", response);
    }});
};

function createObjectLike(_side_, _type_, _meta_) {
    let obj = document.createElement("div");
    obj.className = "ui-widget ui-corner-all ui-state-error ui-draggable draggable " + _side_;
    obj.style.width = "auto";
    if (_side_ == "inner") {
        obj.style.left = "10%";
        obj.style.top = counter_for_inner + "%";
        counter_for_inner += 10;
    } else {
        obj.style.left = "70%";
        obj.style.top = counter_for_outer + "%";
        counter_for_outer += 10;
    }
    obj.style.position = "fixed";
    if (_type_ == 'places') {
        obj.innerText = "Планета " + _meta_.name;
    } else {
        obj.innerText = "Колония " + _meta_.name;
    }
    obj.python_id = _meta_.id;
    obj.python_type = _type_;
    let place = document.getElementById("stuff");
    document.body.insertBefore(obj, place);

}

function saveChanges(code) {
    let line = document.getElementById("boundary").offsetLeft;
    let inners = document.getElementsByClassName("inner");
    let outers = document.getElementsByClassName("outer");
    let result = {};
    let res = "";
    let stage_no = 0;
    for (let i = 0; i < inners.length; i++) {
        if (inners[i].offsetLeft > line) {
            res = "to$" + inners[i].python_type;
            res = res + "$" + inners[i].python_id;
            result['st'+stage_no] = res;
            stage_no += 1;
        }
    }
    for (let i = 0; i < outers.length; i++) {
        if (outers[i].offsetLeft < line) {
            res = "in$" + outers[i].python_type;
            res = res + "$" + outers[i].python_id;
            result['st'+stage_no] = res;
            stage_no += 1;
        }
    }
    alert(result);

    $.postJSON("/conflict/change/" + code + "/", result, function (response) {
        alert(response.result);
    });
}
