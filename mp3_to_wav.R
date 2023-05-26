
library(tuneR)

source_path <- '/mp3'
destin_path <- '/wav'

file_names <- list.files(source_path)

counter <- 0 

for (filename in file_names){
  
  counter <- counter + 1 
  
  if (counter %% 10 == 0){
    print(counter)
  }
  
  name = substr(filename,1,nchar(filename)-3)
  
  r <- readMP3(paste(source_path, '/' , filename, sep=''))
  writeWave(r,paste(destin_path, '/' , name, 'wav', sep=''), extensible=FALSE)
  
}
  
