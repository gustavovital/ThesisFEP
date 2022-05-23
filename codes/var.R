# script providing VAR estimation:
# 
# VAR estimation and impulse response functions
# 
# Gustavo Vital

# Packages ----
library(tidyverse)
library(vars)

# set wd ----
setwd('C:/Users/gusta/Documents/mestrado/dissertation/thesis_code/')

# read dataset ----
data <- read_csv('data\\data_model.csv')

# divide dataset ----
data.var.lm <- data %>% 
  dplyr::select(-date) %>% 
  dplyr::select(lm_negative, cpi_diff, gdp_cycle, interest_diff, ppi_diff, une_diff)

data.var.vader <- data %>% 
  dplyr::select(-date) %>% 
  dplyr::select(vader_negative, cpi_diff, gdp_cycle, interest_diff, ppi_diff, une_diff)

# estimate VAR model ----
var.model.lm <- VAR(data.var.lm, p=2, type='const')
var.model.vader <- VAR(data.var.vader, p=2, type='const')

# lm index ----
cat('******************************************************************************************\n')
cat('LM-SA \n')
cat('******************************************************************************************\n')

data.model <- matrix(nrow = 16) %>% as.tibble()

for(j in c('90', '68')){
  for(i in 1:5){
    
    variables <- c('cpi_diff', 'gdp_cycle', 'interest_diff', 'ppi_diff', 'une_diff')
    var <- variables[i]
    
    matrix.model <- matrix(NA, ncol = 3, nrow = 16) %>% as.tibble()
    colnames(matrix.model) <- c(paste0(var, j), paste0(var, '_lower', j), paste0(var, '_upper', j))
    
    set.seed(214)
    irf <- irf(var.model.lm,
               impulse = 'lm_negative',
               response = var,
               n.ahead = 15,
               boot = T,
               ci = as.numeric(paste0('0.', j)))
    
    matrix.model[, 1] <- unlist(irf[["irf"]])
    matrix.model[, 2] <- unlist(irf[["Lower"]])
    matrix.model[, 3] <- unlist(irf[["Upper"]])
    
    data.model <- cbind(data.model, matrix.model)[colSums(!is.na(cbind(data.model, matrix.model))) > 0]
    
    
  }
}

write.csv(data.model, 'data\\var_lm_irf.csv')

# lm vader ----
cat('******************************************************************************************\n')
cat('VADER \n')
cat('******************************************************************************************\n')

data.model <- matrix(nrow = 16) %>% as.tibble()

for(j in c('90', '68')){
  for(i in 1:5){
    
    variables <- c('cpi_diff', 'gdp_cycle', 'interest_diff', 'ppi_diff', 'une_diff')
    var <- variables[i]
    
    matrix.model <- matrix(NA, ncol = 3, nrow = 16) %>% as.tibble()
    colnames(matrix.model) <- c(paste0(var, j), paste0(var, '_lower', j), paste0(var, '_upper', j))
    
    set.seed(214)
    irf <- irf(var.model.vader,
               impulse = 'vader_negative',
               response = var,
               n.ahead = 15,
               boot = T,
               ci = as.numeric(paste0('0.', j)))
    
    matrix.model[, 1] <- unlist(irf[["irf"]])
    matrix.model[, 2] <- unlist(irf[["Lower"]])
    matrix.model[, 3] <- unlist(irf[["Upper"]])
    
    data.model <- cbind(data.model, matrix.model)[colSums(!is.na(cbind(data.model, matrix.model))) > 0]
    
    
  }
}

write.csv(data.model, 'data\\var_vader_irf.csv')
rm(list = ls())
