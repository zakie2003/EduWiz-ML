from flask import Flask,request,jsonify,make_response
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if(request.method=='POST'):

        age=request.form["age"]
        gender=request.form["gender"]
        learning_style=request.form["learning_style"]
        previous_score=request.form["previous_score"]
        subject=request.form["subject"]
        difficulty=request.form["difficulty"]
        question_type=request.form["question_type"]
        # correct=request.form["correct"]
        time_taken=request.form["time_taken"]
        accuracy=request.form["accuracy"]

        # Checking if all the fields are filled
        if(not all ([age,gender,learning_style,previous_score,subject,difficulty,question_type,time_taken,accuracy])):
            return make_response("all fields are required",400)
        
        temp_data={
            "Age": [age],
            "Gender": [gender],
            "Learning_Style": [learning_style],
            "Previous_Score": [previous_score],
            "Subject": [subject],
            "Difficulty": [difficulty],
            "Question_Type": [question_type],
            # "Correct": [correct],
            "Time_Taken": [time_taken],
            "Accuracy": [accuracy]
        }

        # Concatinate the new data with the existing data

        student_profile = pd.DataFrame(temp_data)
        
        question_data=pd.read_csv("./DataSet/student_api.csv")


        all_data=pd.concat([question_data,student_profile],axis=0)



        #Scaling numarical Values
        scaler=MinMaxScaler()

        all_data[["Age","Previous_Score","Time_Taken","Accuracy"]]=scaler.fit_transform(all_data[["Age","Previous_Score","Time_Taken","Accuracy"]])

        #Encoding Categorical Values
        all_data["Difficulty"]=all_data["Difficulty"].map({"Easy":1,"Medium":2,"Hard":3})
        # all_data["Correct"]=all_data["Correct"].map({True:1,False:0})
        all_data[all_data["Gender"].unique()]=pd.get_dummies(all_data["Gender"])*1
        all_data[all_data["Learning_Style"].unique()]=pd.get_dummies(all_data["Learning_Style"])*1
        all_data[all_data["Subject"].unique()]=pd.get_dummies(all_data["Subject"])*1

        

        #Calculating cosine similarity
        all_data=all_data.drop(["Gender","Learning_Style","Correct","Subject","Question_Type"],axis=1)

        
        print(all_data)

        similarity=cosine_similarity(all_data.iloc[-1].values.reshape(1,-1),all_data.iloc[:-1].values)


        cosine_sim_df = pd.DataFrame({"Cosine similarity":similarity[0]})
        print(cosine_sim_df)
        top_similar_students = cosine_sim_df["Cosine similarity"].sort_values(ascending=False).index[1:]
        
        print(top_similar_students)

        return "Post Method Called Successfully"

    return "Get Method Called Successfully"

if(__name__=='__main__'):
    app.run(debug=True)