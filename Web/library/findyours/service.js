function mySetMobile() {
    $('#modal-developer .circular.image').removeClass('medium');
    $('#modal-developer .circular.image').addClass('small');

    $('#modal-developer .button').contents().filter(function() {
        return this.nodeType === 3;
    }).remove();

    $('#modal-developer .button').addClass('circular icon');
}

function setRadio() {
    $('.radio.checkbox').checkbox();
    $('#param-service .field:nth-child(2) .checkbox').checkbox({
        onChecked: function() {
            $('#param-type .dropdown').removeClass('disabled');
            $('#param-type .dropdown').dropdown('clear');
        }
    });
    $('#param-service .field:nth-child(3) .checkbox').checkbox({
        onChecked: function() {
            $('#param-type .dropdown').dropdown('set value', 'PRJ000');
            $('#param-type .dropdown').dropdown('set text', '휴대폰');
            $('#param-type .dropdown').addClass('disabled');
        }
    });
}

function setDropdown() {
    $('.dropdown').dropdown();
}

function setCalendar(selector1, selector2) {
    $(selector1).calendar({
        type: 'date',
        today: true,
        monthFirst: false,
        maxDate: new Date(),
        endCalendar: $(selector2),
        formatter: {
            date: function(date, settings) {
                if (!date) {
                    return '';
                }

                var year = date.getFullYear();
                var month = date.getMonth() + 1;
                var day = date.getDate();

                if (month < 10) {
                    month = '0' + month;
                }

                if (day < 10) {
                    day = '0' + day;
                }

                return year + month + day;
            }
        }
    });
}

function showForm() {
    $('#content-main').transition('hide');
    $('#content-form').transition('fade up');
}

function showModal(selector) {
    $(selector).modal('show');
}

function checkParam() {
    var paramService = $('#param-service .radio.checked label').attr('class');
    var paramLocate = $('#param-locate .dropdown').dropdown('get value');
    var paramPlace = $('#param-place input').val();
    var paramStart = $('#calendar-start input').val();
    var paramEnd = $('#calendar-end input').val();
    var paramType = $('#param-type .dropdown').dropdown('get value');
    var paramName = $('#param-name input').val();

    $('#content-form .fields, .field').removeClass('error');

    var check = true;

    if (paramService == undefined) {
        $('#param-service').addClass('error');
        check = false;
    }
    
    if (paramLocate[0] == '') {
        $('#param-locate').addClass('error');
        check = false;
    }

    if (paramStart == '') {
        $('#param-start').addClass('error');
        check = false;
    }

    if (paramEnd == '') {
        $('#param-end').addClass('error');
        check = false;
    }

    if (paramType[0] == '') {
        $('#param-type').addClass('error');
        check = false;
    }
    
    if (check == true) {
        MyParam = [paramService, paramLocate[0], paramPlace, paramStart, paramEnd, paramType[0], paramName];
        getResponse(MyParam);
    }
}

function setData(param, page) {
    if (param[0] == 'losFund') {
        return {
            'N_FD_LCT_CD': param[1],
            'DEP_PLACE' : param[2],
            'START_YMD': param[3],
            'END_YMD': param[4],
            'PRDT_CL_CD_01': param[5],
            'PRDT_CL_CD_02': '',
            'PRDT_NM' : param[6],
            'FD_COL_CD' : '',
            'pageNo' : page
        };
    } else if (param[0] == 'searchMobl') {
        return {
            'FD_LCT_CD': param[1],
            'START_YMD': param[3],
            'END_YMD': param[4],
            'PRDT_CL_CD_02': '',
            'COL_CD' : '',
            'pageNo' : page
        };
    }
}

function setResult(response) {
    $('#modal-result table tbody').empty();
    $('#modal-result .menu').empty();

    if (response.length == 1) {
        var tr = '<tr>';
        tr += '<td>' + '조회 결과가 없습니다.' + '</td>';
        tr += '</tr>'
        $('#modal-result table tbody').append(tr);
    } else {
        for (var i = 0; i < response.length - 1; i++) {
            var link = 'javascript:window.open(\'./detail.html?service='+ MyParam[0] + '&ATC_ID=' + response[i].atcId + '&FD_SN=' + response[i].fdSn + '\')';
            var tr = '<tr>';
            tr += '<td>' + response[i].prdtClNm + '</td>';
            tr += '<td><a class="ellipsis" href="' + link + '">' + response[i].fdPrdtNm + '</a></td>';
            tr += '<td>' + response[i].fdYmd + '</td>';
            tr += '<td>' + response[i].depPlace + '</td>';
            tr += '</tr>';
            $('#modal-result table tbody').append(tr);
        }

        for (var i = 0; i < response[response.length - 1].pageCount; i++) {
            var a = '<a class="item" onclick="javascript:getPage(MyParam, ' + (i + 1) + ')">';
            a += (i + 1) + '</a>'
            $('#modal-result .menu').append(a);
            $('#modal-result .menu a:first-child()').addClass('active');
        }
    }

    $('#content-form .raised.segment').removeClass('loading');

    showModal('#modal-result')
}

function getResponse(param) {
    var url = 'http://hwyncho.dlinkddns.com:9350';
    var text = '';

    if (param[0] == "losFund") {
        url += '/LosfundInfoInqireService';
        text = '물품명'
    } else if (param[0] == "searchMobl") {
        url += '/SearchMoblphonInfoInqireService';
        text = '휴대폰 기종'
    }

    $('#content-form .raised.segment').addClass('loading');

    $('#modal-result table thead th:nth-child(2)').text(text);

    $.ajax({
        url: url,
        data: setData(param),
        dataType: 'jsonp',
        jsonp: 'callback',
        success: function(response) {
            setResult(response)
        },
        error: function() {
            $('#content-form .raised.segment').removeClass('loading');
            alert("서버에 오류가 발생했습니다!");
        }
    });
}

function getPage(param, page) {
    var url = 'http://hwyncho.dlinkddns.com:9350';

    if (param[0] == 'losFund') {
        url += '/LosfundInfoInqireService/page';
    } else if (param[0] == 'searchMobl') {
        url += '/SearchMoblphonInfoInqireService/page';
    }

    $('#modal-result .menu a').removeClass('active');

    var selector = '#modal-result .menu a:nth-child(' + page + ')'
    $(selector).addClass('active');

    $('#modal-result .segment:first-child()').addClass('loading');

    $.ajax({
        url: url,
        data: setData(param, page),
        dataType: 'jsonp',
        jsonp: 'callback',
        success: function(response) {
            $('#modal-result table tbody').empty();
            for (var i = 0; i < response.length; i++) {
                var link = 'javascript:window.open(\'./detail.html?service='+ MyParam[0] + '&ATC_ID=' + response[i].atcId + '&FD_SN=' + response[i].fdSn + '\')';
                var tr = '<tr>';
                tr += '<td>' + response[i].prdtClNm + '</td>';
                tr += '<td><a class="ellipsis" href="' + link + '">' + response[i].fdPrdtNm + '</a></td>';
                tr += '<td>' + response[i].fdYmd + '</td>';
                tr += '<td>' + response[i].depPlace + '</td>';
                tr += '</tr>';
                $('#modal-result table tbody').append(tr);
            }
            
            $('#modal-result .segment:first-child()').removeClass('loading');
        },
        error: function() {
            $('#modal-result .segment:first-child()').removeClass('loading');
            alert("서버에 오류가 발생했습니다!");
        }
    });
}
