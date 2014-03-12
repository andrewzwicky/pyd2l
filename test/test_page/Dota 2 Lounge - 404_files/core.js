$("#rarityselectright").change(function () {
  $("#rarityselectright option:selected").each(function () {
    if($(this).text() == "Rarity All") setSubCat('Dota',1,1);
    else setSubCat('Dota',12,1,1,$(this).text());
  });
});

$("#heroselectright").change(function () {
  $("#heroselectright option:selected").each(function () {
    if($(this).text() == "Heroes All") setSubCat('Dota',1,1);
    else setSubCat('Dota',11,1,1,$(this).text());
  });
});

$("#rarityselect").change(function () {
  $("#rarityselect option:selected").each(function () {
    if($(this).text() == "Rarity All") $("#itemlist .item").show();
	else raritySort($(this).text());
  });
});

function raritySort(rarity) {
  $("#itemlist .rarity").parent(".item").hide();
  $("#itemlist ."+rarity).parent(".item").show();
}

$("#heroselect").change(function () {
  $("#heroselect option:selected").each(function () {
    if($(this).text() == "Heroes All") $("#itemlist .item").show();
    else heroSort($(this).text());
  });
});

function heroSort(hero) {
  $('.simplePagerNav').css('visibility','hidden');
  $("#itemlist .item").hide();
  $("#itemlist .hero:contains('"+hero+"')").parent().parent(".item").show();
}

function livePreview(trade, that) {
  $("#preview").html('<img src="../img/load.gif" id="loading" style="margin: 0.75em 2%">');
  $("#preview").css('marginTop', that.position().top - 90 );
  $.ajax({
    url: 'ajax/livePreview.php',
    type: 'POST',
    data: "t="+trade,
    success: function(data) {
      $("#preview").html(data).slideDown('fast');
    }
  });
}

function ajaxLoad(where, what) {
  $(where).html('<img src="../img/load.gif" id="loading" style="margin: 0.75em 2%">');
  $.ajax({
    url: 'ajax/'+what+'.php',
    type: 'POST',
    success: function(data) {
      $(where).html(data).slideDown('fast');
    }
  });
}

function addBookmark(trade) {
  $.ajax({
    type: "POST",
    url: "core/addbookmark.php",
    data: "trade="+trade
  });
}

function removeBookmark(trade) {
  $.ajax({
    type: "POST",
    url: "core/removebookmark.php",
    data: "trade="+trade
  });
}

function removeQueue() {
	$.ajax({
		url: "ajax/removeQueue.php",
		success: function(data) {
			if (data) {
				window.alert(data);
			} else {
				window.location.href = location.href;
			}
		}
	});
}

function setLanguage(lang) {
  $.ajax({
    type: "POST",
    url: "ajax/setLanguage.php",
    data: "lang="+lang,
	success: function(data) {
		window.location.href = location.href;
	}
  });
}

function choseStream(match,lang) {
  $.ajax({
    type: "POST",
    url: "ajax/choseStream.php",
    data: "m="+match+"&lang="+lang,
	success: function(data) {
		$("#stream").html(data);
	}
  });
}

function choseVOD(match,lang) {
  $.ajax({
    type: "POST",
    url: "ajax/choseVOD.php",
    data: "m="+match+"&lang="+lang,
	success: function(data) {
		$("#youtube").html(data);
	}
  });
}

function changeSteamOfferURL(changeOnly, bets) {
    bets = typeof bets !== 'undefined' ? bets : false;
    
    var change = "";
    var forbets = "";
    var betsid = "";
    if (bets) {
        forbets = "&bets=1";
        betsid = "bets";
    }
    if ($("#steamoffers"+betsid).val() != null && changeOnly == true) {
        var str = $("#steamoffers"+betsid).val();
        var n = str.indexOf("token=");
        if (n != -1) change = str.substring(n+6,n+14);
    }

    $.ajax({
        type: "POST",
        url: "ajax/changeSOURL.php",
        data: 'steamoffers=' + change + forbets,
        success: function(data) {
            window.location.href = location.href;
        }
    });
}