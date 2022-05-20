# script providing variable selection elastic net:
# 
# elastic net for variable selection
# 
# Gustavo Vital

# Packages

library(tidyverse)
library(caret)
library(Matrix)
library(glmnet)
library(Metrics)
library(pROC)
library(doParallel)
library(foreach)

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
                         # 'index.lm' = data$lm_negative,
                         # 'index.vader' = data$vader_negative,
                         'covid' = data$covid,
                         'debt_crises' = data$debt_crises,
                         # 'index.lm_12' = lag(data$lm_negative, 12),
                         # 'index.vader_12' = lag(data$vader_negative, 12),
                         'cps_12' = lag(data$cps, 12),
                         'une_12' = lag(data$une, 12),
                         'interest_12'= lag(data$interest, 12),
                         'cpi_12' = lag(data$cpi, 12),
                         'gdp_12' = lag(data$gdp, 12),
                         'ppi_12' = lag(data$ppi, 12)) %>%
  drop_na() # remove NA

sink(file = "data\\elastic_net_output.txt")

cat('******************************************************************************************\n')
cat('INDEX CONTROL: VADER \n')
cat('******************************************************************************************\n')

data.model.vader <- data.frame(data.model, 
                               'index.vader' = data$vader_negative[13:nrow(data)],
                               'index.vader_12' = lag(data$vader_negative, 12)[13:nrow(data)])

for(i in 1:6){
  # define variables
  variables <- c('cps', 'une', 'interest', 'cpi', 'gdp', 'ppi')
  variable <- variables[i]
  
  set.seed(214)
  
  # divide data set into train and test
  split <- sample(nrow(data.model.vader), floor(0.8*nrow(data.model.vader)))
  
  data.train <- data.model.vader[split, ]
  data.test <- data.model.vader[-split, ]
  
  # get y and x by data.model
  y_train <- data.train[ , i]
  y_test <- data.test[ , i]
  
  X_train <- data.train[ , -i]
  X_test <- data.test[ , -i]
  
  train.sparse <- sparse.model.matrix(~. -1, X_train)
  test.sparse <- sparse.model.matrix(~. -1, X_test)
  
  
  alphacv <- seq(0.01, 0.99, 0.01)
  count <- 0
  
  mtx <- matrix(NA, nrow = length(alphacv), ncol = 3)
  colnames(mtx) <- c('alpha', 'lambda', 'cvmean')
  
  # determine the best lambda and alpha ----
  for(a in alphacv){
    
    count <- count + 1
    
    cv.elastc.net <- cv.glmnet(x = train.sparse,
                               y = y_train,
                               alpha = a,
                               parallel = TRUE)
    
    mtx[count, 1] <- c(a)
    mtx[count, 2] <- c(cv.elastc.net$lambda.min)
    mtx[count, 3] <- c(cv.elastc.net$cvm[cv.elastc.net$lambda == cv.elastc.net$lambda.min])
    
  }
  
  alpha <- mtx[mtx[, 3] == min(mtx[, 3])][1]
  lambda <- mtx[mtx[, 3] == min(mtx[, 3])][2]
  
  elastic.net <- glmnet(x = train.sparse, 
                        y = y_train,
                        alpha = alpha,
                        lambda = lambda)
  
  
  predict.elastic.net <- predict(elastic.net, test.sparse, type = 'response')
  
  # define coefficients of the matrix
  coefs <- as.matrix(coef(elastic.net))
  ix <- which(abs(coefs[, 1]) > 0)
  
  cat("=============================================\n")
  cat(paste0("Model Elastic Net ", i, " - Dependent Variable: ", variable), '\n')
  cat(paste0("Best lambda: ", lambda), '\n')
  cat(paste0("Best alpha: ", alpha), '\n')
  cat("Variavel used on the model:\n")
  print(coefs[ix,1, drop=FALSE])
  cat("=============================================\n")
  cat("Model Accuracy\n")
  cat("=============================================\n")
  results <- data.frame('MAE' = mae(predict.elastic.net, data.test[, i]),
                        'MSE' = mse(predict.elastic.net, data.test[, i]),
                        'RMSE' = rmse(predict.elastic.net, data.test[, i]),
                        'R2' = R2(predict.elastic.net, data.test[, i])[1])
  
  rownames(results) <- ''
  print(results)
  cat('\n- - - - - - - - - - - - - - - - - - - - - - -\n')
  
}

