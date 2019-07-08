"""
#============================================================
# README.md
#============================================================
기술명 [techname] | API명 [apicode]
http://aiopen.etri.re.kr/service_list.php
"""
import os
import inspect
from datetime import datetime, timezone, timedelta
import pandas as pd
import urllib3
import json
import re
import idebug as dbg
from inews import models
from bson.objectid import ObjectId
from pandas.io.json import json_normalize

#============================================================
"""APIs."""
#============================================================

OPEN_API_URI = "http://aiopen.etri.re.kr:8000"

def get_jsondata(res):
    """
    [HTTP Response Body]
    {
    	"request_id": "reserved field",
    	"result": 0, # 0:정상완료, -1:실패
    	"return_type": "com.google.gson.internal.LinkedTreeMap",
    	"return_object": {어휘 관계분석 결과 JSON}
    }
    [HTTP Response Body]
    {
    	"request_id": "reserved field",
    	"result": 0,
    	"return_type": "kr.re.etri.aiopen.restapi.client.dto.OpenApiLmInterfaceResult",
    	"return_object": {언어 분석 결과 JSON}
    }
    """
    datastr = str(res.data, "utf-8")
    jsondata = json.loads(datastr)
    if jsondata['result'] is -1:
        print(f"\n\n jsondata['reason'] : {jsondata['reason']}")
        if re.search('exceed',string=jsondata['reason']) is not None:
            return False #stop.
        else:
            return True #retry.
    else:
        return jsondata['return_object']

class LangAnalysis:
    """WiseNLU
    [ analysis_code ]
    형태소 분석 : “morp”,
    어휘의미 분석 (동음이의어 분석) : “wsd”
    어휘의미 분석 (다의어 분석) : “wsd_poly”
    개체명 인식 : “ner”
    의존 구문 분석 : “dparse”
    의미역 인식 : “srl”
    """
    def __init__(self, apicode):
        self.techname = __class__.__name__
        self.access_key = os.environ['ETRI_ACCESS_KEY']
        self.url = f"{OPEN_API_URI}/WiseNLU"
        self.verify_apicode(apicode)

    def verify_apicode(self, apicode):
        apicodes = ['morp','wsd','wsd_poly','ner','dparse','srl']
        if apicode in apicodes:
            self.apicode = apicode
        else:
            print(f"\n Your apicode({apicode}) is invalid.\n Available apicodes : {apicodes}")

    def api(self, text, maxLen=10000):
        if (hasattr(self,'apicode') is False) or (len(text) is 0):
            print(f"\n\n No have apicode OR len(text) is 0. --> ETRI로 요청 아예 안함.")
        else:
            requestJson = {
                "request_id": "reserved field",
                "access_key": self.access_key,
                "argument": {
                    "text": text[:maxLen],
                    "analysis_code": self.apicode}}
            http = urllib3.PoolManager()
            self.res = http.request(
                "POST",
                self.url,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                body=json.dumps(requestJson))
            return get_jsondata(self.res)

class LexicalRelationAnalysis:
    """어휘관계 분석 기술 WiseWWN = WiseWordNet
    [ sub-apis ]
    어휘 정보 | Word
    동음이의어 정보 | Homonym
    다의어 정보 | Polysemy
    어휘 간 유사도 분석 | WordRel
    """
    def __init__(self, apicode):
        self.techname = __class__.__name__
        self.access_key = os.environ['ETRI_ACCESS_KEY']
        self.verify_apicode(apicode)

    def verify_apicode(self, apicode):
        apicodes = ['Word','Homonym','Polysemy','WordRel']
        if apicode in apicodes:
            self.apicode = apicode
            self.url = f"{OPEN_API_URI}/WiseWWN/{self.apicode}"
        else:
            print(f"\n Your apicode({apicode}) is invalid.\n Available apicodes : {apicodes}")

    def api(self, word):
        if (hasattr(self,'apicode') is False) or (len(word) is 0):
            print(f"\n\n No have apicode OR len(word) is 0. --> ETRI로 요청 아예 안함.")
        else:
            requestJson = {
            	"access_key": self.access_key,
            	"argument": {
            		"word": word}}
            http = urllib3.PoolManager()
            self.res = http.request(
                "POST",
                self.url,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                body=json.dumps(requestJson))
            return get_jsondata(self.res)

#============================================================
"""Analyzer."""
#============================================================

#class ResultLoader:

