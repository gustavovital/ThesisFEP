# script providing IRF plots:
# 
# IRF plots
# 
# Gustavo Vital

# Packages ----
library(tidyverse)

# set wd ----
setwd('C:/Users/gusta/Documents/mestrado/dissertation/thesis_code/')

# get data ----
data.lm <- read_csv('data\\var_lm_irf.csv')
data.vader <- read_csv('data\\var_vader_irf.csv')

# add row 0 ----
data.lm <- rbind(0, data.lm)
data.vader <- rbind(0, data.vader)

# plot IRF functions ----

cpi <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = cpi_diff_lower90, ymax = cpi_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = cpi_diff_lower68, ymax = cpi_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = cpi_diff90), size = .7) +
  geom_point(aes(y = cpi_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.7) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Consumer Price Index') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

ppi <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = ppi_diff_lower90, ymax = ppi_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = ppi_diff_lower68, ymax = ppi_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = ppi_diff90), size = .7) +
  geom_point(aes(y = ppi_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.7) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Producer Prices In') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))
