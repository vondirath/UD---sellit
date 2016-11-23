$(document).ready
$(function () {
    $(".arrow").click(function () {
        $('html, body').animate({
            scrollTop: $(".loginlink").offset().top
        }, 1500);
    })
})
