from lib.database.mysql import WorkBench



wb = WorkBench()

wb.use('yumo')
print(wb.show(False))

print(wb.info.get_fetchs("yumo", "yuanshen"))