function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#createColony").on("submit", function() {
        createColony(this);
        return false;
    });

    $("#removeColony").on("submit", function() {
        removeColony(this);
        return false;
    });

    $("#createPlanet").on("submit", function() {
        createPlanet(this);
        return false;
    });

    $("#addResource").on("submit", function() {
        addResource(this);
        return false;
    });

    $("#addMember").on("submit", function() {
        addMember(this);
        return false;
    });

});

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        response = eval('(' + response + ')')
        if (callback) callback(response);
    }, error: function(response) {
        console.log("ERROR:", response);
    }});
};

function createColony(form) {
    if (!form.name.value || !form.chief.value){
        alert('fill gaps. not empty');
        return;
    }
    var message = $(form).formToDict();

    $.postJSON("/new/colony/", message, function(response) {

        resources = response.resources;
        error = response.error;

        if (error == undefined){
            alert(
                'Создана колония у которой ' + resources.Apple + ' яблок и ' +
                resources.Banana + ' бананов и ' +
                resources.Cherry + ' черешнь.'
            );
        } else {
            alert(error);
        }
    });
}

function createPlanet(form) {
    if (!form.name.value){
        alert('fill gap. not empty');
        return;
    }
    var message = $(form).formToDict();

    $.postJSON("/new/planet/", message, function(response) {
        alert(Object.values(response));
    });
}

function addResource(form) {
    if (!form.count.value){
        alert('fill gap. not empty');
        return;
    }
    var message = $(form).formToDict();

    $.postJSON("/new/resource/", message, function(response) {
        alert(Object.values(response));
    });
}

function removeColony(form) {
    $.postJSON("/colony/remove/" + form.col_name.value + '/', '', function(response) {
        alert(Object.values(response));
    });
}

function addMember(form) {
    if (!form.alias.value || !form.force.value){
        alert('fill gaps. not empty');
        return;
    }
    var message = $(form).formToDict();

    $.postJSON("/new/member/", message, function(response) {
        alert(Object.values(response));
    });
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};
