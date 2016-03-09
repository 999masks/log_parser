import re
import Tkinter

log_dir = " "
count = 0 # test test count
cases = 0
temp_result = []
fin_result  ={}  #dictionary to store test result and log file
log_dic = {}
need_subtest = False

switch = False
file_name = "graphics_WW22_RVP7.log"
log_file = open (file_name, "r" )
#print log_file
try:
  for line in log_file:  # start matchin lines
     #print line
     count +=1
     if re.match("^\-\-+", line):
       if switch == False:
          switch = True
          print "switched true", "found line at: ", count
       else:
         switch = False
         print "switshed to false", count
         break


     elif switch and  re.match("^\/", line): # log part in log file
         temp_result.append(line)
         #print "appending lines at", count

     else:
         switch = False
         continue
         print "this line not consist failure logs", line, count

  if need_subtest != True: # wil cover test case dot subtest feauture,
    for line_1 in temp_result:
      raw_test_name = re.search("(/+\S+/results-\d+-\S+/|/+\S+/results-\d+-)(\S+)", line_1)
      cases +=1
      test_name = raw_test_name.group(2)
      #print "test_name", test_name
      search_ps_fail = re.search("^/.+(PASSED|FAILED|FAIL|ERROR)", line_1)
      ps_fail = search_ps_fail.group(1)
      #print "Pass/Fail", ps_fail
      #print line_1
      test_name_list = []
      if "[  PASSED  ]" not in line_1:
        raw_exec_logs = re.search("^/\S+(\s+([^[]+))", line_1)
        exec_log = raw_exec_logs.group(2)
        #print "exec_logs", exec_log

        if len(exec_log) < 2:
          test_name_list = "no logs are generaed"
        else:
          log_dic[test_name]=test_name_list.append(exec_log)
        #print "test_name_list", test_name_list
        log_dic[test_name]=test_name_list
      elif "FAILED" or "FAIL" or "ERROR" not in line_1:
        test_name_list.append("PASS")
        log_dic[test_name]=test_name_list

  elif need_subtest:
    for line_1 in temp_result:
      raw_test_name = re.search("(/+\S+/results-\d+-\S+/|/+\S+/results-\d+-)(\S+)", line_1)
      cases +=1
      test_name = (raw_test_name.group(2)).split(".")[0]
      print  "test_name",  test_name
      search_ps_fail = re.search("^/.+(PASSED|FAILED|FAIL|ERROR)", line_1)
      ps_fail = search_ps_fail.group(1)
      print ps_fail
      n_test_name = " "
      if test_name not in fin_result:     # if test_name != n_test_name:   #avoid to add same test case neme in dictionary,
                                          # keep first result, not subtest result e.g. keep FAILED instead of error
        fin_result[test_name]= ps_fail

except:
  print "error happens on:",count, "line is: ", line, "temp result", temp_result
print temp_result
'''
else:
  print "please specify report type"
'''

#TODO not correct parsing stres test





#print "log_dic", log_dic, "number of items", len(log_dic)  #cases,"-cases procesed", "\n",fin_result, "\ndictionary size is ", len(fin_result)