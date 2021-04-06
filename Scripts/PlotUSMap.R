library(ggplot2)
library(tidyverse)
library(maps)
library(usmap)

states <- map_data("state")
snames <- data.frame(state = tolower(state.name), abb = state.abb)
state_label <- states %>%
  group_by(region) %>%
  summarize(long = mean(range(long)),
            lat = mean(range(lat))) %>%
  merge(snames, by.x = "region", by.y = "state")

plot_by_state <- function(df, title, fname){
  p <- df %>%
    group_by(state) %>%
    summarize(crime = sum(value * population) / sum(population)) %>%
    mutate(state = tolower(state)) %>%
    merge(states, by.x = "state", by.y = "region", all.y = T) %>%
    replace_na(list(crime = 0)) %>%
    arrange(order) %>%
    ggplot(aes(x = long, y = lat, label = toupper(state))) +
    geom_polygon(aes(group = group, fill = crime), color = "black") +
    scale_fill_viridis_c(option = "C", direction = -1, end = 1) +
    geom_text(data = state_label, aes(x = long, y = lat, label = abb)) +
    labs(fill = "Crime Per 100K Population", x = "Longitude", y = "Latitude",
         title = title)
  
  png(paste0("../Plots/", fname, ".png"), width = 1000, height = 600)
  print(p)
  dev.off()
}

data <- read.csv("../Data/communities_rmMissing.csv")
state_names <- read.csv("../Data/StateCode.csv")
df <- merge(data, state_names, by.x = "state", by.y = "FIPS", all.y = T)
df <- data.frame(state = df$StateName, 
                 value = df$ViolentCrimesPerPop,
                 population = df$population)
plot_by_state(df, "Real Crime Rate Per 100K Population", "real_crime")

df_decisionTree <- read.csv("../Data/pred_decisionTree.csv")
df_decisionTree <- merge(df_decisionTree, state_names, by.x = "state", 
                         by.y = "FIPS", all.y = T)
df_decisionTree <- data.frame(state = df_decisionTree$StateName,
                              value = df_decisionTree$Prediction,
                              population = df_decisionTree$population)
plot_by_state(df_decisionTree, "Predicted Crime Rate Per 100K Population Using Decision Tree",
              "pred_crime_decisionTree")

df_linear <- read.csv("../Data/pred_linear.csv")
df_linear <- merge(df_linear, state_names, by.x = "state", 
                         by.y = "FIPS", all.y = T)
df_linear <- data.frame(state = df_linear$StateName,
                              value = df_linear$pd,
                              population = df_linear$population)
plot_by_state(df_linear, "Predicted Crime Rate Per 100K Population Using Linear Regression",
              "pred_crime_linear")

df_stackedLearner <- read.csv("../Data/pred_stackedLearner.csv")
df_stackedLearner <- merge(df_stackedLearner, state_names, by.x = "state", 
                   by.y = "FIPS", all.y = T)
df_stackedLearner <- data.frame(state = df_stackedLearner$StateName,
                        value = df_stackedLearner$value,
                        population = df_stackedLearner$population)
plot_by_state(df_stackedLearner, "Predicted Crime Rate Per 100K Population Using Stacked Learner",
              "pred_crime_stackedLearner")

df_adaboost <- read.csv("../Data/pred_adaboost.csv")
df_adaboost <- merge(df_adaboost, state_names, by.x = "state", 
                           by.y = "FIPS", all.y = T)
df_adaboost <- data.frame(state = df_adaboost$StateName,
                                value = df_adaboost$value,
                                population = df_adaboost$population)
plot_by_state(df_adaboost, "Predicted Crime Rate Per 100K Population Using Adaboost",
              "pred_crime_adaboost")
