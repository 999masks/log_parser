import re
import Tkinter

log_dir = " "
count = 0 # test test count
cases = 0
temp_result = []
fin_result  ={}  #dictionary to store test result and log file
report = {}
need_subtest = True
flag1 = False
file_name = "04_bvt_cq_celeron.log"
log_file = open (file_name, "r" )
PASSED=["PASSED"]
test_log = ""

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

if I_want_a_beer:
  drink beer
if I_want_pizza:
  eat pizza
else:
  eat apple
This means I may or may not get a beer, but I will get either pizza or apple.
Change to

elif I_want_pizza

and I get exactly one of beer, pizza and apple.
Fortunatly beer is more important than food.

'''

#print log_file

for line in log_file:  # start matchin lines
   #print line
   count +=1
   if line.startswith("-----------------"):
     flag1 = not flag1
     #print "switched", flag1, "found line at: ", count
     continue

   if flag1 and  re.match("^/", line): # log part in log file
       temp_result.append(line)
       #print "appending lines at", count
   elif len(line) < 1:
     break

   else:
     continue
log_file.close()



if need_subtest == False : # wil cover test case dot subtest feauture,
  for line_1 in temp_result:
    raw_line = re.search("^/.*?/results-\d+-([^/ \t]+)", line_1)
    if not raw_line:
      continue
    raw_test_name = raw_line.group(1)
    if not raw_test_name in report:
      cases +=1
      report[raw_test_name]=[]
    #print "test_name", test_name
    search_ps_fail = re.search("^/.+(PASSED|FAILED|FAIL|ERROR)", line_1)
    if search_ps_fail:
      if search_ps_fail.group(1) == "PASSED":
        report[raw_test_name]=PASSED
      else:
        split_line = re.search("^/\S*\s*(.*)$", line_1)
        #print split_line.group(1)
        report[raw_test_name].append(split_line.group(1))

  export_file = open("report.csv", 'w')
  for items in report:
    print items
    export_file.write(items)
  export_file.close()

elif need_subtest:
  count_line = 0
  #with ("log_file.csv" )
  for line_2 in temp_result:
    count_line +=1
    try:
      if len(line_2) > 1 and "[" in line_2:
        raw_line = re.search("^/\S+results-\d+-(\S+).*\[\s+(PASSED|FAILED|ERROR)?", line_2) # BTW ? mark at the end of brackets is indicating optional group
        raw_test_name = raw_line.group(1)
        test_status = raw_line.group(2)
        root_test=raw_test_name.split("/")[0]
        if len(raw_test_name.split("/")) >1:
           sub_test =raw_test_name.split("/")[1] # some test dont have , if they do divide subtest
        if len(line_2) > 1 and line_2.find("[")== -1: #filter out lines without result line (it should consist "[", but some line hase it too)
          print "came here"
          raw_line = re.search("^/\S+results-\d+-(\S+)\s+(.*[^\n])", line_2) # if there is no square bracket, it is error log
          test_log = raw_line.group(2)
      elif len(line_2) > 1:
        print "elif"
      #print "\n", line_2
      print "\n", "TEST_name", root_test, "TEST_status", test_status, "TEST_log", test_log
      #print "test case name", raw_test_name.group(1), "status", raw_test_name.group(2) #, "test_sttaus: ",  raw_test_name.group(2), "tets_log: ", raw_test_name.group(3)   #icarus code ("^/\S*?results-\d+-([^/ ]+)(/(\S+))?", line)
    except:
      print "error happens", line_2,

    #else:
     # break
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

else:
  print "please specify report type"


#print "error happens on:", "line is:  ", count_line, line_2, "temp result",



print "report" , report

"""
print "The answers"
for test_case in report:
  print "test_case: ", test_case
  if report[test_case] is PASSED:
    print "Well done"
  else:
    for test_case_result in report[test_case]:
      print "error log: ", "\t",test_case_result

"""



#print "log_dic", log_dic, "number of items", len(log_dic)  #cases,"-cases procesed", "\n",fin_result, "\ndictionary size is ", len(fin_result)
