from SelectSetting import AllCoursesData
from SelectSetting import SelectNumberList
from SelectSetting import SelectCourse
from SelectSetting import CreditList
from SelectSetting import AddCourseABCD
from SelectSetting import CreditList
from SelectSetting import EnglishNameList
from SelectSetting import GEclassData
import csv
import os
import pandas as pd
import numpy as np
from itertools import accumulate

# 對照表
weekday_mapping = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4, 'S': 5}
number_mapping = {'1': 0, '2': 1, '3': 2, '4': 3, 'n': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12}

file_path = './data/cslearn.csv'
df = pd.read_csv(file_path)

df = pd.concat((df, pd.DataFrame({'中文課名':[EnglishNameList[0], EnglishNameList[1]], '科號':['-1','-1'], '類別':['1','1']})),  ignore_index=True)

# 創建字串陣列（8*7*13），初始值為 None
course_codes = np.full((8, 7, 13), None)

credit = [0 for i in range(0, 8)]
course_list = [pd.DataFrame() for i in range(8)]

result_df = pd.DataFrame()

AllCourses = []

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

        if row['科號'] == '-1':
            temp_max_rank_course = AllCoursesData.loc[AllCoursesData['中文課名'] == row['中文課名']]

        else:
            temp_max_rank_course = AllCoursesData.loc[AllCoursesData['科號'].astype(str).str.contains(str(row['科號']))]

        while True:
            if len(temp_max_rank_course) < rank_to_find:
                # print(row['中文課名'])
                break

            max_rank_course = temp_max_rank_course.nlargest(rank_to_find, '等級制').iloc[rank_to_find - 1:rank_to_find].copy()

            time = max_rank_course['上課時間'].iloc[0].replace(',', '')
            school_point = int(max_rank_course['學分'].iloc[0])

            time_mapping = [
                [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
                for i in range(0, len(time) - 1, 2)
            ]

            find_flag = False

            for semester in range(8):
                loop_flag = False
                if credit[semester] + school_point > CreditList[semester]:
                    continue

                for time in time_mapping:
                    if course_codes[semester, time[0], time[1]]:
                        loop_flag = True
                        break
                
                if not loop_flag and int((max_rank_course['科號'].iloc[0][-6])) == (semester >> 1) + 1:
                    for time in time_mapping:
                        course_codes[semester, time[0], time[1]] = max_rank_course['中文課名'].iloc[0]

                    credit[semester] += max_rank_course['學分'].iloc[0]
                    AllCourses.append(max_rank_course['科號'].iloc[0])
                    course_list[semester] = pd.concat([course_list[semester], max_rank_course], ignore_index = True)
                    result_df = pd.concat([result_df, max_rank_course], ignore_index = True)

                    find_flag = True

                    if type == 2:
                        ABCDsum += 1
                        if ABCDsum >= 3:
                            break
                        
                    break
            if find_flag:
                break

            rank_to_find += 1

# TODO: 校定必修(英文，通識，體育)
        
GEC1 = pd.DataFrame(GEclassData[GEclassData['通識分類'].str.contains('核心通識CoreGEcourses1')]).sort_values(by = ['等級制'], ascending = False)
GEC2 = pd.DataFrame(GEclassData[GEclassData['通識分類'].str.contains('核心通識CoreGEcourses2')]).sort_values(by = ['等級制'], ascending = False)
GEC3 = pd.DataFrame(GEclassData[GEclassData['通識分類'].str.contains('核心通識CoreGEcourses3')]).sort_values(by = ['等級制'], ascending = False)
GEC4 = pd.DataFrame(GEclassData[GEclassData['通識分類'].str.contains('核心通識CoreGEcourses4')]).sort_values(by = ['等級制'], ascending = False)

GE_list = []
GE_Credit = 0

for GEC in [GEC1, GEC2, GEC3, GEC4]:
    for index, row in GEC.iterrows():
        GE_flag = False
        for semester in range(8):

            if int(row['科號'][3]) & 1 != (semester + 1) & 1:
                continue

            if credit[semester] + row['學分'] > CreditList[semester]:
                continue

            time = row['上課時間'].replace(',', '')
            
            time_mapping = [
                [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
                for i in range(0, len(time) - 1, 2)
            ]

            loop_flag = False

            for time in time_mapping:
                if course_codes[semester, time[0], time[1]]:
                    loop_flag = True
                    break

            if loop_flag:
                break

            for time in time_mapping:
                course_codes[semester, time[0], time[1]] = row['中文課名']
            GE_list.append(row['科號'])
            GE_Credit += row['學分']
            credit[semester] += row['學分']
            result_df = pd.concat([result_df, row.to_frame().T], ignore_index = True)
            course_list[semester] = pd.concat([course_list[semester], row.to_frame().T.drop(columns = ['通識分類'])], ignore_index = True)
            GE_flag = True
            break
        if GE_flag:
            break

GE = GEclassData[~GEclassData['科號'].isin(GE_list)].sort_values(by = ['等級制'], ascending = False)

for index, row in GE.iterrows():
    if GE_Credit >= 20:
        break
    for semester in range(8):

        if int(row['科號'][3]) & 1 != (semester + 1) & 1:
            continue

        if credit[semester] + row['學分'] > CreditList[semester]:
            continue

        time = row['上課時間'].replace(',', '')
            
        time_mapping = [
            [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
            for i in range(0, len(time) - 1, 2)
        ]

        loop_flag = False

        for time in time_mapping:
            if course_codes[semester, time[0], time[1]]:
                loop_flag = True
                break

        if loop_flag:
            break

        for time in time_mapping:
            course_codes[semester, time[0], time[1]] = row['中文課名']
        GE_list.append(row['科號'])
        GE_Credit += row['學分']
        credit[semester] += row['學分']
        result_df = pd.concat([result_df, row.to_frame().T], ignore_index = True)
        course_list[semester] = pd.concat([course_list[semester], row.to_frame().T.drop(columns = ['通識分類'])], ignore_index = True)
        GE_flag = True
        break

##### 電機資訊專業選修
# TODO: 
target_prefixes = ['EE', 'CS', 'ISA', 'COM']
AllSelectedCourse = pd.DataFrame()
selected_credit = 0

for prefix in target_prefixes:

    prefix_courses = AllCoursesData[AllCoursesData['科號'].str.contains(prefix)]

    prefix_courses = prefix_courses[~prefix_courses['科號'].isin(result_df['科號'].values)]

    AllSelectedCourse = pd.concat([AllSelectedCourse, prefix_courses], ignore_index = True)

AllSelectedCourse = AllSelectedCourse.sort_values(by = ['等級制'], ascending = False)
AllSelectedCourse = AllSelectedCourse[~AllSelectedCourse['中文課名'].str.contains('專題')]
AllSelectedCourse = AllSelectedCourse[~AllSelectedCourse['中文課名'].str.contains('書報討論')]

for index, row in AllSelectedCourse.iterrows():
    if selected_credit > 12:
        break
    for semester in range(8):
        if int(row['科號'][-6]) != (semester >> 1) + 1:
            continue

        if int(row['科號'][3]) & 1 != (semester + 1) & 1:
            continue

        if credit[semester] + row['學分'] > CreditList[semester]:
            continue

        time = row['上課時間'].replace(',', '')
        
        time_mapping = [
            [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
            for i in range(0, len(time) - 1, 2)
        ]

        loop_flag = False

        for time in time_mapping:
            if course_codes[semester, time[0], time[1]]:
                loop_flag = True
                break

        if loop_flag:
            break

        for time in time_mapping:
            course_codes[semester, time[0], time[1]] = row['中文課名']
        selected_credit += row['學分']
        credit[semester] += row['學分']
        result_df = pd.concat([result_df, row.to_frame().T], ignore_index = True)
        course_list[semester] = pd.concat([course_list[semester], row.to_frame().T], ignore_index = True)
        break

# TODO: 其餘選修
    
if '1' in SelectNumberList and '2' in SelectNumberList:
    Other = AllCoursesData[AllCoursesData['科號'].str.contains('MATH') | AllCoursesData['科號'].str.contains('STAT') | AllCoursesData['科號'].str.contains('PHYS')]

elif '1' in SelectNumberList:
    Other = AllCoursesData[AllCoursesData['科號'].str.contains('MATH') | AllCoursesData['科號'].str.contains('STAT')]

elif '2' in SelectNumberList:
    Other = AllCoursesData[AllCoursesData['科號'].str.contains('PHYS')]

else:
    Other = AllCoursesData[~(AllCoursesData['科號'].str.contains('MATH') | AllCoursesData['科號'].str.contains('STAT') | AllCoursesData['科號'].str.contains('PHYS'))]

Other = Other[~Other['科號'].isin(result_df['科號'].values)].sort_values(by = ['等級制'], ascending = False)

for index, row in Other.iterrows():
    for semester in range(8):
        if int(row['科號'][-6]) != (semester >> 1) + 1:
            continue

        if int(row['科號'][3]) & 1 != (semester + 1) & 1:
            continue

        if credit[semester] >= CreditList[semester]:
            continue

        time = row['上課時間'].replace(',', '')
        
        time_mapping = [
            [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
            for i in range(0, len(time) - 1, 2)
        ]

        loop_flag = False

        for time in time_mapping:
            if course_codes[semester, time[0], time[1]]:
                loop_flag = True
                break

        if loop_flag:
            break

        for time in time_mapping:
            course_codes[semester, time[0], time[1]] = row['中文課名']
        selected_credit += row['學分']
        credit[semester] += row['學分']
        result_df = pd.concat([result_df, row.to_frame().T], ignore_index = True)
        course_list[semester] = pd.concat([course_list[semester], row.to_frame().T], ignore_index = True)
        break

# 顯示最高等級的課程
# print("最高等級制的課程:")
# print(result_df)

# TODO: print出每學期課表
# Print out each semester's schedule
for semester in range(8):
    print(f"Semester {semester + 1}: {credit[semester]}")
    for day in range(7):
        day_schedule = []
        for period in range(13):
            course_code = course_codes[semester, day, period]
            if isinstance(course_code, pd.Series):
                # If course_code is a Series, take the first item
                course_code = course_code.iloc[0]
            if course_code:
                day_schedule.append(str(course_code))  # Ensure it's a string
            else:
                day_schedule.append("--")
        print("Day {}: {}".format(day, ' '.join(day_schedule)))
    print("\n")

for course in course_list:
    print(course)

print("總學分： ", list(accumulate(credit))[7])