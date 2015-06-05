DROP TABLE Allocate;
DROP TABLE Sponsors;
DROP TABLE Companies;
DROP TABLE Owns;
DROP TABLE Municipalities;
DROP TABLE Stakeholders;
DROP TABLE Skills;
DROP TABLE NeedSkills;
DROP TABLE HaveSkills;
DROP TABLE WorkIn;
DROP TABLE Participate;
DROP TABLE People;
DROP TABLE Project;

-- 1.2

CREATE TABLE Stakeholders (
  CVR CHAR(8) PRIMARY KEY,
  TEL CHAR(8) UNIQUE,
  URL VARCHAR(255) UNIQUE,
  Text VARCHAR(255) NOT NULL
);

CREATE TABLE Companies (
   CVR CHAR(8) PRIMARY KEY REFERENCES Stakeholders(CVR)
);

CREATE TABLE Owns (
  OwnerCVR CHAR(8) REFERENCES Stakeholders(CVR),
  CVR CHAR(8) REFERENCES Stakeholders(CVR),
  PRIMARY KEY (OwnerCVR, CVR)
);

CREATE TABLE Municipalities (
  CVR CHAR(8) PRIMARY KEY REFERENCES Stakeholders(CVR),
  Budget REAL
);

CREATE TABLE People (
  Name VARCHAR(35) PRIMARY KEY,
  Email VARCHAR(255) UNIQUE,
  TEL VARCHAR(8) UNIQUE
);

CREATE TABLE WorkIn (
  CVR CHAR(8) REFERENCES Stakeholders(CVR) NOT NULL,
  PersonName VARCHAR(35) REFERENCES People(Name) NOT NULL
);

CREATE TABLE Project (
  PID INT PRIMARY KEY,
  Budget REAL,
  URL VARCHAR(255) UNIQUE
);

CREATE TABLE Skills (
  Name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE NeedSkills (
  SkillName VARCHAR(50) REFERENCES Skills(Name),
  PID INT REFERENCES Project(PID),
  RequiredPeople INT,
  PRIMARY KEY (SkillName, PID)
);

CREATE TABLE HaveSkills (
  SkillName VARCHAR(50) REFERENCES Skills(Name),
  PID INT REFERENCES Project(PID),
  PRIMARY KEY (SkillName, PID)
);

CREATE TABLE Sponsors (
  PID INT PRIMARY KEY REFERENCES Project(PID),
  CVR CHAR(8) REFERENCES Stakeholders(CVR) NOT NULL
);

CREATE TABLE Participate (
  CVR CHAR(8) REFERENCES Stakeholders(CVR),
  PID INT REFERENCES Project(PID),
  Role VARCHAR(255),
  PRIMARY KEY (CVR, PID)
);

CREATE TABLE Allocate (
  FromDate DATE,
  ToDate DATE,
  Percentage REAL,
  PersonName VARCHAR(35) REFERENCES People(Name),
  PID INT REFERENCES Project(PID),
  PRIMARY KEY (FromDate, ToDate, Percentage, PersonName, PID)
);

-- 1.3

INSERT INTO Stakeholders (CVR, TEXT) VALUES ('21212121', 'Shut up and take my money');
INSERT INTO Companies (CVR) VALUES ('21212121');
INSERT INTO Stakeholders (CVR, TEXT) VALUES ('42424242', 'Yessir');
INSERT INTO Companies (CVR) VALUES ('42424242');
INSERT INTO Owns(OwnerCVR, CVR) VALUES ((SELECT CVR FROM Companies WHERE Companies.CVR = '42424242'),
                                         (SELECT CVR FROM Companies WHERE Companies.CVR = '21212121'));
INSERT INTO Project(PID, URL, Budget) VALUES (42, 'http://42.com', 100000);
INSERT INTO Sponsors(PID, CVR) VALUES ((SELECT PID FROM Project WHERE Project.PID = 42),
                                      (SELECT CVR FROM Companies WHERE Companies.CVR = '21212121'));

INSERT INTO Skills (name) VALUES ('Computer Programming');
INSERT INTO NeedSkills(SkillName, PID, RequiredPeople) VALUES (
  (SELECT name FROM Skills WHERE Skills.name = 'Computer Programming'),
  (SELECT PID FROM Project WHERE Project.PID = 42),
  42
);

-- 1.4

UPDATE Project
SET Budget=420000
WHERE Project.Budget = 100000;

