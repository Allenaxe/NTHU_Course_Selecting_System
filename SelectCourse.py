from SelectSetting import AllCoursesData
from SelectSetting import SelectType
from SelectSetting import SelectCourse
from SelectSetting import CreditList
from SelectSetting import AddCourseABCD
from SelectSetting import CreditList
import csv
import os
import pandas as pd
import numpy as np

# 對照表
weekday_mapping = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4, 'S': 5}
number_mapping = {'1': 0, '2': 1, '3': 2, '4': 3, 'n': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12}

file_path = './data/cslearn.csv'
df = pd.read_csv(file_path)

# 創建布爾陣列（8*7*13），初始值為 False
time_available = np.full((8, 7, 13), False, dtype=bool)
highest_ranked_courses = []
sum = []
for i in range(8):
    sum.append(0)
#print(SelectCourse , SelectType)

ABCDsum = 0
for type in range(3):
    MustclassData = []

    if type == 0:
        # 中文課名, 科號, 類別
        MustclassData = df[df['類別'] == '1'].dropna(subset=['中文課名', '科號'])
        MustclassData = MustclassData[['科號', '中文課名']].reset_index(drop=True)
    elif type == 1:
        # 中文課名, 科號, 類別
        MustclassData = df[df['類別'] == SelectCourse].dropna(subset=['中文課名', '科號'])
        MustclassData = MustclassData[['科號', '中文課名']].reset_index(drop=True)
    elif type == 2:
        MustclassData = AddCourseABCD

    for index, row in MustclassData.iterrows():
        rank_to_find = 1
        #print("rank_to_find ", rank_to_find,"type = ",type)
        if row['科號'] == '-1':
            temp_max_rank_course = AllCoursesData.loc[AllCoursesData['中文課名'] == row['中文課名']]
        else:
            temp_max_rank_course = AllCoursesData.loc[AllCoursesData['科號'].astype(str).str.contains(str(row['科號']))]
        while True:
            if len(temp_max_rank_course) < rank_to_find:
                break
            max_rank_course = temp_max_rank_course.nlargest(rank_to_find, '等級制').iloc[rank_to_find - 1:rank_to_find].copy()
            # 將上課時間映射到數字

            time = max_rank_course['上課時間'].iloc[0].replace(',', '')
            school_point = int(max_rank_course['學分'].iloc[0])

            # 將上課時間映射到數字
            time_mapping = [
                [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
                for i in range(0, len(time) - 1, 2)
            ]   
            # 檢查上課時間是否為 False
            # 檢查 time_available 是否為 False
            find_flag = False
            for i in range(8):
                if sum[i] + school_point > CreditList[i]:
                    continue 
                for j in range(len(time_mapping)):
                    if time_available[i, time_mapping[j][0], time_mapping[j][1]] == True:
                        break
                # 更新 time_available，將對應的時間標記為 True
                for j in range(len(time_mapping)):
                    time_available[i, time_mapping[j][0], time_mapping[j][1]] = True
                # 將找到的課程加入最終列表
                highest_ranked_courses.append(max_rank_course)
                find_flag = True
                if type == 2:
                    ABCDsum += 1
                    if ABCDsum >= 3:
                        break
                break
            if find_flag:
                break

            # 找下一個等級制最高的課程
            rank_to_find += 1




# 將結果轉換為 DataFrame
result_df = pd.concat(highest_ranked_courses, ignore_index=True)

# 顯示最高等級的課程
print("最高等級制的課程:")
print(result_df)
