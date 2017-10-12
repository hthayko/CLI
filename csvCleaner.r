setwd("~/CLI/")
orig = read.csv(file ="tmp/sp_contacts.csv")
ret = data.frame(
  first_name = as.character(orig$First.Name),
  last_name = as.character(orig$Last.Name),
  phone_number = as.character(orig$Phone),
  email = as.character(orig$Email),
  zip_code = as.character(orig$Zip.Code),
  birthday = as.character(orig$Birthday),
  stringsAsFactors = FALSE
)
a = as.character(orig$Phone)
ret = ret[substr(ret$phone_number, 0, 1) == "1" & nchar(ret$phone_number) == 11 & !is.na(ret$phone_number),]
ret$zip_code[nchar(ret$zip_code) < 4 | nchar(ret$zip_code) > 5] = ""
ret$zip_code[!grepl("[0-9]+$", ret$zip_code)] = ""
write.csv(ret, file ="tmp/sp_contacts_ready.csv", row.names = FALSE)
