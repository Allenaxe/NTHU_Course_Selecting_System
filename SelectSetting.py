import pandas as pd

print("此排課程式目標為達到資工系的畢業門檻")

###選擇科系
while True:
    print("請選擇想額外修習的科系(預設已包含資工系、電資學院、通識、英語、大學中文)")
    print("1 數學系     2 物理系   3 無額外修習其他系")
    SelectNumber = input("請輸入科系代碼(多選請以空白為間隔並以換行為結束):")
    SelectNumberList = SelectNumber.split(" ")

    ###確認輸入無誤
    if "3" in SelectNumberList and len(SelectNumberList) > 1:
        print("輸入有誤請重新輸入")
        print("\n")
        continue
    elif "1" not in SelectNumberList and "2" not in SelectNumberList and "3" not in SelectNumberList:
        print("輸入有誤請重新輸入")
        print("\n")
        continue
    else:
        print("\n")
        break

###輸入各學期學分
while True:
    print("請輸入從大一上至大四下各學期的期望修習學分")
    CreditList = [None] * 8
    CreditList[0] = int(input("請輸入大一上期望修習學分:"))
    CreditList[1] = int(input("請輸入大一下期望修習學分:"))
    CreditList[2] = int(input("請輸入大二上期望修習學分:"))
    CreditList[3] = int(input("請輸入大二下期望修習學分:"))
    CreditList[4] = int(input("請輸入大三上期望修習學分:"))
    CreditList[5] = int(input("請輸入大三下期望修習學分:"))
    CreditList[6] = int(input("請輸入大四上期望修習學分:"))
    CreditList[7] = int(input("請輸入大四下期望修習學分:"))

    ###確認輸入無誤
    CreditSum = 0
    for x in CreditList:
        CreditSum += x
    if CreditSum < 128:
        print("輸入有誤請重新輸入")
        print("\n")
        continue
    else:
        print("總學分為:", CreditSum)
        print("\n")
        break

###讀取Excel檔案
file_path = './data/all_done.xlsx'
df = pd.read_excel(file_path)

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

print(AllCoursesData)