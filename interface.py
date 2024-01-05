import pandas as pd
import streamlit as st
import time




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
    CSclassData = CSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(CSclassData)

    ###電資院課
    EECSclassData = df[df['系所全名'] == '電機資訊學院學士班'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    EECSclassData = EECSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(EECSclassData)

    ###通識課
    GEclassData = df[df['系所全名'] == '通識教育中心'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    GEclassData = GEclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(GEclassData)

    ###英文課
    LANGclassData = df[df['系所全名'] == '英語教育中心(110起)'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    LANGclassData = LANGclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(LANGclassData)

    ###大學中文
    CLclassData = df[(df['系所全名'] == '中國文學系') & (df['中文課名'] == '大學中文')].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
    CLclassData =CLclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    #print(CLclassData)

    AllCoursesData = pd.concat([CSclassData, EECSclassData, GEclassData, LANGclassData, CLclassData], ignore_index=True)
    #print(AllCoursesData)

    ###數學課
    if "1" in SelectNumberList:
        MATHclassData = df[df['系所全名'] == '數學系'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
        MATHclassData = MATHclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
        #print(MATHclassData)
        AllCoursesData = pd.concat([AllCoursesData, MATHclassData], ignore_index=True)
        #print(AllCoursesData)

    ###物理課
    if "2" in SelectNumberList:
        PHYSclassData = df[df['系所全名'] == '物理學系'].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
        PHYSclassData = PHYSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
        #print(PHYSclassData)
        AllCoursesData = pd.concat([AllCoursesData, PHYSclassData], ignore_index=True)
        #print(AllCoursesData)

    return AllCoursesData




counter = 1 

st.set_page_config(page_title="NTHU Course Selecting System", page_icon=":rocket:", layout="wide")
st.sidebar.markdown("<div style='text-align: center; font-size: 30px;'>設定</div>", unsafe_allow_html=True)
st.title("NTHU Course Selecting System")
st.divider()
SelectNumberList = choose_departments()
expected_credits = enter_expected_credits()
###讀取Excel檔案
file_path = './data/all_done.csv'
df = pd.read_csv(file_path)
AllCoursesData = filter_and_concat_courses(df,SelectNumberList)


counter += 1
key = f"input{counter}"
if st.button("顯示符合需求的課程",key=key):
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1, f'載入中 {i+1} %')
        time.sleep(0.01)


    time.sleep(0.3)
    st.dataframe(AllCoursesData)




counter += 1
key = f"input{counter}"
if st.button("顯示推薦課表",key=key):
    
    
    schedule_data = {
        # 'Time': ['1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a','b','c'],
        'M': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'T': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'W': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'R': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        'F': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    }

    df_schedule = pd.DataFrame(schedule_data)
    new_index = ('1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c')
    df_schedule.set_index(pd.Index(new_index), inplace=True)
    
    st.subheader("大一上 推薦課表:")
    st.table(df_schedule)
    st.subheader("大一下 推薦課表:")
    st.table(df_schedule)
    st.subheader("大二上 推薦課表:")
    st.table(df_schedule)
    st.subheader("大二下 推薦課表:")
    st.table(df_schedule)
    st.subheader("大三上 推薦課表:")
    st.table(df_schedule)
    st.subheader("大三下 推薦課表:")
    st.table(df_schedule)
    st.subheader("大四上 推薦課表:")
    st.table(df_schedule)
    st.subheader("大四下 推薦課表:")
    st.table(df_schedule)
