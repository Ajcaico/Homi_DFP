#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Daniel Lesser Public PA School Data import

#NotebookApp.iopub_data_rate_limit=10000000.0 (bytes/sec)
#NotebookApp.rate_limit_window=10.0 (secs)
import pandas as pd

schools = {}
#columns = []
AlleghenyZipcodes = {'15101','15003','15005','15006','15007','15102','15014','15104','15015','15017',
                 '15018','15020','15106','15024','15025','15026','15108','15028','15030','15046',
                 '15031','15034','15110','15035','15112','15037','15332','15044','15045','15116',
                 '15047','15049','15120','15126','15051','15642','15056','16046','15057','15136',
                 '15131','15132','15133','15135','15063','15146','15064','15668','15065','15068',
                 '15137','15071','15139','15140','15201','15202','15203','15204','15205','15206',
                 '15207','15208','15209','15210','15211','15212','15213','15214','15215','15216',
                 '15217','15218','15219','15220','15221','15222','15223','15224','15225','15226',
                 '15227','15228','15229','15232','15233','15234','15235','15236','15237','15238',
                 '15239','15241','15243','15260','15290','15142','15075','15076','16055','15143',
                 '15129','15144','15082','15084','15085','15145','16059','15147','15086','15088',
                 '15122','15089','15090','15148'}
SchoolComplete = []
AlleghenySchools = {}
AlleghenySchoolZipAgg = {}

def ReadFiles_M():
    fin = open("SPP.APD.2016.2017.txt", "rt", encoding = 'utf-8')
    if(fin.mode == 'rt'):
        header = next(fin) #grabs header line
        headerRow = header.rstrip('\n').split("|")
        counter = 0
        TotalRows = 0
        for line in fin:      # read file line by line, search, and write table attributes to tuple
            if (counter == 0): #for first time going through, creates a new school list
                school = []
                row = line.rstrip('\n').split("|")
                school.extend([row[0], row[1], row[2], row[3], row[5]])  
                counter+=1
            elif (counter <45): #grabs and appends all attributes in APD file to school list
                row = line.rstrip('\n').split("|")
                school.append(row[5])
                counter+=1
            else: #at end of school, adds the school to the dictionary and starts over again
                schools[school[2]+"."+school[3]] = school
                school = []
                row = line.rstrip('\n').split("|")
                school.extend([row[0], row[1], row[2], row[3], row[5]])
                counter = 1
            TotalRows+=1

    fin.close()

    fin = open("SPP.FF.2016.2017.txt", "rt", encoding = 'utf-8') #reading through 2nd file to grab relevant stats
    if(fin.mode == 'rt'):
        for line in fin:
            row = line.rstrip('\n').split("|")
            school = schools.get(row[2]+"."+row[3],None) #grabs the relevant school with the key
            if school != None: #adds the relevant stats to the school
                if row[4] == 'Dropout Rate (Percent)':
                    school.append(row[5])
                if row[4] == 'Economically Disadvantaged':
                    school.append(row[5])
                if row[4] == 'Number of Advanced Placement Courses Offered':
                    school.append(row[5])
                if row[4] == 'Percent of Gifted Students':
                    school.append(row[5]) 
                if row[4] == 'School Address (City)':
                    school.append(row[5])
                if row[4] == 'School Address (State)':
                    school.append(row[5])
                if row[4] == 'School Address (Street)':
                    school.append(row[5])
                if row[4] == 'School Enrollment':
                    school.append(row[5])
                if row[4] == 'School Zip Code':
                    school.append(row[5])
                schools[school[2]+"."+school[3]] = school #puts back into dictionary with new info

    fin.close()


#Method for narrowing zip codes to Allegheny County
def NarrowAllegheny_M():

    for key, value in schools.items():
        if value[-1] in AlleghenyZipcodes:
            AlleghenySchools[key] = value

#Creating a list of schools where each school has a list of individual attributes
#necessary for writing out to excel using panda dataframes

def SchoolListList_M():

    for key,value in schools.items():
        tempList = []
        tempList.append(key)
        tempList.extend(value)

        SchoolComplete.append(tempList) 
        
#relevant attributes:
#Attendance Rate #Index:[8]
#Calculated Score #Index:[11]
#Graduation Rate #Index[12]
#ELA/Literature- Percent Proficient or Advanced on PSSA/Keystone #Index[18]
#Final Academic Score #Index[19]
#Mathematics/Algebra I - Percent Proficient or Advanced on PSSA/Keystone Exam #Index[29]
#Science/Biology - Percent Proficient or Advanced on PSSA/Keystone #Index[48]
#Dropout Rate (Percent) #Index[49]
#Economically Disadvantaged #Index[50]
#Number of Advanced Placement Courses Offered #Index[51]
#Percent of Gifted Students #Index[52]
#School Enrollment #Index[56]
#School Zip Code #Index[57]

