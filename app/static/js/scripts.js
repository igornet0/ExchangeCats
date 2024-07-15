$(document).ready(function() {
    $("#wallet").click(function() {
        document.location.href = "/wallet/" + tg.initDataUnsafe.user.id;
    });

    $('.coin_elem').click(function(e) {
        var coinName = $(this).attr("coin-id");

        document.location.href = "/coin/" + coinName;
    });
});