tocompare = c("SW25-29", "VM65-69")

library(DBI)
library(lmerTest)
con = dbConnect(RSQLite::SQLite(), "cambridgedata.db")
dbListTables(con)

results = dbReadTable(con, "results")

dbListFields(con, "results")

cropresults = results[(results[["age"]] == tocompare[1]) | (results[["age"]] == tocompare[2]),]

print(cropresults[1:5,])

cropresults[["age"]] = factor(cropresults[["age"]])
cropresults[["runnerid"]] = factor(cropresults[["runnerid"]])
cropresults[["runid"]] = factor(cropresults[["runid"]])

par(mfrow=c(1,3))
plot(cropresults[["age"]],1000/cropresults[["time"]])
results1 = 1000/cropresults[cropresults[["age"]] == tocompare[1],"time"]
qqnorm(results1, main=tocompare[1])
qqline(results1)
results2 = 1000/cropresults[cropresults[["age"]] == tocompare[2],"time"]
qqnorm(results2, main=tocompare[2])
qqline(results2)

#bad model
attach(cropresults)
y = 1000/time
summary(lm(y ~ age))
detach(cropresults)

#better model
attach(cropresults)
y = 1000/time
model = lmer(y ~ age + (1|runid) + (1|runnerid))
summary(model)
detach(cropresults)

dbDisconnect(con)