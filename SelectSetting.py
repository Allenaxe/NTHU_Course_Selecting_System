import pandas as pd

print("此排課程式目標為達到資工系的畢業門檻")

###選擇科系
while True:
    print("請選擇想額外修習的科系(預設已包含資工系、電資學院、通識、英語、大學中文)")
    print("1 數學系     2 物理系   3 無額外修習其他系")
    SelectNumber = input("請輸入科系代碼(多選請以空白為間隔並以換行為結束):")
    SelectNumberList = SelectNumber.split(" ")

    print("請選擇想選擇的課")
    print("X 普通物理B Y 普通化學 Z 生命科學")
    SelectCourse = input("請輸入代碼:")

    print("請選擇不想要的類別")
    print("A A類    B B類    C C類    D D類")
    SelectType = input("請輸入代碼:")

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
    CreditList = [16] * 8
    # CreditList[0] = int(input("請輸入大一上期望修習學分:"))
    # CreditList[1] = int(input("請輸入大一下期望修習學分:"))
    # CreditList[2] = int(input("請輸入大二上期望修習學分:"))
    # CreditList[3] = int(input("請輸入大二下期望修習學分:"))
    # CreditList[4] = int(input("請輸入大三上期望修習學分:"))
    # CreditList[5] = int(input("請輸入大三下期望修習學分:"))
    # CreditList[6] = int(input("請輸入大四上期望修習學分:"))
    # CreditList[7] = int(input("請輸入大四下期望修習學分:"))

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
file_path = './data/all_done.csv'
df = pd.read_csv(file_path)

CSclassData = df[df['系所全名'] == '資訊工程學系'].dropna(subset=['科號', '中文課名', '學分'])
CSclassData['教師'] = CSclassData['教師'].fillna('')
CSclassData['上課時間'] = CSclassData['上課時間'].fillna('')
CSclassData['等級制'] = CSclassData['等級制'].fillna(0)
CSclassData = CSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)