cat('******************************************************************************************\n')
cat('INDEX CONTROL: LM-SA \n')
cat('******************************************************************************************\n')

data.model.lm <- data.frame(data.model, 
                            'index.lm' = data$lm_negative[13:nrow(data)],
                            'index.lm_12' = lag(data$lm_negative, 12)[13:nrow(data)])

for(i in 1:6){
  # define variables
  variables <- c('cps', 'une', 'interest', 'cpi', 'gdp', 'ppi')
  variable <- variables[i]
  
  set.seed(214)
  
  # divide data set into train and test
  split <- sample(nrow(data.model.lm), floor(0.8*nrow(data.model.lm)))
  
  data.train <- data.model.lm[split, ]
  data.test <- data.model.lm[-split, ]
  
  # get y and x by data.model
  y_train <- data.train[ , i]
  y_test <- data.test[ , i]
  
  X_train <- data.train[ , -i]
  X_test <- data.test[ , -i]
  
  train.sparse <- sparse.model.matrix(~. -1, X_train)
  test.sparse <- sparse.model.matrix(~. -1, X_test)
  
  
  alphacv <- seq(0.01, 0.99, 0.01)
  count <- 0
  
  mtx <- matrix(NA, nrow = length(alphacv), ncol = 3)
  colnames(mtx) <- c('alpha', 'lambda', 'cvmean')
  
  # determine the best lambda and alpha ----
  for(a in alphacv){
    
    count <- count + 1
    
    cv.elastc.net <- cv.glmnet(x = train.sparse,
                               y = y_train,
                               alpha = a,
                               parallel = TRUE)
    
    mtx[count, 1] <- c(a)
    mtx[count, 2] <- c(cv.elastc.net$lambda.min)
    mtx[count, 3] <- c(cv.elastc.net$cvm[cv.elastc.net$lambda == cv.elastc.net$lambda.min])
    
  }
  
  alpha <- mtx[mtx[, 3] == min(mtx[, 3])][1]
  lambda <- mtx[mtx[, 3] == min(mtx[, 3])][2]
  
  elastic.net <- glmnet(x = train.sparse, 
                        y = y_train,
                        alpha = alpha,
                        lambda = lambda)
  
  
  predict.elastic.net <- predict(elastic.net, test.sparse, type = 'response')
  
  # define coefficients of the matrix
  coefs <- as.matrix(coef(elastic.net))
  ix <- which(abs(coefs[, 1]) > 0)
  
  cat("=============================================\n")
  cat(paste0("Model Elastic Net ", i, " - Dependent Variable: ", variable), '\n')
  cat(paste0("Best lambda: ", lambda), '\n')
  cat(paste0("Best alpha: ", alpha), '\n')
  cat("Variavel used on the model:\n")
  print(coefs[ix,1, drop=FALSE])
  cat("=============================================\n")
  cat("Model Accuracy\n")
  cat("=============================================\n")
  results <- data.frame('MAE' = mae(predict.elastic.net, data.test[, i]),
                        'MSE' = mse(predict.elastic.net, data.test[, i]),
                        'RMSE' = rmse(predict.elastic.net, data.test[, i]),
                        'R2' = R2(predict.elastic.net, data.test[, i])[1])
  
  rownames(results) <- ''
  print(results)
  cat('\n- - - - - - - - - - - - - - - - - - - - - - -\n')
  
}
sink(file = NULL)

