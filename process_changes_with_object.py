import os.path
class Commit(object):
    #class contructor
    def __init__(self, revision, author, date, time, no_of_lines, changed_path=[], comment=[]):
        self.revision = revision
        self.author = author
        self.date = date
        self.time = time
        self.no_of_lines = no_of_lines
        self.changed_path = changed_path
        self.comment = comment
        self.edit = 0
        self.add = 0
        self.delete = 0
    #added number of adds edits and deletes
    def __repr__(self):
        return self.revision + '\t' + self.author + \
                '\t' + self.date + '\t' + self.time + '\t' + str(self.no_of_lines) + \
				'\t' +str(self.add)+ '\t'+ str(self.edit)+ '\t' + str(self.delete)+ '\t'+ ' '.join(self.comment) + '\n'

def get_commits(data):
    sep = 72*'-'
    commits = []
    index = 0
    while index < len(data):
        try:
            # parse each of the commits and put them into a list of commits
            details = data[index + 1].split('|')
            
            # the author with spaces at end removed.
            commit = Commit(details[0].strip(),
                details[1].strip().replace('/OU=Domain Control Validated/CN=svn.company.net', 'svn.company.net'),
                details[2].strip().split(' ')[0],
                details[2].strip().split(' ')[1],
                int(details[3].strip().split(' ')[0]))
            change_file_end_index = data.index('', index + 1)
            commit.changed_path = data[index + 3 : change_file_end_index]
            commit.comment = data[change_file_end_index + 1 : 
                    change_file_end_index + 1 + commit.no_of_lines]
           # print(commit.changed_path[0])
            #Files added or deleted or edited you can see added and deleted in changed path
            for chpath in commit.changed_path:
                    chpath = chpath.split(' ')
                    if chpath[0] == 'D':
                        commit.delete += 1
                    if chpath[0] == 'A':
                        commit.add += 1
                    if chpath[0] == 'M':
                        commit.edit += 1
                   

            
            # add details to the list of commits.
            commits.append(commit)
            index = data.index(sep, index + 1)
        except IndexError:
            index = len(data)
    return commits

#read in file check if exists
def read_file(any_file):
    exists = os.path.isfile(any_file)
    # use strip to strip out spaces and trim the line.
    if exists:
        return [line.strip() for line in open(any_file, 'r')]
    else:
        return None

def save_commits(commits, any_file):
    my_file = open(any_file, 'w')
    my_file.write("revision\tauthor\tdate\ttime\tno_of_lines\tadd\tedit\tdel\tcomment\n")
    for commit in commits:
        my_file.write(str(commit))
    my_file.close()
    
    
def get_authors(data):
    #sep = '\t'
    authors = {}
    
    ##Did in changesvisualise.py through Panadas - getAuthorInfo
    return authors

if __name__ == '__main__':
    # open the file - and read all of the lines.
    changes_file = 'changes_python.log'
    data = read_file(changes_file)
    if data != None:
        print (len(data))
        commits = get_commits(data)
        print (len(commits))
        print (commits[0])
        #print (commits[0].author)
        save_commits(commits, 'changes.csv')
        authors = get_authors(commits)
        #print(authors)
        
       # self.assertEqual(10, len(authors))
        #self.assertEqual(191, authors['Thomas'])
    
    
    
    
    
    