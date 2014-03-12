function submitStream(m) {
    $("#streamSubmit").slideUp('fast');
    $.ajax({
        type: "POST",
        url: "ajax/submitStream.php",
        data: "m=" + m + "&link=" + $("#link").val(),
        success: function(data) {
            $("#streamSubmit").html(data);
            $("#streamSubmit").slideDown('fast');
        }
    });
}

function selectTeam(that, on) {
    $('#on').val(on);
    $('.active').removeClass();
    that.addClass('active');
}

function addToPoll(that) {
    if ($('.left').children().size() < 4)
        that.appendTo('.left').attr('onclick', 'removeFromPoll($(this))');
}

function removeFromPoll(that) {
    that.appendTo('#backpack').attr('onclick', 'addToPoll($(this))');
}

function placeBet(match) {
    if (!$('#on').val()) {
        window.alert("You didn't select a team.");
        $("#placebut").show();
    }
    else {
        if ($('.left').children().size() > 0) {
            $.ajax({
                type: "POST",
                url: "ajax/postBet.php",
                data: $("#betpoll").serialize() + "&match=" + match,
                success: function(data) {
                    if (data) {
                        $(".buttonright").show();
                        window.alert(data);
                    } else {
                        window.location.href = "mybets";
                    }
                }
            });
        } else {
            $.ajax({
                type: "POST",
                url: "ajax/postQueue.php",
                data: $("#betpoll").serialize() + "&match=" + match,
                success: function(data) {
                    if (data) {
                        $(".buttonright").show();
                        window.alert(data);
                    } else {
                        window.location.href = location.href;
                    }
                }
            });
        }
    }
}

function placeBetKeys(match) {
    if (!$('#on').val()) {
        window.alert("You didn't select a team.");
        $("#placebut").show();
    }
    else {
        if ($('.left').children().size() > 0) {
            $.ajax({
                type: "POST",
                url: "ajax/postBet.php",
                data: $("#betpoll").serialize() + "&match=" + match,
                success: function(data) {
                    if (data) {
                        $(".buttonright").show();
                        window.alert(data);
                    } else {
                        window.location.href = "mybets";
                    }
                }
            });
        } else {
            $.ajax({
                type: "POST",
                url: "ajax/postQueueKey.php",
                data: $("#betpoll").serialize() + "&match=" + match,
                success: function(data) {
                    if (data) {
                        $(".buttonright").show();
                        window.alert(data);
                    } else {
                        window.location.href = location.href;
                    }
                }
            });
        }
    }
}

function addItemsBet(match) {
    if ($('.left').children().size() > 0) {
        $.ajax({
            type: "POST",
            url: "ajax/addItemsBet.php",
            data: $("#betpoll").serialize() + "&match=" + match,
            success: function(data) {
                if (data) {
                    $("#placebut").show();
                    window.alert(data);
                } else {
                    window.location.href = "mybets";
                }
            }
        });
    }
}

function changeTeams(match) {
    $.ajax({
        type: "POST",
        url: "ajax/changeTeams.php",
        data: "match=" + match,
        success: function(data) {
            if (data) {
                window.alert(data);
            } else {
                window.location.href = "mybets";
            }
        }
    });
}

function requestReturn(bot) {
    $.ajax({
        type: "POST",
        url: "ajax/postQueue.php",
        data: "bot=" + bot,
        success: function(data) {
            if (data) {
                window.alert(data);
            } else {
                window.location.href = "mybets";
            }
        }
    });
}