def ZipAgg_M():
    #method for giving 1 row per zip code of all relevant attributes.

    for zip in AlleghenyZipcodes:
        localSchools = {}

        #Measures
        AttendanceRate = 0
        Calc_Score = 0
        Grad_Rate = 0
        Lit_PSSA = 0
        Final_Academic_Score = 0
        Math_PSSA = 0
        Science_PSSA = 0
        Dropout_Rate = 0
        Economically_Disadvantage = 0
        Num_AP = 0
        Num_Gifted = 0
        School_Enrollment = 0

        #Counts
        AttendanceRate_c = 0
        Calc_Score_c = 0
        Grad_Rate_c = 0
        Lit_PSSA_c = 0
        Final_Academic_Score_c = 0
        Math_PSSA_c = 0
        Science_PSSA_c = 0
        Dropout_Rate_c = 0
        Economically_Disadvantage_c = 0
        Num_AP_c = 0
        Num_Gifted_c = 0
        School_Enrollment_c = 0

        #print("checked zipcode is: ", zip)     
        #adds schools within the zip code to a local dict
        for key, value in schools.items():
            #print("school zipcode is: ", value[-1])
            if value[-1] == zip:
                localSchools[key] = value  
        #print(len(localSchools))
        if(len(localSchools)>0):


        #Testing print statements to check for population of zip pivot
        #    print("num schools: ", len(localSchools))
        #    for key, value in localSchools.items():
        #        print(key, value)
        #        try:
        #            print("attendance:", float(value[8]))
        #        except:
        #            print("attendance:", value[8])
        #        try:               
        #            print("score:", float(value[11]))
        #        except:
        #            print("score:", value[11])
        #        try:
        #            print("grad:", float(value[12]))
        #        except:
        #            print("grad:", value[12])
        #        try:
        #            print("lit:", float(value[18]))
        #        except:
        #            print("lit:", value[18])
        #        try:
        #            print("final_ac:", float(value[19]))
        #        except:
        #            print("final_ac:", value[19])
        #        try:
        #            print("math:", float(value[29]))
        #        except:
        #            print("math:", value[29])
        #        try:
        #            print("science:", float(value[48]))
        #        except:
        #            print("science:", value[48])
        #        try:
        #           print("dropout:", float(value[49]))
        #        except:
        #            print("dropout:", value[49])
        #        try:
        #            print("econ disad:", float(value[50]))
        #        except:
        #            print("econ disad:", value[50])
        #       try:
        #            print("num_ap:", float(value[51]))
        #        except:
        #            print("num_ap:", value[51])
        #        try:
        #            print("num_gift:", float(value[52]))
        #        except:
        #            print("num_gift:", value[52])
        #        try:
        #            print("School_Enroll:", float(value[56]))
        #        except:
        #            print("School_Enroll:", value[56])

            #run through the local schools and calculate averages
            School_Count = 0
            for key, value in localSchools.items():
                School_Count+=1
                try:
                    AttendanceRate += float(value[8])
                    AttendanceRate_c+=1
                except:
                    None
                try:
                    Calc_Score += float(value[11])
                    Calc_Score_c+=1
                except:
                    None
                try:
                    Grad_Rate += float(value[12])
                    Grad_Rate_c+=1
                except:
                    None
                try:
                    Lit_PSSA += float(value[18])
                    Lit_PSSA_c+=1
                except:
                    None
                try:
                    Final_Academic_Score += float(value[19])
                    Final_Academic_Score_c+=1
                except:
                    None
                try:
                    Math_PSSA += float(value[29])
                    Math_PSSA_c+=1
                except:
                    None
                try:
                    Science_PSSA += float(value[48])
                    Science_PSSA_c+=1
                except:
                    None
                try:
                    Dropout_Rate += float(value[49])
                    Dropout_Rate_c+=1
                except:
                    None
                try:
                    Economically_Disadvantage += float(value[50])
                    Economically_Disadvantage_c+=1
                except:
                    None
                try:
                    Num_AP += float(value[51])
                    Num_AP_c+=1
                except:
                    None
                try:
                    Num_Gifted += float(value[52])
                    Num_Gifted_c+=1
                except:
                    None
                try:
                    School_Enrollment +=float(value[56])
                    School_Enrollment_c+=1
                except:
                    None

        #testing print statements    
            #print("attendance:", AttendanceRate, AttendanceRate_c)
            #print("score:", Calc_Score, Calc_Score_c)
            #print("grad:", Grad_Rate, Grad_Rate_c)
            #print("lit:", Lit_PSSA, Lit_PSSA_c)
            #print("final_ac:", Final_Academic_Score, Final_Academic_Score_c)
            #print("math:", Math_PSSA, Math_PSSA_c)
            #print("science:", Science_PSSA, Science_PSSA_c)
            #print("dropout:", Dropout_Rate, Dropout_Rate_c)
            #print("econ disad:", Economically_Disadvantage, Economically_Disadvantage_c)
            #print("num_ap:", Num_AP, Num_AP_c)
            #print("num_gift:", Num_Gifted, Num_Gifted_c)
            #print("School_Enroll:", School_Enrollment, School_Enrollment_c)


            #calc averages
            try:
                AttendanceRate /= AttendanceRate_c
            except:
                AttendanceRate = 0
            try:
                Calc_Score /= Calc_Score_c
            except:
                Calc_Score = 0
            try:
                Grad_Rate /= Grad_Rate_c
            except:
                Grad_Rate = 0
            try:
                Lit_PSSA /= Lit_PSSA_c
            except:
                Lit_PSSA = 0
            try:
                Final_Academic_Score /= Final_Academic_Score_c
            except:
                Final_Academic_Score = 0
            try:
                Math_PSSA /= Math_PSSA_c
            except:
                Math_PSSA = 0
            try:
                Science_PSSA /= Science_PSSA_c
            except:
                Science_PSSA = 0
            try:
                Dropout_Rate /= Dropout_Rate_c
            except:
                Dropout_Rate= 0
            try:
                Economically_Disadvantage /= School_Enrollment
            except:
                Economically_Disadvantage = 0
            try:
                Num_AP /= Num_AP_c
            except:
                Num_AP=0
            try:
                Num_Gifted /= School_Enrollment
            except:
                Num_Gifted = 0
            try:
                Avg_Enroll = School_Enrollment/School_Enrollment_c
            except:
                Avg_Enroll = 0

            #Blended Score out of 100
            BlendedScore = ((0.3)*Final_Academic_Score + (0.2)*Calc_Score + (0.1)*AttendanceRate
                            + (0.1)*Grad_Rate + (0.2)*Lit_PSSA + (0.2)*Math_PSSA + (0.1)*Science_PSSA
                            + (0.1)*Num_AP*10 + (0.1)*Num_Gifted - (0.2)*Dropout_Rate
                            - (0.2)*Economically_Disadvantage)

            schoolAgg = [AttendanceRate, Calc_Score, Grad_Rate, Lit_PSSA, Final_Academic_Score,
                             Math_PSSA, Science_PSSA, Dropout_Rate, Economically_Disadvantage, 
                             Num_AP, Num_Gifted, Avg_Enroll,School_Count,BlendedScore]


            Category_Set = {'AttendanceRate', 'Calc_Score', 'Grad_Rate', 'Lit_PSSA', 'Final_Academic_Score',
                           'Math_PSSA', 'Science_PSSA', 'Dropout_Rate', 'Economically_Disadvantage', 
                           'Num_AP', 'Num_Gifted', 'Avg_Enroll', 'School_Count', 'BlendedScore'}

            AlleghenySchoolZipAgg[zip] = {'AttendanceRate': AttendanceRate, 'Calc_Score': Calc_Score,
                'Grad_Rate': Grad_Rate, 'Lit_PSSA': Lit_PSSA, 'Final_Academic_Score': Final_Academic_Score,
                'Math_PSSA': Math_PSSA, 'Science_PSSA': Science_PSSA, 'Dropout_Rate': Dropout_Rate, 
                'Economically_Disadvantage': Economically_Disadvantage, 'Num_AP': Num_AP,
                'Num_Gifted': Num_Gifted, 'Avg_Enroll': Avg_Enroll, 'School_Count': School_Count,
                'BlendedScore': BlendedScore} 

        
