import streamlit as st
import pandas as pd
import time
import copy

column_config = {
            "Alias": st.column_config.Column(
                help="Alias",
                width="medium",
                required=True,
            ),
            "Data Type": st.column_config.SelectboxColumn(
                label="Type",
                help="Data Type",
                width="small",
                options=[
                    "Text",
                    "Long",
                    "Double",
                    "Date",
                    "Geometry",
                    "Object ID"
                ],
                required=True,
            ),
            "Type Filter": st.column_config.SelectboxColumn(
                help="Type Filter",
                width="medium",
                options=[
                    "є будь-яким з",
                    "знаходиться між",
                ],
                required=True,
            )
        }

json_temp = {
    'Text' : {
                "fieldObj": {
                    "name": "Text",
                    "label": "cadasrNumb",
                    "dateFormat": "",
                    "shortType": "string",
                    "type": "esriFieldTypeString"
                },
                "operator": "stringOperatorIsAnyOf",
                "valueObj": {
                    "isValid": True,
                    "type": "multiple",
                    "value": []
                },
                "interactiveObj": {
                    "prompt": "Кадастровий номер",
                    "hint": "Виберіть одне або декілька значень",
                    "cascade": "previous"
                },
                "caseSensitive": False
                },
    'Long' : {
                "fieldObj": {
                    "name": "Long",
                    "label": "dzkOwnCoun",
                    "dateFormat": "",
                    "shortType": "number",
                    "type": "esriFieldTypeInteger"
                },
                "operator": "numberOperatorIsAnyOf",
                "valueObj": {
                    "isValid": True,
                    "type": "multiple",
                    "value": []
                },
                "interactiveObj": {
                    "prompt": "Кількість власників за ДЗК",
                    "hint": "Виберіть одне або декілька значень",
                    "cascade": "previous"
                },
                "caseSensitive": False
                },
    'Double' : {
                "fieldObj": {
                    "name": "Double",
                    "label": "dzkOwnCoun",
                    "dateFormat": "",
                    "shortType": "number",
                    "type": "esriFieldTypeInteger"
                },
                "operator": "numberOperatorIsAnyOf",
                "valueObj": {
                    "isValid": True,
                    "type": "multiple",
                    "value": []
                },
                "interactiveObj": {
                    "prompt": "Кількість власників за ДЗК",
                    "hint": "Виберіть одне або декілька значень",
                    "cascade": "previous"
                },
                "caseSensitive": False
                },
    'Date': {
                "fieldObj": {
                    "name": "Date",
                    "label": "endDateNr",
                    "dateFormat": "shortDateLE",
                    "shortType": "date",
                    "type": "esriFieldTypeDate"
                },
                "operator": "dateOperatorIsBetween",
                "valueObj": {
                    "isValid": True,
                    "type": "value",
                    "value1": None,
                    "value2": None,
                    "virtualDate1": None,
                    "virtualDate2": None
                },
                "interactiveObj": {
                    "prompt": "Дата закінчення права оренди (нормалізована)",
                    "hint": "Вкажіть значення у форматі\"від - до\"",
                    "cascade": "none"
                },
                "caseSensitive": False
            }
}

st.title('Створення json файлу для фільтру/запиту 😎')

csv = pd.DataFrame(
    {
        'Field Name': ['OBJECTID', 'Shape', 'str_id', 'str_type', 'codifier', 'str_name', 'name_old', 'note', 'name_eng', 'additional', 'Shape_Length'],
        'Alias' : ['OBJECTID', 'Shape', 'ID запису про вулицю', 'Тип дорожньо-вуличної мережі', 'КАТОТТГ', 'Назва вулиці (чинна)', 'Назва вулиці (архівна)', 'Примітка', 'Назва вулиці латиницею', 'Уточнююча частина назви вулиці', 'Shape_Length'],
        'Data Type' : ['OBJECTID','Geometry', 'Text', 'Long', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Double'],
    }
).to_csv(index=False).encode('utf-8')

st.download_button(
    label="Завантажити приклад CSV файлу",
    data=csv,
    file_name='Приклад файлу.csv',
    mime='text/csv',
)

uploaded_file = st.file_uploader("Виберіть csv файл", accept_multiple_files=False)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Enable'] = df['Data Type'].apply(lambda x: True if x == 'Text' or x == 'Long' or x == "Double" else False)
    df['Type Filter'] = df['Data Type'].apply(lambda x: 'є будь-яким з' if x == 'Text' or x== "Long" else "знаходиться між" if x == 'Date' or x == 'Double' else "")
    edited_df = st.data_editor(df[['Field Name', 'Alias', 'Data Type', 'Enable', 'Type Filter']], column_config=column_config)

    if st.button('Сформувати json ⚙️', type="primary"):
        progress_text = "Форумування json, будь ласка зачекайте 🕝"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        
        
        result_df = edited_df[edited_df['Enable'] == True]
        result_list = []
        for index in result_df.index:            
            temp_json = copy.deepcopy(json_temp[result_df['Data Type'][index]])
            temp_json['fieldObj']['name'] = result_df['Field Name'][index]
            temp_json['fieldObj']['label'] = result_df['Alias'][index]
            temp_json['interactiveObj']['prompt'] = result_df['Alias'][index]

            result_list.append(temp_json)

        result_list