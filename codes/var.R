# script providing VAR estimation:
# 
# VAR estimation and impulse response functions
# 
# Gustavo Vital

# Packages
library(tidyverse)
library(vars)

# set wd ----
setwd('C:/Users/gusta/Documents/mestrado/dissertation/thesis_code/')

# read dataset
data <- read_csv('data\\data_model.csv')

data.var.lm <- data %>% 
  # filter(date > as.Date('2013-04-01')) %>%
  dplyr::select(-date) %>% 
  dplyr::select(lm_negative, cpi_diff, gdp_cycle, interest_diff, ppi_diff, une_diff)


VARselect(data.var.lm, lag.max = 5, type = "const",
          exogen = data.frame('covid' = data$covid,
                              'debt_crises' = data$debt_crises))


var.model.lm <- VAR(data.var.lm, p=2, type='const')

set.seed(214)
irf <- irf(var.model.lm,
         impulse = 'lm_negative',
         response = 'interest_diff',
         n.ahead = 18,
         boot = T,
         ci = .68)


matrix <- matrix(NA, nrow = 18, ncol = 15)
colnames(matrix) <- c('cpi', 'cpi_lower', 'cpi_upper',
                      'gdp', 'gdp_lower', 'gdp_upper',
                      'int', 'int_lower', 'int_upper',
                      'ppi', 'ppi_lower', 'ppi_upper',
                      'une', 'une_lower', 'une_upper')


for(i in 1:6){
  variables <- colnames(matrix)[c(2, 5, 8, 11, 14)]
  
  matrix[, i]
  
  
}




