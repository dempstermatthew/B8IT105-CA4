import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class VizualResult(object): 
    def __init__(self, filename):
        self.filename = filename
        self.__df = None
    ##load the changes.csv that was created from the change_log.csv
    def loadChangesFile(self):
        df = pd.read_csv(self.filename, sep ='\t',   error_bad_lines = False
                         )
        return df
    ## viewing of data in the data frane
    def lookAtDataInDataframe(self, df):
        print(df.head())  ## try see all the data
        print(df.keys())  ## check the key values
        print(df[df.columns[0:8]])  ## don't show comment
        print(df.describe())  # look mean, max
        print(df.loc[2,:]) ## get a particular row
        print(df.iloc[5][0])  ## get particular column in the row
        
    ##populate the dataframe so other methods can use it.
    def setDataframe(self, value):
        self.__df = value
    ## return the dta frame so other methods can us it    
    def getDataframe(self):
        return self.__df 
    
    #copy dataframe to DfAuthor data frame and delete columns that are not need
    #should be left with the fields author and no_of_lines in the data frame
    def getAuthorLine(self):
        dfAuthor = self.__df.copy()
        dfAuthor.drop('revision',1, inplace=True)
        dfAuthor.drop('comment',1,inplace=True )
        dfAuthor.drop('date',1,inplace=True )
        dfAuthor.drop('time',1,inplace=True )
        dfAuthor.drop('add',1,inplace=True )
        dfAuthor.drop('del',1,inplace=True )
        dfAuthor.drop('edit',1,inplace=True )
        return dfAuthor
    ###copy dataframe to dfAuthorDate data frame and delete columns that are not need
    #should be left with the fields author, date and no_of_lines in the data frame
    def getAuthorDateLine(self):
        dfAuthorDate = self.__df.copy()
        dfAuthorDate.drop('revision',1, inplace=True)
        dfAuthorDate.drop('comment',1,inplace=True )
        dfAuthorDate.drop('time',1,inplace=True )
        dfAuthorDate.drop('add',1,inplace=True )
        dfAuthorDate.drop('del',1,inplace=True )
        dfAuthorDate.drop('edit',1,inplace=True )
        return dfAuthorDate
    
    ###copy dataframe to dfTime data frame and delete columns that are not need
    #should be left with the fields hour no_of_lines in the data frame
    def getTimeLine(self):
        dfTime = self.__df.copy()
        dfTime.drop('revision',1, inplace=True)
        dfTime.drop('author',1, inplace=True)
        dfTime.drop('comment',1,inplace=True )
        dfTime.drop('date',1,inplace=True )
        dfTime['hour'] = pd.to_datetime(dfTime['time'], format='%H:%M:%S').dt.hour
        dfTime.drop('time',1,inplace=True )
        dfTime.drop('add',1,inplace=True )
        dfTime.drop('del',1,inplace=True )
        dfTime.drop('edit',1,inplace=True )
        return dfTime
    ###copy dataframe to dfAuthorTime data frame and delete columns that are not need
    #should be left with the fields author, hour and no_of_lines in the data frame
    def getAuthorTimeLine(self):
        dfAuthorTime = self.__df.copy()
        dfAuthorTime.drop('revision',1, inplace=True)
        dfAuthorTime.drop('comment',1,inplace=True )
        dfAuthorTime.drop('date',1,inplace=True )
        dfAuthorTime['hour'] = pd.to_datetime(dfAuthorTime['time'], format='%H:%M:%S').dt.hour
        dfAuthorTime.drop('time',1,inplace=True )
        dfAuthorTime.drop('add',1,inplace=True )
        dfAuthorTime.drop('del',1,inplace=True )
        dfAuthorTime.drop('edit',1,inplace=True )
        return dfAuthorTime
   
    ##changes to files by commit
    def getAuthorAddDelEdit(self):
        dfAuthorAddEditDel = self.__df.copy()
        dfAuthorAddEditDel.drop('revision',1, inplace=True)
        dfAuthorAddEditDel.drop('comment',1,inplace=True )
        dfAuthorAddEditDel.drop('date',1,inplace=True )
        dfAuthorAddEditDel.drop('time',1,inplace=True )
        dfAuthorAddEditDel.drop('no_of_lines',1,inplace=True )
        return dfAuthorAddEditDel
    
    ## take a dataframe and add two colums two it
    ##take the date field and make sure it is a date field not a string.
    ##use the date field to get the day of the week
    ##then only out the rros in the dataframe that are eith Sat or Sun
    ##used to find out who is working on a sat or sun.
    def getAuthorSatSunLineCounts(self,dfAuthorDate):
         dfAuthorDate['my_dates'] = pd.to_datetime(dfAuthorDate['date'])
         dfAuthorDate['day_of_week'] = dfAuthorDate['my_dates'].dt.day_name()
         dfAuthorSun = dfAuthorDate[dfAuthorDate.day_of_week == 'Sunday']
         dfAuthorSat = dfAuthorDate[dfAuthorDate.day_of_week == 'Saturday']
         dfAuthorSatSun = pd.concat([dfAuthorSat, dfAuthorSun], ignore_index=True)
         dfAuthorSatSun.drop('my_dates',1,inplace=True )
         return(dfAuthorSatSun)
    ## group data frame by author to see number of files Added, Deleted, and Modified during each commit    
    def getAuthorAddEditDelCounts(self,dfAuthorAddEditDel):
         print(dfAuthorAddEditDel.keys())
         df_totals = dfAuthorAddEditDel.groupby('author').sum()
         df_totals['GrandTot'] = df_totals['add'] + df_totals['del'] + df_totals['edit']
         return df_totals
         
    ##group data frame by author and sum the no_of_lines , to show number of lines booked in by author
    def getAuthorLineCounts(self,dfAuthor):
         dfAuthor = dfAuthor.groupby(['author']).sum().sort_values(by=['no_of_lines', 'author'], ascending=[False, True])
         return dfAuthor
     
    ##group data frame by author and date and sum the no_of_lines , to show number of lines booked in by author and what date they did this on
    def getAuthorDateLineCounts(self,dfAuthorDate):
         return(dfAuthorDate.groupby(['date','author']).sum().sort_values(by=['date','no_of_lines', 'author'], ascending=[True, False,True]))
    
    ##group data frame by hour and sum the no_of_lines , to show number of lines booked in by the hour         
    def getTimeLineCounts(self,dfAuthorTime):
         return(dfAuthorTime.groupby(['hour']).sum().sort_values(by=['hour'], ascending=[True]))
    ##group data frame by hour,author, and sum the no_of_lines , to show number of lines booked in by the hour     and by who    
    def getAuthorTimeLineCounts(self,dfAuthorTime):
         return(dfAuthorTime.groupby(['hour','author']).sum().sort_values(by=['hour', 'no_of_lines', ], ascending=[False, False]))
         
