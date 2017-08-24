# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
import re
from collections import Counter
class DictInfer(object):
    def __init__(self, Dict_Infer):
        self.Dict_Infer = Dict_Infer

    def sex_infer(self,num, words1, source_name):
        result = '相关信息不足'
        count1 = 0
        count21 = 0
        count22 = 0
        for item in self.Dict_Infer['female']['certain']:
            if item in words1:
                count21 = count21 + 1
            elif item in source_name:
                count21 = count21 + 1
        for item in self.Dict_Infer['male']:
            if item in words1:
                count1 = count1 + 1
        for item in self.Dict_Infer['female']['positive']:
            if item in words1:
                count22 = count22 + 1
            elif item in source_name:
                count22 = count22 + 1
        if count21 != 0:
            result = '女'
        elif count21 == 0:
            if count1 >= 2:
                result = '男'
            elif count22 >= 2:
                result = '女'
            elif count22 <= 1:
                result = '相关信息不足'
            else:
                result = '相关信息不足'
        if result == '男' and num <30:
            result = '相关信息不足'
        return result

    def location_infer(self, life_concern, work_concern, source_name):
        location = '相关信息不足'
        loc_count = {}

        for k in self.Dict_Infer['location'].keys():
            loc_count[k] = 0
        for line1 in life_concern:
            if line1[0].year >= 2015:
                for k,v in self.Dict_Infer['location'].items():
                    for item in v:
                        if item in line1[1]:
                            loc_count[k] = loc_count[k] + 1
        for line2 in work_concern:
            if line2[0].year >= 2015:
                for k,v in self.Dict_Infer['location'].items():
                    for item in v:
                        if item in line2[1]:
                            loc_count[k] = loc_count[k] + 0.5
        for line3 in source_name:
            if line3[0].year >= 2015:
                for k,v in self.Dict_Infer['location'].items():
                    for item in v:
                        if item in line3[1]:
                            loc_count[k] = loc_count[k] + 2

        sort_loc_count = sorted(loc_count.items(), key=lambda item:item[1], reverse=True)
        count = sort_loc_count[0][1]
        if count <= 4:
             result = location
        else:
             result = sort_loc_count[0][0]
        return result

    def kid_infer(self, num, words1, words2, source_name):
        count1 = 0
        count2 = 0
        result = '相关信息不足'

        for item in self.Dict_Infer['kids']:
            if item in words1:
                count1 = count1 + 1
            if item in words2:
                count1 = count1 + 1
            if item in source_name:
                count2 = count2 + 1
        if count1 == 1 and count2 == 1:
            result = '50%几率 有孩子'
        elif count1 > 1 or count2 > 1:
            result = '有孩子'
        else:
            result = '没有孩子'
        if result == '没有孩子' and num <= 30:
            result = '相关信息不足'
        return result

    def university_infer(self, words1, source_name):
        result = '相关信息不足'
        for item in source_name:
            if item in self.Dict_Infer['university']:
                result = item
            elif '大学校友会' in item:
                result = item[:-3]
            elif '大学学生会' in item:
                result = item[:-3]
            elif '大学研究生' in item:
                result = item[:-3]
            elif '大学研究生会' in item:
                result = item[:-4]
            elif '团委' in item:
                result = item[:-2]
            elif '大学学生事务中心' in item:
                result = item[:-6]
            elif '校友中心' in item:
                result = item[:-4]
        return result

    def marriage_infer(self, num, words1, kid):
        result = '相关信息不足'
        if num >= 30:
            if kid == '有孩子':
                result = '已婚'
            else:
                for item in self.Dict_Infer['marriage']:
                    if item in words1:
                        result = '已婚'
                        break
                if result == '相关信息不足':
                    result = '未婚'
        return result

    def kid_age_infer(self,words1):
        kid_age = '相关信息不足'
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0

        for item in self.Dict_Infer['kids_age']['level1']:
            if item in words1:
                count1 = count1 + 1
        for item in self.Dict_Infer['kids_age']['level2']:
            if item in words1:
                count2 = count2 + 1
        for item in self.Dict_Infer['kids_age']['level3']:
            if item in words1:
                count3 = count3 + 1
        for item in self.Dict_Infer['kids_age']['level4']:
            if item in words1:
                count4 = count4 + 1
        if count4 == max([count1, count2, count3, count4]):
            kid_age = '16-20'
        elif count3 == max([count1, count2, count3, count4]):
            kid_age = '11-15'
        elif count2 == max([count1, count2, count3, count4]):
            kid_age = '6-10'
        elif count1 == max([count1, count2, count3, count4]):
            kid_age = '1-5'
        return kid_age

    def age_infer(self, num, words1,source_name,kid, marriage):
        age = '相关信息不足'
        count = 0
        if kid == '相关信息不足':
            age = '相关信息不足'
        if kid == '没有孩子':
            if marriage == '未婚':
                age = '22-27'
            elif marriage == '已婚':
                age = '27-32'
        elif kid == '有孩子':
            kid_age = self.kid_age_infer(words1)
            if kid_age == '1-5':
                age = '27-32'
            elif kid_age == '6-10':
                age = '32-37'
            elif kid_age == '11-15':
                age = '37-42'
            elif kid_age == '16-20':
                age = '42岁以上'
            else:
                age = '30-40'
        for item in self.Dict_Infer['senior']:
            if item in words1:
                count = count+1
        if count >=1:
            age = '55岁以上'
            kid = '有孩子'
            marriage = '已婚'
        if age=='相关信息不足' and num <=30:
            age = '相关信息不足'
        return (kid, marriage, age)

    def graduation_infer(self, num, words1, source_name):
        graduation = '相关信息不足'
        count = 0
        if num >= 30:
            if self.university_infer(words1, source_name) != '相关信息不足':
                graduation = '拥有大学文凭'
            else:
                for item in self.Dict_Infer['graduation']:
                    if item in words1:
                        count = count + 1
                if count >= 1:
                    graduation = '拥有大学文凭'
                else:
                    graduation = '相关信息不足'
        return graduation

    def important_time(self, life_concern):
        age = '未提及'
        university = '未提及'
        text1 = r'毕业\S+年'
        text2 = r'\S+年毕业'
        pattern1 = re.compile(text1.decode('utf-8'))
        pattern2 = re.compile(text2.decode('utf-8'))
        for line in life_concern:
            if re.search(pattern1, line[1]) is not None:
                try:
                    year1 = re.search(r'\d+', re.search(pattern1, line[1]).group()).group()
                    age = int(year1) + 22
                    for k in self.Dict_Infer['university'].keys():
                        for item in self.Dict_Infer['university'][k]:
                            if item in line[1]:
                                university = k
                except(AttributeError):
                    pass
            elif re.search(pattern2, line[1]) is not None:
                try:
                    year2 = re.search(r'\d+', re.search(pattern1, line[1]).group()).group()
                    age = 117 - int(year2) + 22
                except(AttributeError):
                    pass
            if 25 <= age < 30:
                age = '27-32'
            elif 32 <= age < 37:
                age = '32-37'
            elif 37 <= age < 42:
                age = '37-42'
            elif 42 <= age:
                age = '42岁以上'
        return (age, university)

    def car_infer(self, num, words1,source_name, income):
        result = '相关信息不足'
        count = 0
        for item in self.Dict_Infer['cars']:
            if item in words1:
                count = count + 1
            elif item in source_name:
                count = count + 1
        if count >= 2:
            result = '有车'
        elif count == 1:
            result = '50% 几率有车'
        elif income == '月收入至少2万以上':
            result = '有车'
        elif income == '':
            result = '50% 几率有车'
        elif income == '月收入1万以下':
            result = '没有车'
        if result == '没有车' and num<=30:
            result = '相关信息不足'
        return result

    def house_infer(self, num, words1, source_name):
        result = '相关信息不足'
        count = 0

        for item in self.Dict_Infer['house']:
            if item in words1:
                count = count + 1
            elif item in source_name:
                count = count + 1
        if count >= 2:
            result = '有住房'
        elif count == 1:
            result = '50% 几率有住房'
        elif count == 0:
            result = '无法确定是否有住房'

        if result == '无法确定是否有住房' and num <= 30:
            result = '相关信息不足'
        return result

    def income_infer(self, num, words1, house, location):
        result = '相关信息不足'
        count1 = 0
        count2 = 0
        count3 = 0
        for item in self.Dict_Infer['income']['level3']:
            if item in words1:
                count3 = count3 + 1
        for item in self.Dict_Infer['income']['level2']:
            if item in words1:
                count2 = count2 + 1
        for item in self.Dict_Infer['income']['level1']:
            if item in words1:
                count1 = count1 + 1
        if count3 >= 3:
            result = '月收入至少2万以上'
        elif location in ['北京','上海','广州','深圳'] and house == '有住房':
            result = '月收入至少2万以上'
        elif location in ['北京', '上海', '广州', '深圳'] and house == '50% 几率有住房':
            result = '月收入至少在1万到2万之间'
        elif count2 >= 3:
            result = '月收入至少在1万到2万之间'
        else:
            result = '月收入1万以下'

        if result == '月收入1万以下' and num <= 30:
            result = '相关信息不足'
        return result

    @staticmethod
    def time_infer(time):
        hour = []
        for item in time:
            hour.append(item.hour)
        hour_new = Counter(hour)
        point = [22,23,0,1,2,3,4,5,6,7,8]
        sleep = []
        wake_up = []
        count1 = 0
        count2 = 0
        sleep_time = 0
        wake_up_time = 0
        for i in range(1,10):
            if hour_new[point[i]] < hour_new[point[i-1]] and hour_new[point[i]] > hour_new[point[i+1]]:
                sleep.append(point[i])

                count1 = count1 + hour_new[point[i]]

            if hour_new[point[i]] > hour_new[point[i-1]] and hour_new[point[i]] < hour_new[point[i+1]]:
                wake_up.append(point[i])
                count2 = count2 + hour_new[point[i]]

        for item1 in sleep:
            if item1 < 12:
                sleep_time += (item1+24) * float(hour_new[item1])/float(count1)
            else:
                sleep_time += item1 * float(hour_new[item1])/float(count1)

        for item2 in wake_up:
            wake_up_time += item2 * float(hour_new[item2])/float(count2)
        return (sleep_time+0.5, wake_up_time-0.5)
