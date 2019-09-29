#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
import json
import logging
import sys
import os
from sys import path
from Num2Word import Num2Word
from XunFeiTTS import XunFeiTTS
import Config as Config

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
    format='%(levelname)s:%(asctime)s:%(message)s'
)

class RespBody():
    # d = "{\"code\":0,\"data\":{\"city\":{\"cityId\":50,\"counname\":\"中国\",\"name\":\"闵行区\",\"pname\":\"上海市\",\"timezone\":\"8\"},\"forecast\":[{\"conditionDay\":\"多云\",\"conditionIdDay\":\"1\",\"conditionIdNight\":\"31\",\"conditionNight\":\"多云\",\"predictDate\":\"2018-10-17\",\"tempDay\":\"23\",\"tempNight\":\"14\",\"updatetime\":\"2018-10-17 22:09:00\",\"windDirDay\":\"北风\",\"windDirNight\":\"北风\",\"windLevelDay\":\"3-4\",\"windLevelNight\":\"3-4\"},{\"conditionDay\":\"多云\",\"conditionIdDay\":\"1\",\"conditionIdNight\":\"31\",\"conditionNight\":\"多云\",\"predictDate\":\"2018-10-18\",\"tempDay\":\"21\",\"tempNight\":\"12\",\"updatetime\":\"2018-10-17 22:09:00\",\"windDirDay\":\"北风\",\"windDirNight\":\"北风\",\"windLevelDay\":\"5-6\",\"windLevelNight\":\"3-4\"},{\"conditionDay\":\"多云\",\"conditionIdDay\":\"1\",\"conditionIdNight\":\"31\",\"conditionNight\":\"多云\",\"predictDate\":\"2018-10-19\",\"tempDay\":\"22\",\"tempNight\":\"13\",\"updatetime\":\"2018-10-17 22:09:00\",\"windDirDay\":\"东北风\",\"windDirNight\":\"东北风\",\"windLevelDay\":\"3-4\",\"windLevelNight\":\"3\"}]},\"msg\":\"success\",\"rc\":{\"c\":0,\"p\":\"success\"}}"
    # 利用__dict__将返回的json转换为字典
    def __init__(self, d) -> None:
        self.__dict__ = d

class Forecast():
    def __init__(self, d) -> None:
        self.prdict_date = d.predictDate # yyyy-MM-dd
        self.update_time = d.updatetime # yyyy-MM-dd HH:mm:ss
        self.condition_day = d.conditionDay # 多云
        self.condition_night = d.conditionNight # 多云
        self.temp_day = d.tempDay # 23
        self.temp_night = d.tempNight # 14
        self.wind_dir_day = d.windDirDay # 北风
        self.wind_dir_night = d.windDirNight # 北风
        self.wind_level_day = d.windLevelDay # 3-4
        self.wind_level_night = d.windLevelNight # 4

    def wind_level_to_word(self, wind_level):
        """
        将风力等级转为中文文字
        :param wind_level: 风力等级 传入3-4
        :return: 返回三至四
        """
        wind_level = str(wind_level)
        if not wind_level.__contains__('-'):
            return Num2Word.to_word(wind_level)
        return Num2Word.to_word(wind_level.split('-')[0]) + '至' + Num2Word.to_word(wind_level.split('-')[1])

    def to_chinese(self):
        """
        将天气遇到转为中文文字
        :return:
        """
        month = self.prdict_date.split('-')[1]
        day = self.prdict_date.split('-')[2]
        date_word = Num2Word.to_word(month) + '月' + Num2Word.to_word(day) + '日'
        return "%s, 白天天气%s, 温度%s度, %s%s级, 夜间天气%s, 温度%s度, %s%s级" % \
              (date_word, self.condition_day, Num2Word.to_word(self.temp_day), self.wind_dir_day, self.wind_level_to_word(self.wind_level_day),
               self.condition_night, Num2Word.to_word(self.temp_night), self.wind_dir_night, self.wind_level_to_word(self.wind_level_night))

class MoJiWeather():
    def __init__(self) -> None:
        self.config = {
            "baseURL": "http://freecityid.market.alicloudapi.com",
            "forecastURL": "/whapi/json/alicityweather/briefforecast3days",
            "AppCode": Config.ALI_APP_CODE,
            "headers": {
                "Host":"freecityid.market.alicloudapi.com",
                "gateway_channel":"http",
                "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
                "Authorization":"APPCODE " + Config.ALI_APP_CODE  # 注意要注意一下 APPCODE 后面有一个空格
            },
            "token": Config.ALI_TOKEN
        }
        self.city_codes = {
            "BeiJing": "2",
            "ShangHaiMinHang": "50"
        }

    def fetch_forecast(self, cityId):
        req_body = {
            "cityId": str(cityId),
            "token": self.config["token"]
        }
        json_str = json.dumps(req_body)
        url = self.config["baseURL"] + self.config["forecastURL"]
        # print(url)
        # print(self.config["headers"])
        resp = requests.post(url=url, data=req_body, headers=self.config["headers"])
        resp_json = resp.content.decode('utf8')
        # print(resp_json)
        # print(resp.headers)
        logging.debug("[MoJiWeather.fetch_forecast] - status = %s" % resp.status_code)
        logging.debug("[MoJiWeather.fetch_forecast] - resp json = %s" % resp_json)

        resp_body = json.loads(resp_json, object_hook=RespBody)

        code = resp_body.code
        if code == 0:
            data = resp_body.data
            city = data.city
            province_name = city.pname
            city_name = city.name
            logging.info("[MoJiWeather.fetch_forecast] - %s, %s" % (province_name, city_name))

            three_days_forecast_list = data.forecast
            return three_days_forecast_list
        else:
            logging.info("[MoJiWeather.fetch_forecast] - Resp Not Success")
            return []


if __name__ == '__main__':
    mo_ji_weather = MoJiWeather()
    forecast_list = mo_ji_weather.fetch_forecast(mo_ji_weather.city_codes["ShangHaiMinHang"])

    print(forecast_list)

    xun_fei_tts = XunFeiTTS()
    s = ""
    forecast_words = []
    for forecast in forecast_list:
        f = Forecast(forecast)
        forecast_words.append(f.to_chinese())
        print(f.to_chinese())
    s = ",".join(forecast_words)
    logging.debug("[MojiWeather.main] - %s" % s)
    xun_fei_tts.fetch_voice_and_play(s)
    pass