def printToExcel_M():
    df = pd.DataFrame(AlleghenySchoolZipAgg).T
    df.to_excel('AggregateData.xlsx')
    
    df2 = pd.DataFrame(SchoolComplete)
    df2.to_excel('CompleteData.xlsx')



def testPrintStatements():
    print("done with local schools")
    print("Allegheny School Count:", len(AlleghenySchools))
    print("Number of zips: ", len(AlleghenyZipcodes))
    print("ZipCode School Aggregate Count:",len(AlleghenySchoolZipAgg))

    for key,value in AlleghenySchoolZipAgg.items():
        print("Zipcode: ", key)
        print("Academic Score: ", value['AttendanceRate'], "Blended: ", value['Calc_Score'])


    #for Quality checking purposes.
    #print(columns)
    for key, value in schools.items():
        print(key,end=",")
        print(value)
        print("")
    #print("Total Rows: " + str(TotalRows))    
    #print(schools.items)
    #print(AlleghenyZips)
    #for key, value in AlleghenySchools.items():
    #    print(key,end=",")
    #    print(value)
    #    print("")
    #print("PA School Count:", len(schools))
    #print("Allegheny School Count:", len(AlleghenySchools)) 

def ReturnAggregate():
    return pd.DataFrame(AlleghenySchoolZipAgg).T

#Main Method
def SchoolMainMethod_M():
    ReadFiles_M()
    NarrowAllegheny_M()
    SchoolListList_M()
    ZipAgg_M()
    printToExcel_M()


# In[ ]:


##openpyxl version.  Pandas a lot easier!
#don't use this code

#import openpyxl as op
#wb = op.Workbook()

#Create 2 tabs
#ws1 = wb.create_sheet("Complete_data")
#ws2 = wb.create_sheet("Aggregate_data")

#Writing to aggregate data tab
#ws2 = wb.active
#for key,value in AlleghenySchoolZipAgg.items():
    
    
#    print("Zipcode: ", key)
#    print("Academic Score: ", value['AttendanceRate'], "Blended: ", value['Calc_Score'])

#wb.save('SchoolsData.xlsx')


#wb[ws1]['B4'] = "testing"


# In[3]:


SchoolMainMethod_M()


# In[ ]:







# In[ ]:




