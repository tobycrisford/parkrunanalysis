library(DBI)
library(lmerTest)
con = dbConnect(RSQLite::SQLite(), "cambridgedata.db")
dbListTables(con)

results = dbReadTable(con, "results")

dbListFields(con, "results")

results[["gender"]] = factor(results[["gender"]])

par(mfrow=c(1,3))
plot(results[["gender"]],1000/results[["time"]])
hist(1000/results[results[["gender"]] == "M","time"],main="M")
hist(1000/results[results[["gender"]] == "F","time"],main="F")

dbDisconnect(con)