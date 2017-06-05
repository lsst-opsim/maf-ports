from __future__ import print_function
import os
import sys
import sqlite3
import lsst.sims.maf.db as db


#trackingDb = 'trackingDb_all.py'
trackingDb = sys.argv[1]
print('Updating tracking database %s' % (trackingDb))
newDb = 'new_' + trackingDb
# Give one way to assign some opsimGroups
autogroup = {'Tier1 2016': ['minion_1016', 'minion_1012', 'minion_1013', 'kraken_1043',
                            'enigma_1281', 'enigma_1282', 'kraken_1045', 'kraken_1059',
                            'kraken_1052', 'kraken_1053', 'minion_1020', 'minion_1018',
                            'minion_1022', 'minion_1017']}

# Connect to and pull out the data from the old database.
conn = sqlite3.connect(trackingDb)
cursor = conn.cursor()
query = 'select * from runs order by mafRunId'
cursor.execute(query)
runlist = cursor.fetchall()
c = cursor.description
oldcolumns = []
for ci in c:
    oldcolumns.append(ci[0])

new = db.TrackingDb(newDb)
for r in runlist:
    # Just to make this next bit easier to read, translate 'r' into a dictionary.
    run = {}
    for i, col in enumerate(oldcolumns):
        run[col] = r[i]
    # Assign values for new tracking database, if available in old database.
    mafRunId = run['mafRunId']
    mafDir = run['mafDir']
    opsimRun = run['opsimRun']
    opsimComment = run['opsimComment']
    mafComment = run['mafComment']
    if 'opsimGroup' in run:
        opsimGroup = run['opsimGroup']
    else:
        opsimGroup = None
    if 'opsimVersion' in run:
        opsimVersion = run['opsimVersion']
    else:
        opsimVersion = None
    if 'opsimDate' in run:
        opsimDate = run['opsimDate']
    else:
        opsimDate = None
    if 'mafVersion' in run:
        mafVersion = run['mafVersion']
    else:
        mafVersion = None
    if 'mafDate' in run:
        mafDate = run['mafDate']
    else:
        mafDate = None
    if 'dbFile' in run:
        dbFile = run['dbFile']
    else:
        dbFile = None

    # See if we can assign an auto-group.
    if opsimGroup is None:
        for key in autogroup:
            if opsimRun in autogroup[key]:
                opsimGroup = key
    # Or just use the first part of the run name (i.e. hostname).
    if opsimGroup is None:
        opsimGroup = opsimRun.split('_')[0]

    # Look to see if we can find more/new information on disk.
    if os.path.isdir(mafDir):
        print('Looking for new/extra information on disk')
        autoOpsimRun = None
        autoOpsimComment = None
        autoOpsimVersion = None
        autoOpsimDate = None
        autoMafVersion = None
        autoMafDate = None
        if os.path.isfile(os.path.join(mafDir, 'configSummary.txt')):
            file = open(os.path.join(mafDir, 'configSummary.txt'))
            for line in file:
                tmp = line.split()
                if tmp[0].startswith('RunName'):
                    autoOpsimRun = ' '.join(tmp[1:])
                if tmp[0].startswith('RunComment'):
                    autoOpsimComment = ' '.join(tmp[1:])
                # MAF Date may be in a line with "MafDate" (new configs)
                #  or at the end of "MAFVersion" (old configs).
                if tmp[0].startswith('MAFDate'):
                    autoMafDate = tmp[-1]
                if tmp[0].startswith('MAFVersion'):
                    autoMafVersion = tmp[1]
                    if len(tmp) > 2:
                        autoMafDate = tmp[-1]
                if tmp[0].startswith('OpsimDate'):
                    autoOpsimDate = tmp[-2]
                if tmp[0].startswith('OpsimVersion'):
                    autoOpsimVersion = tmp[1]
                    if len(tmp) > 2:
                        autoOpsimDate = tmp[-2]
            file.close()
        if (opsimRun is None) or (opsimRun == 'NULL'):
            opsimRun = autoOpsimRun
        if (opsimComment is None) or (opsimComment == 'NULL'):
            opsimComment = autoOpsimComment
        if (opsimDate is None) or (opsimDate == 'NULL'):
            opsimDate = autoOpsimDate
        if (opsimVersion is None) or (opsimVersion == 'NULL'):
            opsimVersion = autoOpsimVersion
        if (mafDate is None) or (mafDate == 'NULL'):
            mafDate = autoMafDate
        if (mafVersion is None) or (mafVersion == 'NULL'):
            mafVersion = autoMafVersion
    else:
        print('Cannot find %s directory on disk, will only reuse old information.' % (mafDir))
    # Convert date formats to 'year-month-day' if they are not already.
    if mafDate is not None:
        if len(mafDate.split('/')) > 1:
            t = mafDate.split('/')
            if len(t[2]) == 2:
                t[2] = '20' + t[2]
            mafDate = '-'.join([t[2], t[1], t[0]])
    if opsimDate is not None:
        if len(opsimDate.split('/')) > 1:
            t = opsimDate.split('/')
            if len(t[2]) == 2:
                t[2] = '20' + t[2]
            opsimDate = '-'.join([t[2], t[1], t[0]])

    runId = new.addRun(opsimGroup=opsimGroup, opsimRun=opsimRun, opsimComment=opsimComment,
                       opsimVersion=opsimVersion, opsimDate=opsimDate,
                       mafComment=mafComment, mafVersion=mafVersion, mafDate=mafDate,
                       mafDir=mafDir, dbFile=dbFile, mafRunId=mafRunId)
    print('Added run info with mafRunId %d (previously %d)' % (runId, mafRunId))

new.close()
