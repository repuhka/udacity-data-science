import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import warnings

# read data
titanic = pd.read_csv("titanic_data.csv")

# initial data exploration
print titanic.head()

df_titanic = titanic[["Survived", "Name", "Pclass", "Sex", "Age", "SibSp", "Parch"]]

print(df_titanic.describe(include="all"))
print(df_titanic["Sex"].value_counts())

df_titanic = df_titanic[df_titanic["Age"].notnull()]
print(len(df_titanic))

# Child function


def child(x):
    if x >= 18:
        return 0
    else:
        return 1

df_titanic['Child'] = pd.Series(df_titanic["Age"].apply(child), index=df_titanic.index)

# Survival vs. Gender graph
sb.set(style="darkgrid")
sb.barplot(data=df_titanic, x="Sex", y="Survived", palette="GnBu_d")
sb.plt.show()

# Survival vs. Adult or Child graph

sb.barplot(data=df_titanic, x="Child", y="Survived", palette="GnBu_d")
sb.plt.show()

# Survival vs. Gender and child/adult graph

sb.barplot(data=df_titanic, x="Sex", y="Survived", hue="Child", palette="GnBu_d")
sb.plt.show()

# Is a Family man more likely to survive?

warnings.filterwarnings('ignore')


def isMaleAdult(x):
    return x["Child"] == 0 and x["Sex"] == "male"

df_man_titanic = df_titanic[df_titanic.apply(isMaleAdult, axis=1)]


def aFamilyMan(x):
    if x["SibSp"] >0:
        if x["Parch"] > 0:
            return "Father"
        else:
            return "Husband"
    else:
        return "Bachelor"

df_man_titanic["FamilyMan"] = pd.Series(df_man_titanic.apply(aFamilyMan, axis =1), index=df_man_titanic.index)
print(df_man_titanic["FamilyMan"].value_counts())

# Percentage of survival based on family status


def percSurvived(x, type):
    sub = x[x["FamilyMan"] == type]
    total = len(sub)
    survived = sum(sub["Survived"]==1)
    return float(survived)/total * 100

print "Husbands survived: ", percSurvived(df_man_titanic, "Husband")
print "Fathers survived: ", percSurvived(df_man_titanic, "Father")
print "Bachelors survived: ", percSurvived(df_man_titanic, "Bachelor")

# survival based on FamilyMan categorization

sb.factorplot(data=df_man_titanic, x="Survived", col="FamilyMan", kind="count", palette="GnBu_d")
sb.plt.show()

# survival by gender and passenger class

sb.barplot(data=df_titanic, x="Sex", y="Survived", hue="Pclass", palette="GnBu_d")
sb.plt.show()

# survival by passenger class

sb.barplot(data=df_titanic, x="Pclass", y="Survived", palette="GnBu_d")
sb.plt.show()

# survivors by age

age_survivors = df_titanic[df_titanic["Survived"]==1]["Age"]
ax=sb.distplot(age_survivors)
ax.set(xlabel="Age",ylabel="% Survivors")
sb.plt.show()

# all passengers by age

sb.jointplot("Age", "Survived", data=df_titanic, kind="kde", space=0, color="b")
sb.plt.show()


# survivors per age

max_age = int(df_titanic["Age"].max())
age_dist = pd.DataFrame(index=xrange(max_age), columns=["Survived", "Dead"])
age_dist = age_dist.fillna(0)
for age in age_dist.index:
    survive_age = df_titanic[df_titanic["Age"].astype(int) == age]["Survived"]
    age_dist.loc[age, "Dead"] = sum(survive_age == 0)
    age_dist.loc[age, "Survived"] = sum(survive_age == 1)

prop_survived = age_dist.Survived / age_dist.sum(axis="columns")
prop_survived = prop_survived.fillna(0)
prop_survived.index.name = "Age"
prop_survived.name = "Proportion of survival"
plt.title("Distribution of Survivals by Age")
prop_survived.plot(kind="bar", figsize=(20, 2), legend=True)
plt.show()

# examine max number of survivors from age groups with 100% survival

print "Max number of survivors: ", age_dist.loc[[0, 5, 12, 13, 53, 63]].Survived.max()
print "Best age to survive: ", age_dist.loc[[0, 5, 12, 13, 53, 63]].Survived.idxmax()

# statistical test for significant diff between gender survivals

male = df_titanic[df_titanic["Sex"] == "male"]
female = df_titanic[df_titanic["Sex"] == "female"]
all_ppl = len(male) + len(female)
print "all people: ", all_ppl
print "females: ", len(female)
print "male: ", len(male)

# 2 tailed z test

import math

male_p = float(len(male[male["Survived"] == 1])) / len(male)
female_p = float(len(female[female["Survived"] == 1])) / len(female)
p = (male_p * len(male) + female_p * len(female)) / all_ppl
print "p: ", p
SE = math.sqrt(p * (1 - p) * (float(1) / len(male) + float(1) / len(female)))
print "SE: ", SE
z = (male_p - female_p) / SE
print "z: ", z

# children vs adults test

child = df_titanic[df_titanic["Child"] == 1]
adult = df_titanic[df_titanic["Child"] == 0]
print "total people: ", all_ppl
print "children: ", len(child)
print "adults: ", len(adult)


child_p = float(len(child[child["Survived"] == 1])) / len(child)
adult_p = float(len(adult[adult["Survived"] == 1])) / len(adult)
p = (child_p * len(child) + adult_p * len(adult)) / all_ppl
print "p: ", p
SE = math.sqrt(p * (1 - p) * (float(1) / len(child) + float(1) / len(adult)))
print "SE: ", SE
z = (child_p - adult_p) / SE
print "z: ", z