def load_result(targetmodel, targetcol, techname, apicode, docid, method, type_regex):
    etri = models.ETRIAI(targetmodel, targetcol, techname, apicode)
    etri.load(filter={
        'docid':docid,
        'results':{'$elemMatch':{'sentence':{'$ne':None}}},
    })
    if len(etri.docs) is 0:
        print("\n len(etri.docs) is 0.")
    else:
        df = json_normalize(etri.docs,'results',['docid'])
        if len(df) is 0:
            print("\n json_normalize(etri.docs,'results',['docid']) is 0.")
        else:
            df = json_normalize(df.to_dict('records'),'sentence',['docid'])
            if len(df) is 0:
                print("\n json_normalize(df.to_dict('records'),method,['docid']) is 0.")
            else:
                df = json_normalize(df.to_dict('records'),method,['docid'])
                if 'type' in list(df.columns):
                    df = df[df.type.str.contains(pat=type_regex)]
                else:
                    print("\n 'type' not in list(df.columns).")
                return df
#"""
targetmodel = 'Article__네이버'
targetcol = 'headline'
techname = 'LangAnalysis'
apicode = 'srl'
docid = ObjectId('5c9bfe94639bfb5340fc6b67')
method = 'morp'
type_regex = '^NN[GP]'

#df = load_result(targetmodel, targetcol, techname, apicode, docid, method, type_regex)

def load_results(targetmodel, targetcol, techname, apicode, method, type_regex):
    """
    ************************************************************
     <class 'idebug.performance.Function'> | report_init
     caller : <ipython-input-6-2498b8afc3e9> | load_results
     visible_inputs : {'targetmodel': 'Article__네이버', 'targetcol': 'bodytext', 'techname': 'LangAnalysis', 'apicode': 'srl', 'docid': ObjectId('5c9bfe94639bfb5340fc6b67'), 'method': 'morp', 'type_regex': '^NN[GP]'}

    ************************************************************
     <class 'idebug.performance.Function'> | report_mid
     caller : <ipython-input-6-2498b8afc3e9> | load_results |  etri.load() 에 걸린시간.
     start_dt : 2019-04-29 23:27:10.463422+02:00
     end_dt : 2019-04-29 23:32:16.106041+02:00
     interval_runtime : 5.1_[mins]

    ************************************************************
     <class 'idebug.performance.Function'> | report_mid
     caller : <ipython-input-6-2498b8afc3e9> | load_results |  json_normalize() 에 걸린시간.
     start_dt : 2019-04-29 23:32:16.106041+02:00
     end_dt : 2019-04-29 23:38:01.344299+02:00
     interval_runtime : 5.8_[mins]

    ************************************************************
     <class 'idebug.performance.Function'> | report_mid
     caller : <ipython-input-6-2498b8afc3e9> | load_results |  new_df 변환에 걸린시간.
     start_dt : 2019-04-29 23:38:01.344299+02:00
     end_dt : 2019-04-29 23:38:12.595281+02:00
     interval_runtime : 11.3_[secs]

    ************************************************************
     <class 'idebug.performance.Function'> | report_fin
     caller : <ipython-input-6-2498b8afc3e9> | load_results | None
     start_dt : 2019-04-29 23:27:10.463422+02:00
     end_dt : 2019-04-29 23:38:12.595390+02:00
     runtime : 11.0_[mins]
    """
    fr = dbg.Function(inspect.currentframe()).report_init()
    etri = models.ETRIAI(targetmodel, targetcol, techname, apicode)
    etri.load({},{'_id':0,'docid':1,'results':1})
    fr.report_mid(addi_info=" etri.load() 에 걸린시간.")
    df = etri.get_df()
    df = json_normalize(etri.docs,'results',['docid'])
    df = json_normalize(df.to_dict('records'),'sentence',['docid'])
    df = json_normalize(df.to_dict('records'),method,['docid'])
    df = df[df.type.str.contains(pat=type_regex)]
    fr.report_mid(addi_info=" json_normalize() 에 걸린시간.")

    nouns = []
    for n,g in df.groupby('docid'):
        nouns.append({'docid':n, 'noun_txt':" ".join(list(g.lemma))})
    df = pd.DataFrame(nouns)
    fr.report_mid(addi_info=" new_df 변환에 걸린시간.")
    fr.report_fin()
    return df

#df = load_results(targetmodel, targetcol, techname, apicode, docid, method, type_regex)
