import pandas as pd
import streamlit as st
import time
import numpy as np



def choose_departments():
    global counter
    ### 選擇科系
    st.sidebar.header("選擇科系")
    st.sidebar.write("請選擇想額外修習的科系(預設已包含資工系、電資學院、通識、英語、大學中文)")
    st.sidebar.write("1 數學系     2 物理系   3 無額外修習其他系")
    counter += 1

    key = f"input{counter}"
    SelectNumber = st.sidebar.text_input("請輸入科系代碼(多選請以空白為間隔並以換行為結束):",key=key,value=3)
    SelectNumberList = SelectNumber.split(" ")


    ##確認輸入無誤
    counter += 1
    key = f"input{counter}"
    if st.sidebar.button("Submit",key=key):
        if "3" in SelectNumberList and len(SelectNumberList) > 1:
            st.error("科系代碼輸入有誤 請重新輸入")
        elif "1" not in SelectNumberList and "2" not in SelectNumberList and "3" not in SelectNumberList:
            st.error("科系代碼輸入有誤 請重新輸入")
        else:
            st.toast('輸入成功', icon='💾')

    return SelectNumberList

def enter_expected_credits():
    global counter
    ### 輸入各學期學分
    st.sidebar.header("請輸入從大一上至大四下各學期的期望修習學分")
    
    counter += 1
    key = f"input{counter}"
    CreditList = [None] * 8
    CreditList[0] = int(st.sidebar.number_input("請輸入大一上期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[1] = int(st.sidebar.number_input("請輸入大一下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[2] = int(st.sidebar.number_input("請輸入大二下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[3] = int(st.sidebar.number_input("請輸入大二下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[4] = int(st.sidebar.number_input("請輸入大三下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[5] = int(st.sidebar.number_input("請輸入大三下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[6] = int(st.sidebar.number_input("請輸入大四下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"
    CreditList[7] = int(st.sidebar.number_input("請輸入大四下期望修習學分:",key=key,value=0))
    counter += 1
    key = f"input{counter}"


    ###確認輸入無誤
    counter += 1
    key = f"input{counter}"
    if st.sidebar.button("Submit",key=key):
        lesszero_flag = False
        CreditSum = 0
        for x in CreditList:
            if x < 0:
                lesszero_flag = True
            CreditSum += x
        if CreditSum < 128 and not lesszero_flag:
            st.error("期望修習總學分低於128 請重新輸入")
        elif lesszero_flag:
            st.error("期望修習學分不能小於0 請重新輸入")
        else:
            st.sidebar.write("總學分為:", CreditSum)
            st.toast('輸入成功', icon='💾')
  

    return CreditList


def filter_and_concat_courses(df,SelectNumberList):
    

    ###讀取各系資料並排除資料欄有空缺的課
    ###資工系課
    CSclassData = df[df['系所全名'] == '資訊工程學系'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    CSclassData['教師'] = CSclassData['教師'].fillna('')
    CSclassData['等級制'] = CSclassData['等級制'].fillna(0)
    CSclassData = CSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(CSclassData)

    ###電資院課
    EECSclassData = df[df['系所全名'] == '電機資訊學院學士班'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    EECSclassData['教師'] = EECSclassData['教師'].fillna('')
    EECSclassData['等級制'] = EECSclassData['等級制'].fillna(0)
    EECSclassData = EECSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(EECSclassData)

    ###通識課
    GEclassData = df[df['系所全名'] == '通識教育中心'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    GEclassData['教師'] = GEclassData['教師'].fillna('')
    GEclassData['等級制'] = GEclassData['等級制'].fillna(0)
    GEclassData = GEclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(GEclassData)

    ###英文課
    LANGclassData = df[df['系所全名'] == '英語教育中心(110起)'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    LANGclassData['教師'] = LANGclassData['教師'].fillna('')
    LANGclassData['等級制'] = LANGclassData['等級制'].fillna(0)
    LANGclassData = LANGclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(LANGclassData)

    ###大學中文
    CLclassData = df[(df['系所全名'] == '中國文學系') & (df['中文課名'] == '大學中文')].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    CLclassData['教師'] = CLclassData['教師'].fillna('')
    CLclassData['等級制'] = CLclassData['等級制'].fillna(0)
    CLclassData =CLclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(CLclassData)

    AllCoursesData = pd.concat([CSclassData, EECSclassData, GEclassData, LANGclassData, CLclassData], ignore_index=True)
    #print(AllCoursesData)

    ###數學課
    if "1" in SelectNumberList:
        MATHclassData = df[df['系所全名'] == '數學系'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
        MATHclassData['教師'] = MATHclassData['教師'].fillna('')
        MATHclassData['等級制'] = MATHclassData['等級制'].fillna(0)
        MATHclassData = MATHclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
        #print(MATHclassData)
        AllCoursesData = pd.concat([AllCoursesData, MATHclassData], ignore_index=True)
        #print(AllCoursesData)

    ###物理課
    if "2" in SelectNumberList:
        PHYSclassData = df[df['系所全名'] == '物理學系'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
        PHYSclassData['教師'] = PHYSclassData['教師'].fillna('')
        PHYSclassData['等級制'] = PHYSclassData['等級制'].fillna(0)
        PHYSclassData = PHYSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
        #print(PHYSclassData)
        AllCoursesData = pd.concat([AllCoursesData, PHYSclassData], ignore_index=True)
        #print(AllCoursesData)

    return AllCoursesData




counter = 1     #用來識別button key和input key
st.set_page_config(page_title="NTHU Course Selecting System", page_icon=":rocket:", layout="wide")
st.sidebar.markdown("<div style='text-align: center; font-size: 30px;'>設定</div>", unsafe_allow_html=True)
st.title("NTHU Course Selecting System")
st.divider()
###選科系
SelectNumberList = choose_departments()
###選每學期期望學分
expected_credits = enter_expected_credits()
###讀取Excel檔案
file_path = './data/all_done.csv'
df = pd.read_csv(file_path)
###得到可選擇課程
AllCoursesData = filter_and_concat_courses(df,SelectNumberList)


counter += 1
key = f"input{counter}"
if st.button("顯示符合需求的課程",key=key):
    #載入條
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1, f'載入中 {i+1} %')
        time.sleep(0.01)
    #顯示符合需求課程
    time.sleep(0.3)
    st.dataframe(AllCoursesData)








### 拿SelectCourse.py test

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
# print("最高等級制的課程:")
# print(result_df)
# print(result_df.iloc[0])
# print(result_df.iloc[0]['中文課名'])
# print(result_df['中文課名'])
# print(result_df['教師'])
# print(result_df['上課時間'])

# TODO: print出每學期課表









def set_null_time_schedule():
    ###設定一個空的時間表df
    schedule_data = {
        # 'Time': ['1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a','b','c'],
        'M': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'T': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'W': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'R': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'F': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'S': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    }
    df_schedule = pd.DataFrame(schedule_data)
    new_index = ('1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c')
    df_schedule.set_index(pd.Index(new_index), inplace=True)
    return df_schedule


### 處理上課時間的逗號
for idx in range(0,len(result_df['上課時間'])):
    result_df['上課時間'][idx] =  result_df['上課時間'][idx].replace(',', '')
    # print(result_df['上課時間'])

counter += 1
key = f"input{counter}"
if st.button("顯示推薦課表",key=key):
    
    # #test
    # df_schedule = set_null_time_schedule()
    # print(df_schedule)
    # print(df_schedule['M']['1'])


    ###一上課表
    one_up_data = set_null_time_schedule()
    for num, course_time in enumerate(result_df['上課時間']):
        # print(course_time)
        row_col_list = []
        for idx in range(0,len(course_time),2):       #R5R6
            # print(idx)
            temp_row = str(course_time[idx]) #R
            idx += 1                    
            temp_col = str(course_time[idx]) #5
            row_col_list.append((temp_row,temp_col))  #['R']['5']
            # print((temp_row,temp_col))
            # print(idx)
        # print(row_col_list)

        for (row, col) in row_col_list:
            # print(row)
            # print(col)
            one_up_data[row][col] = f"{result_df.iloc[num]['中文課名']}  {result_df.iloc[num]['教師']} {result_df.iloc[num]['上課時間']}"
            # print(one_up_data[row][col])

    print("大一上 推薦課表")
    print(one_up_data)

    st.subheader("大一上 推薦課表:")
    st.table(one_up_data)


    ###一下課表
    one_down_data = set_null_time_schedule()
    st.subheader("大一下 推薦課表:")
    st.table(one_down_data)

    ###二上課表
    two_up_data = set_null_time_schedule()
    st.subheader("大二上 推薦課表:")
    st.table(two_up_data)


    ###二下課表
    two_down_data = set_null_time_schedule()
    st.subheader("大二下 推薦課表:")
    st.table(two_down_data)


    ###三上課表
    three_up_data = set_null_time_schedule()
    st.subheader("大三上 推薦課表:")
    st.table(three_up_data)


    ###三下課表
    three_down_data = set_null_time_schedule()
    st.subheader("大三下 推薦課表:")
    st.table(three_down_data)


    ###四上課表
    four_up_data = set_null_time_schedule()
    st.subheader("大四上 推薦課表:")
    st.table(four_up_data)


    ###四下課表
    four_down_data = set_null_time_schedule()
    st.subheader("大四下 推薦課表:")
    st.table(four_down_data)
