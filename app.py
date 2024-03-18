from flask import Flask, render_template, request
import pandas as pd
#?
app = Flask(__name__)

def read():
    file = pd.ExcelFile('/workspaces/codespaces-flask/_100 вопросов мастеру.xlsx')
    data_frame_dict = {}
    for sheet_name in file.sheet_names:
        data_frame_dict[sheet_name] = pd.read_excel(file, sheet_name, index_col=0)
    return data_frame_dict

dfs = read()

@app.route("/")
def index():
    return render_template('index.html', sheets=dfs.keys())

@app.route('/question/', methods=['POST'])
def question():
    sheet = request.form.get('index')
    sample_obj = dfs[sheet].sample()
    dfs[sheet].drop(sample_obj.index, inplace=True)
    left_amount = dfs[sheet].shape[0]
    return render_template('question.html',
                            name=sample_obj.iloc[0, 0],
                            work=sample_obj.iloc[0, 1],
                            job=sample_obj.iloc[0, 2],
                            question=sample_obj.iloc[0, 3],
                            link=sheet,
                            left_amount=left_amount)