###讀取各系資料並排除資料欄有空缺的課
###資工系課
CSclassData = df[df['系所全名'] == '資訊工程學系'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
CSclassData['教師'] = CSclassData['教師'].fillna(' ')
CSclassData['等級制'] = CSclassData['等級制'].fillna(0)
CSclassData = CSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
# print(CSclassData)

###電資院課
EECSclassData = df[df['系所全名'] == '電機資訊學院學士班'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
EECSclassData['教師'] = EECSclassData['教師'].fillna('')
EECSclassData['等級制'] = EECSclassData['等級制'].fillna(0)
EECSclassData = EECSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
# print(EECSclassData)

###通識課
GEclassData = df[df['系所全名'] == '通識教育中心'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
GEclassData['教師'] = GEclassData['教師'].fillna('')
GEclassData['等級制'] = GEclassData['等級制'].fillna(0)
GEclassData = GEclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
# print(GEclassData)
# print(GEclassData)

###英文課
LANGclassData = df[df['系所全名'] == '英語教育中心(110起)'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
LANGclassData['教師'] = LANGclassData['教師'].fillna('')
LANGclassData['等級制'] = LANGclassData['等級制'].fillna(0)
LANGclassData = df[df['系所全名'] == '英語教育中心(110起)'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
LANGclassData['教師'] = LANGclassData['教師'].fillna('')
LANGclassData['等級制'] = LANGclassData['等級制'].fillna(0)
LANGclassData = LANGclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
# print(LANGclassData)
# print(LANGclassData)

###大學中文
CLclassData = df[(df['系所全名'] == '中國文學系') & (df['中文課名'] == '大學中文')].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
CLclassData['教師'] = CLclassData['教師'].fillna('')
CLclassData['等級制'] = CLclassData['等級制'].fillna(0)
CLclassData = df[(df['系所全名'] == '中國文學系') & (df['中文課名'] == '大學中文')].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
CLclassData['教師'] = CLclassData['教師'].fillna('')
CLclassData['等級制'] = CLclassData['等級制'].fillna(0)
CLclassData =CLclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
# print(CLclassData)
# print(CLclassData)

AllCoursesData = pd.concat([CSclassData, EECSclassData, GEclassData, LANGclassData, CLclassData], ignore_index=True)
# print(AllCoursesData)
# print(AllCoursesData)

listAdd = ['微積分Ｂ一','微積分Ｂ二','普通物理Ｂ一','普通物理Ｂ二','普通化學一','普通化學二','生命科學一','生命科學二']

for i in range(len(listAdd)):
    AddclassData = df[df['中文課名'] == str(listAdd[i])].dropna(subset=['科號', '系所全名', '學分'])
    AddclassData['教師'] = AddclassData['教師'].fillna('')
    AddclassData['上課時間'] = AddclassData['上課時間'].fillna('')
    AddclassData['等級制'] = AddclassData['等級制'].fillna(0)
    AddclassData['中文課名'] = str(listAdd[i])
    AddclassData = AddclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    AllCoursesData = pd.concat([AllCoursesData, AddclassData], ignore_index=True)

Type = [[0],[0],[0],[0]]
Type[0] = TypeA = ['常微分方程','訊號與系統','正規語言','數值最佳化','量子計算概論']
Type[1] = TypeB = ['電路與電子學一','積體電路設計概論','嵌入式系統概論','編譯器設計','超大型積體電路系統設計']
Type[2] = TypeC = ['計算機網路概論','軟體工程','密碼與網路安全概論','平行計算概論']
Type[3] = TypeD = ['資料庫系統概論','人工智慧概論','多媒體技術概論','機器學習概論']
listAdd2 = []
#print(SelectType)
listcharacter = []
jump = 0
if SelectType == 'A':
    listAdd2 = TypeB + TypeC + TypeD
    listcharacter = ['B','C','D']
    jump = 0
elif SelectType == 'B':
    listAdd2 = TypeA + TypeC + TypeD
    listcharacter = ['A','C','D']
    jump = 1
elif SelectType == 'C':
    listAdd2 = TypeB + TypeA + TypeD
    listcharacter = ['B','A','D']
    jump = 2
elif SelectType == 'D':
    listAdd2 = TypeB + TypeC + TypeA
    listcharacter = ['B','C','A']
    jump = 3


AddCourseABCD = pd.DataFrame()
listvisited = []
for t in range(4):
    print("t=",t)
    if t == jump:
        continue
    AddCourseS = pd.DataFrame()
    for i in range(len(Type[t])):
        if Type[t][i] in listvisited:
            continue
        print(Type[t][i])
        AddclassData2 = df[df['中文課名'] == str(Type[t][i])].dropna(subset=['科號', '系所全名', '學分'])
        AddclassData2['教師'] = AddclassData2['教師'].fillna('')
        AddclassData2['上課時間'] = AddclassData2['上課時間'].fillna('')
        AddclassData2['等級制'] = AddclassData2['等級制'].fillna(0)
        AddclassData2['中文課名'] = str(Type[t][i])
        AddclassData2 = AddclassData2[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
        AddCourseS = pd.concat([AddCourseS, AddclassData2], ignore_index=True)
    AddCourseS = AddCourseS.nlargest(1, '等級制')
    listvisited.extend(AddCourseS['中文課名'])
    print("listvisited = ",listvisited)
    print(AddCourseS)
    AddCourseABCD = pd.concat([AddCourseABCD, AddCourseS], ignore_index=True)


AddCourseS = pd.DataFrame()
for i in range(len(listAdd2)):
    if listAdd2[i] in listvisited:
        continue
    AddclassData2 = df[df['中文課名'] == str(listAdd2[i])].dropna(subset=['科號', '系所全名', '學分'])
    AddclassData2['教師'] = AddclassData2['教師'].fillna('')
    AddclassData2['上課時間'] = AddclassData2['上課時間'].fillna('')
    AddclassData2['等級制'] = AddclassData2['等級制'].fillna(0)
    AddclassData2['中文課名'] = str(listAdd2[i])
    AddclassData2 = AddclassData2[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    AddCourseS = pd.concat([AddCourseS, AddclassData2], ignore_index=True)
AddCourseS = AddCourseS.nlargest(1, '等級制')
listvisited.extend(AddCourseS['中文課名'])
print("listvisited = ",listvisited)
print(AddCourseS)
AddCourseABCD = pd.concat([AddCourseABCD, AddCourseS], ignore_index=True)

#print(len(listAdd2))
AddCourseABCD = AddCourseABCD.nlargest(4, '等級制')
###數學課
if "1" in SelectNumberList:
    MATHclassData = df[df['系所全名'] == '數學系'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
    MATHclassData['教師'] = MATHclassData['教師'].fillna('')
    MATHclassData['等級制'] = MATHclassData['等級制'].fillna(0)
    MATHclassData = df[df['系所全名'] == '數學系'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
    MATHclassData['教師'] = MATHclassData['教師'].fillna('')
    MATHclassData['等級制'] = MATHclassData['等級制'].fillna(0)
    MATHclassData = MATHclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    # print(MATHclassData)
    # print(MATHclassData)
    AllCoursesData = pd.concat([AllCoursesData, MATHclassData], ignore_index=True)
    # print(AllCoursesData)
    # print(AllCoursesData)

###物理課
if "2" in SelectNumberList:
    PHYSclassData = df[df['系所全名'] == '物理學系'].dropna(subset=['科號', '中文課名', '學分', '上課時間'])
    PHYSclassData['教師'] = PHYSclassData['教師'].fillna('')
    PHYSclassData['等級制'] = PHYSclassData['等級制'].fillna(0)
    PHYSclassData = PHYSclassData[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
    # print(PHYSclassData)
    # print(PHYSclassData)
    AllCoursesData = pd.concat([AllCoursesData, PHYSclassData], ignore_index=True)
    # print(AllCoursesData)
    # print(AllCoursesData)

# print(AllCoursesData)
# print(AllCoursesData)