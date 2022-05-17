# script providing variable selection lasso:
# 
# LASSO for variable selection
# 
# Gustavo Vital

# Packages

library(tidyverse)
library(caret)
library(Matrix)
library(glmnet)

# set wd ----
setwd('C:/Users/gusta/Documents/mestrado/dissertation/thesis_code/')

# read dataset
data <- read_csv('data\\data_model.csv')

# variables for the model acording to shapiro and literature:
# CPS, UNE, INTEREST, CPI, GDP (GAP), PPI

data.model <- data.frame('cps' = data$cps,
                         'une' = data$une,
                         'interest'= data$interest,
                         'cpi' = data$cpi,
                         'gdp' = data$gdp,
                         'ppi' = data$ppi,
                         'index' = data$lm_negative,
                         'covid' = data$covid,
                         'debt_crises' = data$debt_crises,
                         'index_12' = lag(data$lm_negative, 12),
                         'cps_12' = lag(data$cps, 12),
                         'une_12' = lag(data$une, 12),
                         'interest_12'= lag(data$interest, 12),
                         'cpi_12' = lag(data$cpi, 12),
                         'gdp_12' = lag(data$gdp, 12),
                         'ppi_12' = lag(data$ppi, 12)) %>%
  drop_na() # remove NA

for(i in 1:6){
  # define variables
  variables <- c('cps', 'une', 'interest', 'cpi', 'gdp', 'ppi')
  variable <- variables[i]
  
  set.seed(214)
  
  # divide data set into train and test
  split <- sample(nrow(data.model), floor(0.8*nrow(data.model)))
  
  data.train <- data.model[split, ]
  data.test <- data.model[-split, ]
  
  # get y and x by data.model
  y_train <- data.train[ , i]
  y_test <- data.test[ , i]
  
  X_train <- data.train[ , -i]
  X_test <- data.test[ , -i]
  
  train.sparse <- sparse.model.matrix(~., X_train)
  test.sparse <- sparse.model.matrix(~., X_test)
  
  # determine the best lambda ----
  lasso <- glmnet(x = train.sparse, 
                  y = y_train)
  
  cv.lasso <- cv.glmnet(x = train.sparse, 
                        y = y_train)
  
  lambda <- cv.lasso$lambda.1se
  
  
  # define coefficients of the matrix
  coefs <- as.matrix(coef(cv.lasso))
  ix <- which(abs(coefs[, 1]) > 0)
  
  print("=============================================")
  print(paste0("Model Lasso ", i, " - Dependent Variable: ", variable))
  print("")
  print(paste0("Best lambda: ", lambda))
  print("")
  print("Variavel used on the model:")
  print(coefs[ix,1, drop=FALSE])
  print("")


}
