#setwd("C:/Users/Administrator/OneDrive - TCDUD.onmicrosoft.com/Final Dissertation Docs")


####Evaluating the Forced Alignment

#Reading csv data
DA25 <- read.csv("Evaluation-v1.5.csv",header=TRUE,sep=",")


# evaluating Mismatch between Manual and Automatic duration relates to longer event durations:
#Finding the mean of Manual Duration grouped with KBG.Match
with(DA25,tapply(Manual.Duration,list(KBG.Match),mean))
#Output:
#0         1
#0.9433333 0.4886947

#Finding the mean of Automatic Duration grouped with KBG.Match
with(DA25,tapply(Automatic.Duration,list(KBG.Match),mean))
#Output:
#0         1
#0.9450355 0.4886947


#As expected, there is no difference in duration in the cases of matched annotations.


with(DA25,tapply(Duration.Delta,list(KBG.Match),mean))
#Output:
#          0           1 
#0.001702128 0.000000000 


#There are more matches than mis-matches.
with(DA25,xtabs(~KBG.Match))
#Output:
#KBG.Match
#0   1
#141 475



with(DA25[DA25$KBG.Match==0,],plot(Start.Time.Delta, End.Time.Delta, main="scatterplot",las=1, xlab ="start time", ylab="end time"))
with(DA25[DA25$KBG.Match==0,],cor.test(Start.Time.Delta,End.Time.Delta,method = "spearman"))


#Where there is a mis-match, there is a relatively strong correlation between the difference in start and end times
#between the manual and automatic annotations:
 
# Spearmans rank correlation rho
# 
# data:  Start.Time.Delta and End.Time.Delta
# S = 78161, p-value < 2.2e-16
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
#        rho
# 0.8326964
# 
# There seems to be a greater magnitude of mismatch at end
# points than with start points:

with(DA25[DA25$KBG.Match==0,],summary((Start.Time.Delta-End.Time.Delta)))
#      Min.  1st Qu.   Median     Mean  3rd Qu.     Max.
# -22.0300  -0.4600  -0.1500  -0.0017   0.0400  36.5200
# >
# 

# A directed, paired wilcox test suggests that this holds
for most items:
  with(DA25[DA25$KBG.Match==0,],wilcox.test(Start.Time.Delta,End.Time.Delta,paired=TRUE,alternative="l"))

#         Wilcoxon signed rank test with continuity correction
# 
# data:  Start.Time.Delta and End.Time.Delta
#V = 2818, p-value = 1.325e-05
#alternative hypothesis: true location shift is less than 0

#This holds over the whole data set, as well.
with(DA25,wilcox.test(Start.Time.Delta,End.Time.Delta,paired=TRUE,alternative="l"))

# Wilcoxon signed rank test with continuity correction
# 
# data:  Start.Time.Delta and End.Time.Delta
# V = 2818, p-value = 1.325e-05
# alternative hypothesis: true location shift is less than 0
# 
# 
# But the difference is not sufficient to make the values of
# start time differences and end time differences to have
# a significantly different overall magnitude:

with(DA25,wilcox.test(Start.Time.Delta,End.Time.Delta,paired=FALSE,alternative="l"))

#         Wilcoxon rank sum test with continuity correction
# 
# data:  Start.Time.Delta and End.Time.Delta
# W = 189474, p-value = 0.4771
# alternative hypothesis: true location shift is less than 0
# 
# 
# 
# Only the difference in start times between manual and automatic annotation has a significant correlation with
# duration -- the correlation is with the manual duration and is weak:

with(DA25,cor.test(End.Time.Delta,Automatic.Duration,method="spearman"))

#         Spearman's rank correlation rho
# 
# data:  End.Time.Delta and Automatic.Duration
# S = 39191897, p-value = 0.8815
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
#   rho
# -0.006019836
# 
# Warning message:
#   In cor.test.default(End.Time.Delta, Automatic.Duration, method =
#                         "spearman") :
#   Cannot compute exact p-value with ties

with(DA25,cor.test(End.Time.Delta,Manual.Duration,method="spearman"))

# Spearman's rank correlation rho
# 
# data:  End.Time.Delta and Manual.Duration
# S = 36694163, p-value = 0.1498
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
#         rho
# 0.05809468
# 
# Warning message:
# In cor.test.default(End.Time.Delta, Manual.Duration, method =
# "spearman") :
#    Cannot compute exact p-value with ties

with(DA25,cor.test(Start.Time.Delta,Manual.Duration,method="spearman"))

#         Spearman's rank correlation rho
# 
# data:  Start.Time.Delta and Manual.Duration
# S = 32223333, p-value = 1.603e-05
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
#   rho
# 0.1728568
# 
# Warning message:
#   In cor.test.default(Start.Time.Delta, Manual.Duration, method =
#                         "spearman") :
#   Cannot compute exact p-value with ties

with(DA25,cor.test(Start.Time.Delta,Automatic.Duration,method="spearman"))

# Spearman's rank correlation rho
# 
# data:  Start.Time.Delta and Automatic.Duration
# S = 39566692, p-value = 0.6984
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
#          rho
# -0.01564049
# 
# Warning message:
# In cor.test.default(Start.Time.Delta, Automatic.Duration, method =
# "spearman") :
#    Cannot compute exact p-value with ties