import re
import Tkinter

log_dir = " "
count = 0 # test test count
cases = 0
temp_result = []
fin_result  ={}  #dictionary to store test result and log file
report = {}
need_subtest = False
flag1 = False
file_name = "graphics_WW22_RVP7-1.log"
log_file = open (file_name, "r" )
PASSED=["PASSED"]

'''
log file -/tmp/test_that_results_RZxzsK/results-01-graphics_Stress.tabopenclose                                       [  FAILED  ]
/tmp/test_that_results_RZxzsK/results-01-graphics_Stress.tabopenclose                                         FAIL: Unhandled LoginException: Timed out going through login screen
/tmp/test_that_results_RZxzsK/results-01-graphics_Stress.tabopenclose/graphics_Stress                       [  FAILED  ]
junk chars
/tmp/test_that_results_RZxzsK/graphics_Stress.tabopenclose/graphics_Stress                         FAIL: Unhandled LoginException: Timed out going through login screen
/home/cssdesk/trunk/chroot/logs/telemetry_GpuTests_screenshot_sync_2015_12_14_16_33_09/results-1-telemetry_GpuTests.screenshot_sync                    [  PASSED  ] [^ghj ]
/tmp/test_that_results_bZJx4v/results-56-graphics_LibDRM                                                    [  PASSED  ]
/home/cssdesk/trunk/chroot/logs/f___platform_ExternalUsbPeripherals_control_2015_12_11_22_39_40/results-1-platform_ExternalUsbPeripherals/platform_ExternalUsbPeripherals                       [  PASSED  ]
/home/cssdesk/trunk/chroot/logs/f___platform_ExternalUsbPeripherals_control_2015_12_11_22_39_40/results-1-platform_ExternalUsbPeripherals/platform_ExternalUsbPeripherals/desktopui_SimpleLogin [  PASSED  ]
/tmp/test_that_results_C6tpdR/results-01-platform_DMVerityBitCorruption/platform_DMVerityBitCorruption.first  [  PASSED  ]
'''

#print log_file
try:
  for line in log_file:  # start matchin lines
     #print line
     count +=1
     if line.startswith("-----------------"):
       flag1 = not flag1
       print "switched", flag1, "found line at: ", count
       continue

     if flag1 and  re.match("^/", line): # log part in log file
         temp_result.append(line)
         print "appending lines at", count

     else:
       continue
  log_file.close()



  if need_subtest == False : # wil cover test case dot subtest feauture,
    for line in temp_result:
      raw_test_name = re.search("^/.*?/results-\d+-([^/ \t]+)", line)
      if not raw_test_name:
        continue
      test_name = raw_test_name.group(1)
      if not test_name in report:
        cases +=1
        report[test_name]=[]
      #print "test_name", test_name
      search_ps_fail = re.search("^/.+(PASSED|FAILED|FAIL|ERROR)", line)
      if search_ps_fail:
        if search_ps_fail.group(1) == "PASSED":
          report[test_name]=PASSED
        else:
          split_line = re.search("^/\S*\s*(.*)$", line)
          #print split_line.group(1)
          report[test_name].append(split_line.group(1))

    export_file = open("report.csv", 'w')
    for items in report:
      print items
      export_file.write(items)
    export_file.close()

  elif need_subtest:
    for line in temp_result:
      raw_test_name = re.search("^/.*\S/results-\d+-([^/ \t])", line) # ? mark at the end of brackets is indicating optional group
      print raw_test_name.group(1)   #icarus code ("^/\S*?results-\d+-([^/ ]+)(/(\S+))?", line)
      # cases +=1
      # test_name = (raw_test_name.group(2)).split(".")[0]
      # print  test_name
      # search_ps_fail = re.search("^/.+(PASSED|FAILED|FAIL|ERROR)", line)
      # ps_fail = search_ps_fail.group(1)
      # print ps_fail
      # n_test_name = " "
      # if test_name not in fin_result:     # if test_name != n_test_name:   #avoid to add same test case neme in dictionary,
      #                                     # keep first result, not subtest result e.g. keep FAILED instead of error
      #   fin_result[test_name]= ps_fail



except:
  print "error happens on:",count, "line is: ", line, "temp result"

else:
  print "please specify report type"

#print "report" , report

'''
#print "The answers", temp_result
for test_case in report:
  print "test_case: ", test_case
  if report[test_case] is PASSED:
    print "Well done"
  else:
    for test_case_result in report[test_case]:
      print "error log: ", "\t",test_case_result





#print "log_dic", log_dic, "number of items", len(log_dic)  #cases,"-cases procesed", "\n",fin_result, "\ndictionary size is ", len(fin_result)
'''