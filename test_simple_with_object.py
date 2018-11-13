import unittest
from process_changes_with_object import get_commits, read_file
from changesvisualise import  initialSetup, loadDataFrame, getAuthorInfo, getAuthorLineCount, getAuthorDateLineInfo, getAuthorDateLineCounts, getAuthorSatSunLineCounts, getTimeLineInfo, getTimeLineCounts, getAuthorTimeLineInfo, getAuthorTimeLineCounts, getAuthorAddDelEditInfo, getAuthorAddEditDelCounts

class TestCommits(unittest.TestCase):
    #read in test file
    def setUp(self):
       self.data = read_file('changes_python.log')
          
    def test_number_of_lines(self):
        self.assertEqual(5255, len(self.data))

    def test_number_of_commits(self):
        commits = get_commits(self.data)
        self.assertEqual(422, len(commits))
        self.assertEqual('Thomas', commits[0].author)

        self.assertEqual(['FTRPC-500: Frontier Android || Inconsistencey in My Activity screen',
                'Client used systemAttribute name="Creation-Date" instead of versionCreated as version created.'],
                commits[24].comment)
        self.assertEqual(['M /cloud/personal/client-international/android/branches/android-15.2-solutions/libs/model/src/com/biscay/client/android/model/util/sync/dv/SyncAdapter.java'],
                commits[20].changed_path)
        
class TestVizualResult(unittest.TestCase):
    def setUp(self):
        self.viz = initialSetup()
        
    ##load data frame in the class    
    def test_loadDataFrame(self):
        df = loadDataFrame(self.viz)
        self.assertEqual(422, len(df))  ##positve test
        self.assertNotEqual(423, len(df))  ##neg test
    
    ##Get dataframe with author and  no_of_lines  
    def test_getAuthorInfo(self):
        self.dfAuthor = getAuthorInfo(self.viz)
        self.assertEqual('Vincent' ,self.dfAuthor.loc[2]['author'])  ##positve test
        self.assertNotEqual('Vincent' ,self.dfAuthor.loc[1]['author']) ##neg test
        
    ### groups the dataframe by author and sums no_of_lines
    def test_getAuthorLineCount(self):
        self.dfAuthor = getAuthorInfo(self.viz)
        self.sumAuthors = getAuthorLineCount(self.viz,self.dfAuthor)
        self.assertEqual(234 ,self.sumAuthors.iloc[0]['no_of_lines'])  ##positve test
        self.assertNotEqual(235 ,self.sumAuthors.iloc[0]['no_of_lines']) ##neg test
        
    ##Get dataframe with author, date and  no_of_lines  
    def test_getAuthorDateLine(self):
        self.dfAuthorDate = getAuthorDateLineInfo(self.viz)
        self.assertEqual('Vincent' ,self.dfAuthorDate.loc[2]['author'])  ##positve test
        self.assertNotEqual('Vincent' ,self.dfAuthorDate.loc[1]['author']) ##neg test
        
    ### groups the dataframe by author, date and sums no_of_lines
    def test_getAuthorAddEditDel(self):
        self.dfAuthorAddEditDel = getAuthorAddDelEditInfo(self.viz)
        self.dfAuthorAddEditDelCnt = getAuthorAddEditDelCounts(self.viz,self.dfAuthorAddEditDel)
        self.assertEqual(9 ,self.dfAuthorAddEditDelCnt.iloc[0]['add'])  ##positve test
        self.assertNotEqual(7 ,self.dfAuthorAddEditDelCnt.iloc[0]['add']) ##neg test
        
        
    ### groups the dataframe by author, date and sums no_of_lines
    def test_getAuthorDateLineCounts(self):
        self.dfAuthorDateCnt = getAuthorDateLineInfo(self.viz)
        self.sumAuthors = getAuthorDateLineCounts(self.viz,self.dfAuthorDateCnt)
        self.assertEqual(9 ,self.sumAuthors.iloc[0]['no_of_lines'])  ##positve test
        self.assertNotEqual(10 ,self.sumAuthors.iloc[0]['no_of_lines']) ##neg test
        
    ### groups the dataframe by author, date and sums no_of_lines
    def test_getAuthorSatSunLineCounts(self):
        self.dfAuthorDate = getAuthorDateLineInfo(self.viz)
        self.dfAuthorSatSun = getAuthorSatSunLineCounts(self.viz,self.dfAuthorDate)
        self.assertEqual(1 ,self.dfAuthorSatSun.iloc[0]['no_of_lines'])  ##positve test
        self.assertNotEqual(2 ,self.dfAuthorSatSun.iloc[0]['no_of_lines']) ##neg test
        
    ##Get dataframe with hour and  no_of_lines  
    def test_getTimeLineInfo(self):
        self.dfAuthorTime = getTimeLineInfo(self.viz)
        self.assertEqual(9 ,self.dfAuthorTime.loc[2]['hour'])  ##positve test
        self.assertNotEqual(10 ,self.dfAuthorTime.loc[1]['hour']) ##neg test
     
    ### groups the dataframe by hour and sums no_of_lines    
    def test_getTimeLineCounts(self):
        self.dfAuthorTime = getTimeLineInfo(self.viz)
        self.sumTimeCnt = getTimeLineCounts(self.viz,self.dfAuthorTime)
        self.assertEqual(5 ,self.sumTimeCnt.iloc[0]['no_of_lines'])  ##positve test
        self.assertNotEqual(6 ,self.sumTimeCnt.iloc[0]['no_of_lines']) ##neg test
        
    ##Get dataframe with hour, author,  and  no_of_lines  
    def test_getAuthorTimeLineInfo(self):
        self.dfAuthorTime = getAuthorTimeLineInfo(self.viz)
        self.assertEqual(9 ,self.dfAuthorTime.loc[2]['hour'])  ##positve test
        self.assertNotEqual(10 ,self.dfAuthorTime.loc[1]['hour']) ##neg test
     
   ### groups the dataframe by hour, author and sums no_of_lines 
    def test_getAuthorTimeLineCounts(self):
        self.dfAuthorTime = getAuthorTimeLineInfo(self.viz)
        self.sumTimeCnt = getAuthorTimeLineCounts(self.viz,self.dfAuthorTime)
        self.assertEqual(9 ,self.sumTimeCnt.iloc[0]['no_of_lines'])  ##positve test
        self.assertNotEqual(10 ,self.sumTimeCnt.iloc[0]['no_of_lines']) ##neg test
  
        
if __name__ == '__main__':
    unittest.main()
