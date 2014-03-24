$("textarea").on("keyup", function(e) {
    var textarea = $(this);
    var parent = textarea.parent();
    console.log(textarea.val());
    if (textarea.val() !== "") {
        parent.find("button").hide(1000);
    } else {
        parent.find("button").show(1000);
    }
});

// $("[id^=button]").on("