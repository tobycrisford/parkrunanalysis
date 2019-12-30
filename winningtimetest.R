library(DBI)
con = dbConnect(RSQLite::SQLite(), "cambridgedata.db")
dbListTables(con)

results = dbReadTable(con, "results")

dbListFields(con, "results")

winners = results[results[["position"]] == 1,]

print(winners[1:5,])

print(length(winners[,1]))

wintime = winners[winners[["time"]] > 1000,]

print(wintime[1:5,])

print(length(wintime[,1]))

sortwintime = wintime[order(wintime[["runid"]]),]

gaps = array(0,dim=length(sortwintime[,1])-1)
for (i in 1:length(gaps)) {gaps[i] = sortwintime[i+1,"runid"] - sortwintime[i,"runid"]}
hist(gaps)

library(MASS)
f = fitdistr(gaps - 1, "geometric")
print(f["estimate"])

ct = table(factor(gaps-1,levels=0:(10*max(gaps))))
print(ct)
param = as.double(f["estimate"])
chisq.test(ct, p = param*(1-param)^(0:(10*max(gaps))),simulate.p.value=TRUE)

dbDisconnect(con)