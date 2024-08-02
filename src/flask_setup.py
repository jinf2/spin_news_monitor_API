from flask import Flask,jsonify

app = Flask(__name__)
app.json.sort_keys = False

#news_monitor_API_start
@app.route('/')
def get_items():
    return "welcome to Finding Professor News API"

@app.route('/FindProfNews/<UniversityName>/<DayRange>/<LLMsT>')
def Find_Prof_News(UniversityName,DayRange,LLMsT):
    import src.news_monitors as news_monitors
    result = news_monitors.New_Monitor(UniversityName,DayRange,LLMsT)
    return jsonify(result)
    # return{
    #     "msg":"success",
    #     "data":result
    # }


if __name__ == '__main__':
    app.run()

#http://127.0.0.1:5000/FindProfNews/uiuc/3d/GPT4.0