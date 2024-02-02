library(rpart)
library(rpart.plot)
library(rminer)

rm(list=ls())

df <- read.csv("/tmp/mozilla_vkg0/features.csv", header = T)

df$gender           <- as.factor(df$gender)
df$background_noise <- as.factor(df$background_noise)
df$label            <- as.factor(df$label)

head(df)
str(df)

model <- rpart(label ~ ., data=df)
model
summary(model)
rpart.plot(model)

# Logistic regression
model.logit <- glm(label ~., family=binomial(link='logit'), data=df)
summary(model.logit)

d <- summary(model.logit)
d$coefficients[, 1]
max(d$coefficients[, 1])
sort(d$coefficients[, 1])

# SVM (from rminer)
model.svm <- fit(label ~. , data=df, model="svm", kpar=list(sigma=0.10), C=2)
svm.imp <- Importance(model.svm, data=df)





