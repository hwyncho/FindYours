# -*- coding: utf-8 -*-

import json
import re
import requests
from flask import Flask
from flask import request
from pyquery import PyQuery as pq

# Flask Application
app = Flask(__name__)

# Open API
URL = 'http://openapi.lost112.go.kr/openapi/service/rest'
ServiceKey = u'up0ahmkXV9r50EuIXRtrH%2BFVCZ%2BIG1ZyLEK%2BA6RD0ePZzC79Jdhnv1X7iAtwlIvEolo5Cf2tvZHnIIOm9GWwxg%3D%3D'

# selector
select = 'body items item'
select_rnum = 'rnum'
select_atcId = 'atcId'
select_fdSn = 'fdSn'
select_prdtClNm = 'prdtClNm'
select_clrNm = 'clrNm'
select_fdPrdtNm = 'fdPrdtNm'
select_fdSbjt = 'fdSbjt'
select_fdFilePathImg = 'fdFilePathImg'
select_depPlace = 'depPlace'
select_fdYmd = 'fdYmd'

select_mdcd = 'mdcd'
select_srno = 'srno'

select_fdHor = 'fdHor'
select_fdPlace = 'fdPlace'
select_csteSteNm = 'csteSteNm'
select_fndKeepOrgnSeNm = 'fndKeepOrgnSeNm'
select_orgId = 'orgId'
select_orgNm = 'orgNm'
select_tel = 'tel'

select_uniq = 'uniq'


def getItem(xml, page=False):
    items = []
    for _item in xml(select).items():
        item = {}
        item['atcId'] = _item(select_atcId).text()
        item['fdSn'] = _item(select_fdSn).text()
        item['prdtClNm'] = _item(select_prdtClNm).text()
        item['fdPrdtNm'] = _item(select_fdPrdtNm).text()
        item['depPlace'] = _item(select_depPlace).text()
        item['fdYmd'] = _item(select_fdYmd).text()
        items.append(item)

    if page == True:
        numOfRows = int(xml('body numOfRows').text())
        totalCount = int(xml('body totalCount').text())

        if (totalCount % numOfRows) != 0:
            pageCount = int(totalCount / numOfRows) + 1
        else:
            pageCount = int(totalCount / numOfRows)

        items.append({'pageCount':pageCount})

    return items


@app.route('/')
def index():
    return


@app.route('/LosfundInfoInqireService', methods=['GET', 'POST'])
def lostFund():
    callback = request.values['callback']
    PRDT_CL_CD_01 = request.values['PRDT_CL_CD_01']
    PRDT_CL_CD_02 = request.values['PRDT_CL_CD_02']
    FD_COL_CD = request.values['FD_COL_CD']
    START_YMD = request.values['START_YMD']
    END_YMD = request.values['END_YMD']
    N_FD_LCT_CD = request.values['N_FD_LCT_CD']
    PRDT_NM = request.values['PRDT_NM']
    DEP_PLACE = request.values['DEP_PLACE']

    url = '{0}/{1}?ServiceKey={2}&PRDT_CL_CD_01={3}&PRDT_CL_CD_02={4}&FD_COL_CD={5}&START_YMD={6}&END_YMD={7}&N_FD_LCT_CD={8}'.format(
        URL,
        'LosfundInfoInqireService/getLosfundInfoAccToClAreaPd',
        ServiceKey,
        PRDT_CL_CD_01,
        PRDT_CL_CD_02,
        FD_COL_CD,
        START_YMD,
        END_YMD,
        N_FD_LCT_CD
    )

    response = requests.get(url=url)

    xml = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    xml = pq(xml, parser='xml')

    return callback + '(' + str(json.dumps(getItem(xml, True))) +')'


@app.route('/SearchMoblphonInfoInqireService', methods=['GET', 'POST'])
def searchMobl():
    callback = request.values['callback']
    PRDT_CL_CD_02 = request.values['PRDT_CL_CD_02']
    COL_CD = request.values['COL_CD']
    START_YMD = request.values['START_YMD']
    END_YMD = request.values['END_YMD']
    FD_LCT_CD = request.values['FD_LCT_CD']

    url = '{0}/{1}?ServiceKey={2}&PRDT_CL_CD_02={3}&COL_CD={4}&START_YMD={5}&END_YMD={6}&FD_LCT_CD={7}'.format(
        URL,
        'SearchMoblphonInfoInqireService/getMoblphonAcctoKindAreaPeriodInfo',
        ServiceKey,
        PRDT_CL_CD_02,
        COL_CD,
        START_YMD,
        END_YMD,
        FD_LCT_CD
    )

    response = requests.get(url=url)

    xml = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    xml = pq(xml, parser='xml')

    return callback + '(' + str(json.dumps(getItem(xml, True))) +')'


