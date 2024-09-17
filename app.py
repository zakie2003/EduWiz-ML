from flask import Flask,request,jsonify,make_response
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if(request.method=='POST'):

        TOC=request.form["TOC"]
        Data_Science=request.form["Data Science"]
        Average_Time_Taken=request.form["Average Time Taken"]
        prefence=request.form["Preference of Learning"]
        score=request.form["Previous Score"]
        accuracy=request.form["Accuracy of Student"]

        # Checking if all the fields are filled
        if(not all ([TOC,Data_Science,Average_Time_Taken,prefence,score,accuracy])):
            return make_response("all fields are required",400)
        
        temp_data={
            "TOC": [TOC],
            "Data Science": [Data_Science],
            "Average Time Taken": [Average_Time_Taken],
            "Preference of Learning": [prefence],
            "Previous Score": [score],
            "Accuracy of Student": [accuracy],
        }

        student_profile = pd.DataFrame(temp_data)
        
        question_data=pd.read_csv("./DataSet/Question_Set.csv")

        question_data["Question Difficulty"]=question_data["Question Difficulty"].map({"Easy":1,"Medium":2,"Hard":3})

        # print(question_data)
        question_data.columns=["TOC","Data Science","Average Time Taken","Preference of Learning","Previous Score","Accuracy of Student"]
        all_data=pd.concat([question_data,student_profile],axis=0)

        #Scaling numarical Values

        scaler=MinMaxScaler()
        all_data[["Average Time Taken"]]=scaler.fit_transform(all_data[["Average Time Taken"]])
        all_data[all_data["Preference of Learning"].unique()]=pd.get_dummies(all_data["Preference of Learning"])*1
        all_data=all_data.drop(columns=["Preference of Learning"])

        similarity=cosine_similarity(all_data.iloc[-1].values.reshape(1,-1),all_data.iloc[:-1].values)
        
        cosine_sim_df = pd.DataFrame({"Cosine similarity":similarity[0]})
        print(cosine_sim_df)
        top_similar_students = cosine_sim_df["Cosine similarity"].sort_values(ascending=False).index[1:]
        
        print(top_similar_students)

        return "Post Method Called Successfully"

    return "Get Method Called Successfully"

if(__name__=='__main__'):
    app.run(debug=True)