def initialSetup():     
    viz = VizualResult('changes.csv')
    df = viz.loadChangesFile()  ##loading changes file
    viz.setDataframe(df)  ##set data frame         
    return viz

def loadDataFrame(viz):
    df = viz.getDataframe() ##get data frame 
    return df

def getAuthorInfo(viz):
    dfAuthor =viz.getAuthorLine() ##dataframe with author and no of lines in the dataframe
    return dfAuthor

def getAuthorLineCount(viz, dfAuthor): # groups the dataframe by author and sums no_of_lines
    dfAuthorCnt = viz.getAuthorLineCounts(dfAuthor)
    return dfAuthorCnt

def getAuthorDateLineInfo(viz):
     dfAuthorDate =viz.getAuthorDateLine() ##dataframe with author date and no of lines in the dataframe
     return dfAuthorDate

def getAuthorDateLineCounts(viz, dfAuthorDate): # groups the dataframe by author, date and sums no_of_lines
    dfAuthorDateCnt = viz.getAuthorDateLineCounts(dfAuthorDate)
    return dfAuthorDateCnt

def getAuthorAddDelEditInfo(viz): # groups the dataframe byauthor add,edit and del
    dfAuthorAddEditDel = viz.getAuthorAddDelEdit()
    return dfAuthorAddEditDel 