@app.route('/LosfundInfoInqireService/page', methods=['GET', 'POST'])
def lostFund2():
    callback = request.values['callback']
    PRDT_CL_CD_01 = request.values['PRDT_CL_CD_01']
    PRDT_CL_CD_02 = request.values['PRDT_CL_CD_02']
    FD_COL_CD = request.values['FD_COL_CD']
    START_YMD = request.values['START_YMD']
    END_YMD = request.values['END_YMD']
    N_FD_LCT_CD = request.values['N_FD_LCT_CD']
    PRDT_NM = request.values['PRDT_NM']
    DEP_PLACE = request.values['DEP_PLACE']
    pageNo = request.values['pageNo']

    url = '{0}/{1}?ServiceKey={2}&PRDT_CL_CD_01={3}&PRDT_CL_CD_02={4}&FD_COL_CD={5}&START_YMD={6}&END_YMD={7}&N_FD_LCT_CD={8}&pageNo={9}'.format(
        URL,
        'LosfundInfoInqireService/getLosfundInfoAccToClAreaPd',
        ServiceKey,
        PRDT_CL_CD_01,
        PRDT_CL_CD_02,
        FD_COL_CD,
        START_YMD,
        END_YMD,
        N_FD_LCT_CD,
        pageNo
    )

    response = requests.get(url=url)

    xml = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    xml = pq(xml, parser='xml')

    return callback + '(' + str(json.dumps(getItem(xml))) +')'


@app.route('/SearchMoblphonInfoInqireService/page', methods=['GET', 'POST'])
def searchMobl2():
    callback = request.values['callback']
    PRDT_CL_CD_02 = request.values['PRDT_CL_CD_02']
    COL_CD = request.values['COL_CD']
    START_YMD = request.values['START_YMD']
    END_YMD = request.values['END_YMD']
    FD_LCT_CD = request.values['FD_LCT_CD']
    pageNo = request.values['pageNo']

    url = '{0}/{1}?ServiceKey={2}&PRDT_CL_CD_02={3}&COL_CD={4}&START_YMD={5}&END_YMD={6}&FD_LCT_CD={7}&pageNo={8}'.format(
        URL,
        'SearchMoblphonInfoInqireService/getMoblphonAcctoKindAreaPeriodInfo',
        ServiceKey,
        PRDT_CL_CD_02,
        COL_CD,
        START_YMD,
        END_YMD,
        FD_LCT_CD,
        pageNo
    )

    response = requests.get(url=url)

    xml = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    xml = pq(xml, parser='xml')

    return callback + '(' + str(json.dumps(getItem(xml))) +')'


@app.route('/LosfundInfoInqireService/detail', methods=['GET', 'POST'])
def losFundDetail():
    callback = request.values['callback']
    ATC_ID = request.values['ATC_ID']
    FD_SN = request.values['FD_SN']

    url = '{0}/{1}?ServiceKey={2}&ATC_ID={3}&FD_SN={4}'.format(
        URL,
        'LosfundInfoInqireService/getLosfundDetailInfo',
        ServiceKey,
        ATC_ID,
        FD_SN
    )

    response = requests.get(url=url)

    xml = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    xml = pq(xml, parser='xml')

    items = []
    item = {}
    item['fdPrdtNm'] = xml('body item ' + select_fdPrdtNm).text()
    item['fdFilePathImg'] = xml('body item ' + select_fdFilePathImg).text()
    item['fdYmd'] = xml('body item ' + select_fdYmd).text()
    item['fdPlace'] = xml('body item ' + select_fdPlace).text()
    item['prdtClNm'] = xml('body item ' + select_prdtClNm).text()
    item['depPlace'] = xml('body item ' + select_depPlace).text()
    item['csteSteNm'] = xml('body item ' + select_csteSteNm).text()
    item['tel'] = xml('body item ' + select_tel).text()
    items.append(item)

    return callback + '(' + str(item) +')'


@app.route('/SearchMoblphonInfoInqireService/detail', methods=['GET', 'POST'])
def searchMoblDetail():
    callback = request.values['callback']
    ATC_ID = request.values['ATC_ID']
    FD_SN = request.values['FD_SN']

    url = '{0}/{1}?ServiceKey={2}&ATC_ID={3}&FD_SN={4}'.format(
        URL,
        'SearchMoblphonInfoInqireService/getMoblphonDetailInfo',
        ServiceKey,
        ATC_ID,
        FD_SN
    )

    response = requests.get(url=url)

    xml = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    xml = pq(xml, parser='xml')

    items = []
    item = {}
    item['fdPrdtNm'] = xml('body item ' + select_fdPrdtNm).text()
    item['fdFilePathImg'] = xml('body item ' + select_fdFilePathImg).text()
    item['fdYmd'] = xml('body item ' + select_fdYmd).text()
    item['fdPlace'] = xml('body item ' + select_fdPlace).text()
    item['prdtClNm'] = xml('body item ' + select_prdtClNm).text()
    item['depPlace'] = xml('body item ' + select_depPlace).text()
    item['csteSteNm'] = xml('body item ' + select_csteSteNm).text()
    item['tel'] = xml('body item ' + select_tel).text()
    items.append(item)

    return callback + '(' + str(item) +')'


# Application Run
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
