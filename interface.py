import pandas as pd
import streamlit as st

def main():
    st.title("畢業門檻達成程式")

    selected_departments = choose_departments()
    expected_credits = enter_expected_credits()


    df = pd.read_csv('./data/all_done.csv')
    all_courses_data = filter_and_concat_courses(df, selected_departments)
    print(all_courses_data)
    if st.button("顯示可選課程"):
        st.subheader("選擇的課程資訊：")
        print(all_courses_data)
        st.dataframe(all_courses_data)

def choose_departments():
    st.sidebar.header("選擇科系")
    st.sidebar.write("請選擇想額外修習的科系(預設已包含資工系、電資學院、通識、英語、大學中文)")
    
    options = {"數學系": 1, "物理系": 2, "無額外修習其他系": 3}
    selected_departments = st.sidebar.multiselect("選擇科系", options=options.keys(), default=["無額外修習其他系"])
    
    return [options[department] for department in selected_departments]

def enter_expected_credits():
    st.sidebar.header("輸入各學期學分")
    credits_list = []

    for semester in range(1, 9):
        credit = st.sidebar.number_input(f"大{semester//2+1} {['上', '下'][semester%2]}期望修習學分:", min_value=0)
        credits_list.append(credit)

    total_credits = sum(credits_list)
    st.sidebar.write(f"總學分為: {total_credits}")

    return credits_list

def filter_and_concat_courses(df, selected_departments):
    courses_data = []

    for department_code in selected_departments:
        department_data = df[df['系所全名'] == department_code].dropna(subset=['科號', '中文課名', '學分', '教師', '上課時間', '等級制'])
        department_data = department_data[['科號', '中文課名', '學分', '教師', '上課時間', '等級制']].reset_index(drop=True)
        courses_data.append(department_data)

    all_courses_data = pd.concat(courses_data, ignore_index=True)
    return all_courses_data

if __name__ == "__main__":
    main()
