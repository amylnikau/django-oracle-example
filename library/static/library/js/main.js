function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function () {
    var alert_message = $(".alert");
    $("[data-hide]").on("click", function () {
        $(this).closest("." + $(this).attr("data-hide")).hide();
    });
    if (alert_message.attr('style') != "display: none") {
        alert_message.fadeTo(4000, 500).slideUp(500, function () {
            alert_message.slideUp(500);
        });
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    $(".form-check-input").change(function () {
        $.ajax({
            url: '/trigger-switch',
            method: 'post',
            data: {
                trigger: this.id,
                value: $(this).is(":checked")
            },
            dataType: 'json',
            success: function (data) {
                alert_message.children("span").text(data.message);
                alert_message.show();
                alert_message.fadeTo(4000, 500).slideUp(500, function () {
                    alert_message.slideUp(500);
                });
            }
        });
    });
});