from SelectSetting import AllCoursesData
import pandas as pd
import numpy as np

# 對照表
weekday_mapping = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4, 'S': 5}
number_mapping = {'1': 0, '2': 1, '3': 2, '4': 3, 'n': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12}

file_path = './data/cslearn.csv'
df = pd.read_csv(file_path)

# 中文課名, 科號, 類別
MustclassData = df[(df['類別'] == '1') | (df['類別'] == 'X') | (df['類別'].isin(['A', 'B', 'C', 'D']))]
MustclassData = MustclassData[['科號', '中文課名', '類別']].reset_index(drop=True)

# 創建布爾陣列（8*7*13），初始值為 False
time_available = np.full((8, 7, 13), False, dtype=bool)

highest_ranked_courses = []

##### 系訂必修+大學中文
for category in ['1', 'X']:
    category_data = MustclassData[MustclassData['類別'] == category]
    for index, row in category_data.iterrows():
        rank_to_find = 1
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

            # 將上課時間映射到數字
            time_mapping = [
                [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
                for i in range(0, len(time) - 1, 2)
            ]   
            # 檢查上課時間是否為 False
            # 檢查 time_available 是否為 False
            find_flag = False
            for i in range(8):
                for j in range(len(time_mapping)):
                    if time_available[i, time_mapping[j][0], time_mapping[j][1]] == True:
                        break
                # 更新 time_available，將對應的時間標記為 True
                for j in range(len(time_mapping)):
                    time_available[i, time_mapping[j][0], time_mapping[j][1]] = True
                # 將找到的課程加入最終列表
                highest_ranked_courses.append(max_rank_course)
                find_flag = True
                break
            if find_flag:
                break

            # 找下一個等級制最高的課程
            rank_to_find += 1

##### 專業課程ABCD類
# TODO: 目前是所有ABCD類的每一堂課程都會找出最高分
# 應該要ABCD類至少選3類，學分加起來12
for category in ['A', 'B', 'C', 'D']:
    category_data = MustclassData[MustclassData['類別'] == category]
    # 如果該類別沒有課程，則繼續下一個類別
    for index, row in category_data.iterrows():
        rank_to_find = 1
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

            # 將上課時間映射到數字
            time_mapping = [
                [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
                for i in range(0, len(time) - 1, 2)
            ]   
            # 檢查上課時間是否為 False
            # 檢查 time_available 是否為 False
            find_flag = False
            for i in range(8):
                for j in range(len(time_mapping)):
                    if time_available[i, time_mapping[j][0], time_mapping[j][1]] == True:
                        break
                # 更新 time_available，將對應的時間標記為 True
                for j in range(len(time_mapping)):
                    time_available[i, time_mapping[j][0], time_mapping[j][1]] = True
                # 將找到的課程加入最終列表
                highest_ranked_courses.append(max_rank_course)
                find_flag = True
                break
            if find_flag:
                break

            # 找下一個等級制最高的課程
            rank_to_find += 1

##### 電機資訊專業選修
# TODO: 
# target_prefixes = ['EE', 'CS', 'ISA', 'COM']
# selected_credit = 0

# for prefix in target_prefixes:
#     prefix_courses = AllCoursesData[AllCoursesData['科號'].str.startswith(prefix)]
#     # 根據等級制對所有該前綴的課程進行排序
#     prefix_courses = prefix_courses.sort_values('等級制', ascending=False)

#     for index, row in prefix_courses.iterrows():
#         if selected_credit + row['學分'] > 21:
#             continue  # 如果加上這門課的學分超過21，跳過這門課

#         # 將上課時間映射到數字
#         time = row['上課時間'].replace(',', '')
#         time_mapping = [
#             [weekday_mapping[time[i]], number_mapping[time[i + 1]]]
#             for i in range(0, len(time) - 1, 2)
#         ]

#         # 檢查上課時間是否衝突
#         conflict = False
#         for i in range(8):
#             for j in range(len(time_mapping)):
#                 if time_available[i, time_mapping[j][0], time_mapping[j][1]]:
#                     conflict = True
#                     break
#             if conflict:
#                 break

#         if not conflict:
#             # 如果沒有衝突，標記該課程的時間為佔用，並加入最終列表
#             for j in range(len(time_mapping)):
#                 time_available[i, time_mapping[j][0], time_mapping[j][1]] = True
#             highest_ranked_courses.append(row)
#             selected_credit += row['學分']
#             break  # 找到符合條件的課程後，跳出循環

#         if selected_credit >= 21:
#             break  # 如果已經達到21學分，跳出循環

# 將結果轉換為 DataFrame
result_df = pd.concat(highest_ranked_courses, ignore_index=True)

# TODO: 校定必修(英文，通識，體育)

# TODO: 其餘選修

# 顯示最高等級的課程
print("最高等級制的課程:")
print(result_df)

# TODO: print出每學期課表