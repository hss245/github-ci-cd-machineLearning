import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
pd.options.mode.chained_assignment = None

class ClassificationAlgorithmTraining:
    
    def __init__(self):
        __filePath = "web-page-phishing.csv"
        self.DATA = pd.read_csv(__filePath)
    
    def dataCleaning(self):
        X = self.DATA.iloc[:, :-1]
        Y = self.DATA.iloc[:, -1]
        XTrain, XTest, YTrain, YTest = train_test_split(X, Y, test_size = 0.25, random_state = 27)
        self.standardScalerObject = StandardScaler()
        XTrainTransformed = self.standardScalerObject.fit_transform(XTrain)
        self.modelTraining(XTrainTransformed, YTrain, XTest, YTest)
    
    def modelTraining(self, XTrainTransformed, YTrain, XTest, YTest):
        modelStatisticsComparision = pd.DataFrame(columns = ['Model', 'Algorithm Name', 'Train Accuracy'])
        counter = 0
        
        mlModelLogisticRegression = LogisticRegression(penalty = 'l2')
        mlModelLogisticRegression.fit(XTrainTransformed, YTrain)
        modelStatisticsComparision.loc[counter] = [mlModelLogisticRegression, "Logistic Regression", mlModelLogisticRegression.score(XTrainTransformed, YTrain)]
        counter += 1
        
        mlModelDecisionTreeClassifier = DecisionTreeClassifier(criterion = 'gini', splitter = 'best')
        mlModelDecisionTreeClassifier.fit(XTrainTransformed, YTrain)
        modelStatisticsComparision.loc[counter] = [mlModelDecisionTreeClassifier, "Decision Tree", mlModelDecisionTreeClassifier.score(XTrainTransformed, YTrain)]
        counter += 1
        
        mlModelRandomForestClassifier = RandomForestClassifier(n_estimators = 150, criterion = 'entropy')
        mlModelRandomForestClassifier.fit(XTrainTransformed, YTrain)
        modelStatisticsComparision.loc[counter] = [mlModelRandomForestClassifier, "Random Forest Classifier", mlModelRandomForestClassifier.score(XTrainTransformed, YTrain)]
        counter += 1
        
        mlModelAdaBoostClassifier = AdaBoostClassifier(n_estimators = 100, learning_rate = 0.85, algorithm = "SAMME.R")
        mlModelAdaBoostClassifier.fit(XTrainTransformed, YTrain)
        modelStatisticsComparision.loc[counter] = [mlModelAdaBoostClassifier, "Ada Boost Classifier", mlModelAdaBoostClassifier.score(XTrainTransformed, YTrain)]
        counter += 1
        
        self.modelTesting(XTest, YTest, modelStatisticsComparision)
    
    def modelTesting(self, XTest, YTest, modelStatisticsComparision):
        modelStatisticsComparision["Test Accuracy"] = 0
        modelStatisticsComparision["Recall Value"] = 0
        modelStatisticsComparision["Precision Value"] = 0
        modelStatisticsComparision["F1 Score"] = 0
        
        XTestTransformed = self.standardScalerObject.transform(XTest)
        
        for row in range(modelStatisticsComparision.shape[0]):
            modelStatisticsComparision["Test Accuracy"].iloc[row] = accuracy_score(YTest, modelStatisticsComparision.iloc[row, 0].predict(XTestTransformed))
            modelStatisticsComparision["Recall Value"].iloc[row] = recall_score(YTest, modelStatisticsComparision.iloc[row, 0].predict(XTestTransformed))
            modelStatisticsComparision["Precision Value"].iloc[row] = precision_score(YTest, modelStatisticsComparision.iloc[row, 0].predict(XTestTransformed))
            modelStatisticsComparision["F1 Score"].iloc[row] = f1_score(YTest, modelStatisticsComparision.iloc[row, 0].predict(XTestTransformed))
        
        os.remove("modelStatistic.txt")
        
        with open("modelStatistic.txt", "a") as filePointer:
            for row in range(modelStatisticsComparision.shape[0]):
                filePointer.write(f"""Model Name : '{modelStatisticsComparision.iloc[row, 1]}', 
        Train Accuracy : '{modelStatisticsComparision.iloc[row, 2]}, 
        Test Accuracy : {modelStatisticsComparision.iloc[row, 3]}, 
        Recall Score: {modelStatisticsComparision.iloc[row, 4]},
        Precision Score: {modelStatisticsComparision.iloc[row, 5]},
        F1 Score: {modelStatisticsComparision.iloc[row, 6]}'\n\n""")

if __name__ == "__main__":
    obj = ClassificationAlgorithmTraining()
    obj.dataCleaning()