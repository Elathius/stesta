// For menus

function openNav() {
    document.getElementById("myNav").style.width = "100%";
}

function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}

// <!-- for Add Card overlay -->

function openAdd() {
    document.getElementById("Addpanel").style.height = "100%";
}

function closeAdd() {
    document.getElementById("Addpanel").style.height = "0%";
}

// <!-- For all cards view button / subcard -->

function openView(dis) {
    //var dis = "myNav";
    document.querySelector("#" + dis).style.height = "100%";
    document.body.style.overflow = "hidden";
}

function closeView(dis) {
    document.querySelector("#" + dis).style.height = "0%";
    document.body.style.overflow = "auto";
}



$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function () {

    var parwidth = $('.progress-bar').parent().width();
    $("#taskspace .progress-bar").each(function () {
        var f = $(this).width() / parwidth * 100;
        console.log("done: ", f);
        $(this).width(0);
        console.log(f + "%");
        $(this).animate({
            width: f + "%",
        }, 1500);
    });
    $(".subcardoverlay").each(function () {
        var checked = $(this).find('.inputcountchecked').length;
        var nonchecked = $(this).find('.inputcount').length;
        console.log(checked, "<-");
        console.log(nonchecked + checked, "->");
        $(this).find('#inputcountresult').text(checked + "/" + (nonchecked + checked))
    });
});

var datenow = moment.utc().local().format();
$("#taskspace .card-body").each(function () {
    var dateobject = $(this).find('#deadlinetime').data("deadline-date");
    var timeobject = $(this).find('#deadlinetime').data("deadline-time");

    var date = moment(dateobject).add(moment.duration(timeobject));
    var difference = moment(datenow).diff(moment(date));
    var d = moment.duration(difference).format("d [days], h [hours], m [m], s [s]", {
        largest: 1
    });
    console.log(d);
    console.log("<---->");
    $(this).find('#deadlinetime').text(d);
});
$(".subcardoverlay #subcardheader").each(function () {
    var dateobject = $(this).find('#deadlinetime').data("deadline-date");
    var timeobject = $(this).find('#deadlinetime').data("deadline-time");

    var date = moment(dateobject).add(moment.duration(timeobject));
    var difference = moment(datenow).diff(moment(date));
    var d = moment.duration(difference).format("d [days], h [hours], m [m], s [s]", {
        largest: 1
    });
    console.log(d);
    console.log("^----^");
    $(this).find('#deadlinetime').text(d);
});


