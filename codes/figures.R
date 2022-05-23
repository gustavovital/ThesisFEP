# script providing IRF plots:
# 
# IRF plots
# 
# Gustavo Vital

# Packages ----
library(tidyverse)
library(patchwork)

# set wd ----
setwd('C:/Users/gusta/Documents/mestrado/dissertation/thesis_code/')

# get data ----
data.lm <- read_csv('data\\var_lm_irf.csv')
data.vader <- read_csv('data\\var_vader_irf.csv')

# add row 0 ----
data.lm <- rbind(0, data.lm)
data.vader <- rbind(0, data.vader)

# plot IRF functions ----
cpi.lm <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = cpi_diff_lower90, ymax = cpi_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = cpi_diff_lower68, ymax = cpi_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = cpi_diff90), size = .7) +
  geom_point(aes(y = cpi_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Consumer Price Index') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

ppi.lm <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = ppi_diff_lower90, ymax = ppi_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = ppi_diff_lower68, ymax = ppi_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = ppi_diff90), size = .7) +
  geom_point(aes(y = ppi_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Producer Prices Index') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

interest.lm <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = interest_diff_lower90, ymax = interest_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = interest_diff_lower68, ymax = interest_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = interest_diff90), size = .7) +
  geom_point(aes(y = interest_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Long-Term Government Bond Yields') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

gdp.lm <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = gdp_cycle_lower90, ymax = gdp_cycle_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = gdp_cycle_lower68, ymax = gdp_cycle_upper68), fill = 'gray85') +
  geom_line(aes(y = gdp_cycle90), size = .7) +
  geom_point(aes(y = gdp_cycle90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Output Gap') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

une.lm <- data.lm %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = une_diff_lower90, ymax = une_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = une_diff_lower68, ymax = une_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = une_diff90), size = .7) +
  geom_point(aes(y = une_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Unemployment Rate') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))
 
# VADER
cpi.vader <- data.vader %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = cpi_diff_lower90, ymax = cpi_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = cpi_diff_lower68, ymax = cpi_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = cpi_diff90), size = .7) +
  geom_point(aes(y = cpi_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Consumer Price Index') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

ppi.vader <- data.vader %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = ppi_diff_lower90, ymax = ppi_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = ppi_diff_lower68, ymax = ppi_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = ppi_diff90), size = .7) +
  geom_point(aes(y = ppi_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Producer Prices Index') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

interest.vader <- data.vader %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = interest_diff_lower90, ymax = interest_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = interest_diff_lower68, ymax = interest_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = interest_diff90), size = .7) +
  geom_point(aes(y = interest_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Long-Term Government Bond Yields') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

gdp.vader <- data.vader %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = gdp_cycle_lower90, ymax = gdp_cycle_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = gdp_cycle_lower68, ymax = gdp_cycle_upper68), fill = 'gray85') +
  geom_line(aes(y = gdp_cycle90), size = .7) +
  geom_point(aes(y = gdp_cycle90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Output Gap') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

une.vader <- data.vader %>% 
  ggplot(aes(x = X1)) +
  geom_ribbon(aes(ymin = une_diff_lower90, ymax = une_diff_upper90), fill = 'gray75') +
  geom_ribbon(aes(ymin = une_diff_lower68, ymax = une_diff_upper68), fill = 'gray85') +
  geom_line(aes(y = une_diff90), size = .7) +
  geom_point(aes(y = une_diff90), shape = 21) +
  geom_hline(yintercept = 0, size = 0.3) +
  scale_x_continuous(name = "Horizon", limits = c(0, 12.1), expand = c(0, 0), breaks = c(0, 12)) +
  labs(y = 'Percent', title = 'Unemployment Rate') +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5, size = 12))

# layout 
layout <- "
ABC
DE#
"

gdp.lm + une.lm + cpi.lm + ppi.lm + interest.lm + plot_layout(design = layout)
ggsave("images\\irf_lm.pdf", width = 297, height = 210, units = "mm")

gdp.vader + une.vader + cpi.vader + ppi.vader + interest.vader + plot_layout(design = layout)
ggsave("images\\irf_vader.pdf", width = 297, height = 210, units = "mm")
