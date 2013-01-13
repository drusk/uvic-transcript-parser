CREATE TABLE Students(
	sid INTEGER PRIMARY KEY AUTOINCREMENT,
	currCumulativeGpa INTEGER,
	englishReq VARCHAR(20),
	-- f=failed, p=was on probation but graduated, s=graduated and never on probation
	-- i=has not failed and has not been on probation (in progress)
	classification CHAR(1)
);

CREATE TABLE Terms(
	tid INTEGER PRIMARY KEY AUTOINCREMENT,
	season TEXT NOT NULL,
	startYear CHAR(4) NOT NULL,
	endYear CHAR(4) NOT NULL,
	UNIQUE(season, startYear, endYear)
);

CREATE TABLE Courses(
	cid INTEGER PRIMARY KEY AUTOINCREMENT,
	dept VARCHAR(4) NOT NULL,
	number VARCHAR(4) NOT NULL,
	credits INTEGER,
	UNIQUE(dept, number)
);

CREATE TABLE TermStatus(
	sid INTEGER REFERENCES Students(sid),
	tid INTEGER REFERENCES Terms(tid),
	standing VARCHAR(40),
	sessionalGPA INTEGER,
	creditsEarned INTEGER,
	program TEXT,
	UNIQUE(sid, tid)
);

CREATE TABLE Registration(
	sid INTEGER REFERENCES Students(sid),
	cid INTEGER REFERENCES Courses(cid),
	tid INTEGER REFERENCES Terms(tid),
	gradePoint INTEGER,
	specialStatus VARCHAR(10)
	-- found students can have same course in same term twice 
	--  if they fail then do supplemental exam
	-- UNIQUE(sid, cid, tid)
);
