---
title: "5241 project"
author: "Jiage Song"
date: "3/20/2021"
output: pdf_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```



```{r}
community <- read.csv("communities_rmMissing.csv")
head(community,5)
```



```{r}
community_numeric <- community[,-c(1,2,3)]
pca <- prcomp(community_numeric, scale=FALSE)
summary(pca)
pca$rotation
(pca$x)[1:2]#rotated centered data


```

```{r}
library(dplyr)
library(tidyverse)
crimerate <- community %>% pull(ViolentCrimesPerPop)

community$NewViolentCrimesPerPop <- community$ViolentCrimesPerPop * 699.2 + 729.6 

summary(community$NewViolentCrimesPerPop)
```

```{r}

library(dplyr)
new_community <- community %>%
  select("agePct12t29","pctUrban","MalePctDivorce","PctWorkMom", "PctPersDenseHous","HousVacant","PctHousOccup","PctVacantBoarded","NumStreet")

pca2 <- prcomp(new_community, scale=FALSE)
summary(pca2)
pca2$rotation
(pca2$x)[1:2]#rotated centered data

#install.packages("factoextra")
#install.packages("corrplot")
#install.packages("ggplot2")
library(factoextra)
library(corrplot)


# Plot the correlation circle
a <- seq(0, 2*pi, length = 100)
plot( cos(a), sin(a), type = 'l', col="gray",
      xlab = "PC1 (45.2%)",  ylab = "PC2 (18.43%)",
      main = "Projection of the First Two Pricipal Components")
abline(h = 0, v = 0, lty = 2)



# Add active variables
var_cor_func <- function(var.loadings, comp.sdev){
  var.loadings*comp.sdev
}
loadings <- pca2$rotation
sdev <- pca2$sdev
var.coord <- t(apply(loadings, 1, var_cor_func, sdev))
arrows(0, 0, var.coord[, 1], var.coord[, 2], 
       length = 0.1, angle = 15, code = 2)
text(var.coord, labels=rownames(var.coord), cex = 1, adj=1)


fviz_pca_var(pca2, col.var="contrib") +
  scale_color_gradient2(low = "red", mid = "white",
  high ="blue", midpoint=0) + theme_minimal()
fviz_contrib(pca2, choice = "var", axes = 1, top = 9)
fviz_contrib(pca2, choice = "var", axes = 2, top = 7)
fviz_contrib(pca2, choice = "var", axes = 3, top = 7)

```

