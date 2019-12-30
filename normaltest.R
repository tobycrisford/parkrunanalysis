library(DBI)
con = dbConnect(RSQLite::SQLite(), "cambridgedata.db")
dbListTables(con)

results = dbReadTable(con, "results")

dbListFields(con, "results")

par(mfrow=c(2,2))

hist(results[["time"]])

qqnorm(results[["time"]])

qqline(results[["time"]])

hist(1000/results[["time"]])

qqnorm(1000/results[["time"]])

qqline(1000/results[["time"]])

dbDisconnect(con)