# create_est <- function(input_template){
#   # This function generates an estimation file for an input template
  
#   simple_parameters <- c()
#   complex_parameters <- c()
  
#   # Effective population size parameters
#   population_parameters <- grep("NPOP_", input_template, value = T)
#   append_me <- 
#     paste(
#       "1", population_parameters, "unif", 100, 
#       format(30*10^4, digits = 10, scientific = F), 
#       "output"
#     )
#   simple_parameters <- c(simple_parameters, append_me)
  

  
#   # Migration rate parameters
#   current_migration_parameter_location <- 
#     (as.numeric(grep("\\Migration matrix 0", input_template))+1):
#     (as.numeric(grep("\\Migration matrix 1", input_template))-1)
#   current_migration_parameters <- 
#     unique(
#       unlist(
#         str_split(input_template[current_migration_parameter_location], " ")
#       )
#     )[-1]
#   append_me <- 
#     paste("0", current_migration_parameters, "logunif 1e-10 1e-1 output")
#   simple_parameters <- c(simple_parameters, append_me)

  
#   # Resizing parameters (past population size / future population size)
#   if(any(grepl("RES_", input_template))){
#     populations <- 
#       tibble(
#         population = gsub("NPOP_", "", population_parameters),
#         period = 0,
#         tag = "",
#         parameter = population_parameters
#       )
#     resize_parameter_locations <- grep("RES_", input_template, value = F)
#     resize_parameters <- 
#       gsub(".* (RES_[a-zA-Z]*) .*", "\\1", input_template[resize_parameter_locations])
#   simple_parameters <- c(simple_parameters, paste("0", resize_parameters, "unif 0 100 output"))
#   }  
  
#   # Time parameters
#   time_parameter_locations <- grep("TDIV|TAdm", input_template)
#   time_parameters <- 
#     gsub("^(T[a-zA-Z_]*) .*$", "\\1", input_template[time_parameter_locations])
#   # Put time space between each event
#   if(length(time_parameters) == 1){
#     simple_parameters <- 
#       c(simple_parameters, paste(1, time_parameters, "unif", 1, 5000, "output"))
#   } else if(length(time_parameters) > 1){
#     simple_parameters <- 
#       c(simple_parameters, paste(1, time_parameters[1], "unif", 1, 600, "output"))
#     for(i in 2:length(time_parameters)){
#       # The space between each event
#       extra_time_parameter <- paste0("T_", i-1,"_", i)
#       simple_parameters <- 
#         c(simple_parameters, paste(1, extra_time_parameter, "unif", 0, 500, "hide"))
#       complex_parameters <- 
#         c(
#           complex_parameters, 
#           paste(
#             1, 
#             paste0(time_parameters[i]," = ", extra_time_parameter, "+", time_parameters[i-1]), 
#             "output"
#           )
#         )
#     }
#   }
  
#   # Admixture parameters
#   if(any(grepl("a_", input_template))){
#     # Migrants
#     migrants <- gsub(".* (a_[a-zA-Z]*) .*", "\\1", grep("a_", input_template, value = T))
#     append_me <- paste("0", migrants, "unif", 0, .25, "output")
#     simple_parameters <- c(simple_parameters, append_me) 

#   }
#   return(estimation(simple_parameters, complex_parameters))
# }