def getAuthorSatSunLineCounts(viz, dfAuthorDate): # groups the dataframe by author, date and sums no_of_lines has only sat and sun
    dfAuthorSatSun = viz.getAuthorSatSunLineCounts(dfAuthorDate)
    return dfAuthorSatSun 

def getTimeLineInfo(viz):
     dfAuthorTime =viz.getTimeLine()  ##lines code checked in by hour
     return dfAuthorTime  

def getTimeLineCounts(viz, dfAuthorTime): # groups the dataframe by hour and sums no_of_lines
    dfAuthorTimeCnt = viz.getTimeLineCounts(dfAuthorTime)
    return dfAuthorTimeCnt

def getAuthorTimeLineInfo(viz):
     dfAuthorTime =viz.getAuthorTimeLine()  ##lines code checked in by hour and author
     return dfAuthorTime 

def getAuthorTimeLineCounts(viz, dfAuthorTime): # groups the dataframe by hour, author and sums no_of_lines
    dfAuthorTimeCnt = viz.getAuthorTimeLineCounts(dfAuthorTime)
    return dfAuthorTimeCnt 

def getAuthorAddEditDelCounts(viz, dfAuthorAddEditDel): # groups the dataframe by hour, author and sums no_of_lines
    dfAuthorAddEditDelCnt = viz.getAuthorAddEditDelCounts(dfAuthorAddEditDel)
    return dfAuthorAddEditDelCnt 


if __name__ == '__main__':
    viz = initialSetup()
    df = loadDataFrame(viz) ##get data frame 
    viz.lookAtDataInDataframe(df) ##viewing data
    
    dfAuthor= getAuthorInfo(viz)
    print(getAuthorLineCount(viz, dfAuthor))
    
    dfAuthorDate =getAuthorDateLineInfo(viz)
    print(getAuthorDateLineCounts(viz, dfAuthorDate))  
    print(getAuthorSatSunLineCounts(viz, dfAuthorDate))## who worked sat or sun
    
    dfAuthorTime =getTimeLineInfo(viz)  ##lines code checked in by hour
    print(getTimeLineCounts(viz,dfAuthorTime))
    
    dfAuthorTime =getAuthorTimeLineInfo(viz)
    print(getAuthorTimeLineCounts(viz,dfAuthorTime)) 
    
    ###changes by comitt by add,del and edit
    dfAuthorAddEditDel =getAuthorAddDelEdit(viz) 
    Authounts = getAuthorAddEditDelCounts(viz,dfAuthorAddEditDel)
    Authounts.reset_index(inplace=True)
    
    ##graphs - author and no lines
    df = viz.getAuthorLineCounts(dfAuthor)
    
    
    
    pos = np.arange(len(df.no_of_lines))
    plt.barh(pos,df.no_of_lines,color='blue',edgecolor='black')
    plt.yticks(pos, df.index)
    plt.xlabel('Number of lines', fontsize=16)
    plt.ylabel('author', fontsize=16)
    plt.title('Author - number of lines checked in',fontsize=20)
    plt.show()
    
    ## hour the code is checked in
    df = viz.getTimeLineCounts(dfAuthorTime)
    print(viz.getTimeLineCounts(dfAuthorTime))
    ax = df[['no_of_lines']].plot(kind='bar', title ="Code checked in by hour", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Hour", fontsize=12)
    ax.set_ylabel("lines of code", fontsize=12)
    plt.show()
    
    ##Graph the adedit and delete along side each other use seaborn
    ##https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.melt.html
    dfAddDelEdit = pd.melt(Authounts.drop(columns='GrandTot'),id_vars="author", var_name="TypeOfChange", value_name="TotalChangeOfFiles")
    ##https://www.programcreek.com/python/example/96202/seaborn.factorplot
    sns.factorplot(x='TotalChangeOfFiles', y='author', col='TypeOfChange', data=dfAddDelEdit, kind='bar')
    
    
    ## hour the code is checked in and by author
    df = viz.getAuthorTimeLineCounts(dfAuthorTime)
    ax = df[['no_of_lines']].plot(kind='bar', title ="Code checked in by hour and author", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Hour", fontsize=12)
    ax.set_ylabel("lines of code", fontsize=12)
    plt.show()
    
    
  
   

