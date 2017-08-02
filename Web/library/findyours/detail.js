function getUrlParam() {
    var param = [];
    var temps = window.location.href.slice(
        window.location.href.indexOf('?') + 1
    ).split('&');

    for (var i = 0; i < temps.length; i++) {
        var temp = temps[i].split('=');
        param.push(temp[1]);
    }

    return param;
}

function getDetail(param) {
    var url = 'http://hwyncho.dlinkddns.com:9350';

    if (param[0] == 'losFund') {
        url += '/LosfundInfoInqireService/detail';
    } else if (param[0] == 'searchMobl') {
        url += '/SearchMoblphonInfoInqireService/detail';
    }

    $('.segment').addClass('loading');

    $.ajax({
        url: url,
        data: {
            'ATC_ID' : param[1],
            'FD_SN' : param[2]
        },
        dataType: 'jsonp',
        jsonp: 'callback',
        success: function(response) {
            $('#data-img').attr('src', response.fdFilePathImg);
            $('#data-state').text(response.csteSteNm);
            $('#data-name').text(response.fdPrdtNm);
            $('#data-type').text(response.prdtClNm);
            $('#data-ymd').text(response.fdYmd);
            $('#data-place').text(response.fdPlace);
            $('#data-keep').text(response.depPlace);
            $('#data-tel').text(response.tel);

            if (response.csteSteNm == "종결") {
                $('#data-state').removeClass('blue');
                $('#data-state').addClass('red');
            }

            $('.segment').removeClass('loading');

            setMapApi();
        },
        error: function() {
            $('.segment').removeClass('loading');
            alert("서버에 오류가 발생했습니다!");
        }
    });
}

function setMapApi() {
    var api_key = 'AIzaSyD2lMBhByt6izCKL1EzosjWTXBQuvjZkLs';

    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?v=3&key=' + api_key + '&callback=getMap';

    $('head').append(script);
}

function getMap() {
    var address = $('#data-keep').text();
    var api_key = 'AIzaSyD2lMBhByt6izCKL1EzosjWTXBQuvjZkLs';
    var url = 'https://maps.googleapis.com/maps/api/geocode/json?&key='+ api_key + '&address=' + address;

    $.ajax({
        url: url,
        success: function(response) {
            var lat = response.results[0].geometry.location.lat;
            var lng = response.results[0].geometry.location.lng;

            var map_location = new google.maps.LatLng(lat, lng);
            var marker_location = new google.maps.LatLng(lat, lng);

            var map_options = {
                center: map_location,
                zoom: 18,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            var map = new google.maps.Map(document.getElementById('map'), map_options);

            var marker = new google.maps.Marker({
                position: marker_location,
                map: map,
            });
        }
    });
}

function showMap() {
    $('#modal-map').modal('show');
}
