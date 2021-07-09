--Hien Duong 11587750
--Cpts 451
--HW 4

-- Problem 1
SELECT distinct firstname, lastname, title
FROM UserTable, Instructor, Class
WHERE userID=Instructor.instructorID AND Instructor.instructorID=Class.instructorID AND major='CptS' AND semester='Spring' AND year='2020'
ORDER BY firstname;

-- Problem 2
SELECT classid, major, coursenum, numstudents
FROM (SELECT Enroll.classid, class.major, class.coursenum, Count(Enroll.classid) as numstudents
FROM Class, Enroll
where Enroll.classid=Class.classid
GROUP BY class.coursenum, class.major, Enroll.classid) AS Temp
WHERE Temp.numstudents > 10
ORDER BY major, coursenum;

-- Problem 3
SELECT course.major, course.coursenum, course.title
FROM course left OUTER JOIN prerequisite
ON course.major = prerequisite.major AND course.coursenum = prerequisite.coursenum
WHERE prerequisite.coursenum is null
ORDER BY course.major, course.coursenum;

-- Problem 4
SELECT userid, timestamp, count
FROM (SELECT UserTable.userID, Post.timestamp, Count(UserTable.userID) as count
FROM UserTable, Student, Post
WHERE UserTable.userID = Student.studentID AND Post.userID = Student.studentID
GROUP BY UserTable.userid, Post.timestamp) TEMP
WHERE count > 1;

-- Problem 5 A
SELECT classid, major, coursenum, semester, year, enrollmentlimit
FROM(
SELECT MAX(enrollmentlimit)
FROM Class) Temp, Class
where Temp.max = Class.enrollmentlimit;

-- Probelm 5 B
SELECT Class.classid, Class.major, coursenum, semester, year, enrollmentlimit
FROM (SELECT major, MAX(enrollmentlimit)
FROM Class
GROUP BY major) Temp, Class
WHERE Temp.major=Class.major and Temp.max = Class.enrollmentlimit
ORDER BY major, coursenum;

-- Problem 6
SELECT Temp3.firstname, Temp3.lastname, Temp3.StudentID, csgpa, gpa
FROM (SELECT StudentID, firstname, lastname, ROUND(Cast(Cast(Sum(grade) as float)/Cast(count(grade) as float) as numeric),2) as GPA
FROM (SELECT Temp.StudentId, firstname, lastname, major, classid, grade
FROM (SELECT Student.StudentID, firstname, lastname, major
FROM UserTable, Student
WHERE UserTable.UserID=Student.StudentId) Temp, Enroll
WHERE Temp.StudentID = Enroll.StudentID) Temp2
GROUP BY StudentID, firstname, lastname) Temp3, (SELECT StudentID, firstname, lastname, ROUND(Cast(Cast(Sum(grade) as float)/Cast(count(grade) as float) as numeric),2) as csgpa
FROM (SELECT Temp.StudentId, firstname, lastname, major, classid, grade
FROM (SELECT Student.StudentID, firstname, lastname, major
FROM UserTable, Student
WHERE UserTable.UserID=Student.StudentId) Temp, Enroll
WHERE Temp.StudentID = Enroll.StudentID AND classid LIKE '%CptS%') Temp2
GROUP BY StudentID, firstname, lastname) Temp4
WHERE Temp4.csgpa > Temp3.gpa AND Temp4.StudentID = Temp3.StudentID
ORDER BY Temp3.lastname;

-- Problem 7
SELECT Temp1.firstname, Temp2.firstname, temp1.classid, temp1.assignmentno, temp1.submissiondate, temp1.score
FROM (SELECT userid, firstname, classid, assignmentno,  submissiondate, score
FROM (SELECT firstname, userid
FROM UserTable, Student
Where UserTable.UserID=Student.StudentID) Temp, Submit
Where Temp.userid = Submit.studentid
) Temp1, (SELECT userid, firstname, classid, assignmentno,  submissiondate, score
FROM (SELECT firstname, userid
FROM UserTable, Student
Where UserTable.UserID=Student.StudentID) Temp, Submit
Where Temp.userid = Submit.studentid
)Temp2
WHERE Temp1.userid < Temp2.userid AND Temp1.submissiondate = Temp2.submissiondate AND Temp1.score=Temp2.score
ORDER BY Temp1.firstname, temp2.firstname;

-- Problem 8
SELECT major, coursenum, enrollmentlimit, numstudents
FROM (SELECT classid, Count(studentid) as numstudents
FROM Enroll
GROUP BY classid) Temp1, Class
WHERE Temp1.classid=Class.classid AND Temp1.numstudents > Class.enrollmentlimit;

-- Problem 9
SELECT t.studentid, t.classid, t.assignmentno, content
FROM (SELECT *
FROM Post, PostAbout, Student
WHERE Post.userid=Student.studentid AND Post.postid=PostAbout.postid) t LEFT OUTER JOIN submit
ON submit.studentid=t.userid and t.assignmentno=submit.assignmentno and t.classid=submit.classid
WHERE Submit.studentid is null
ORDER BY t.classid, t.assignmentno;

-- Problem 10
SELECT classid, maxavggrade
FROM (SELECT MAX(avggrade) as maxavggrade
FROM (SELECT classid, CAST(SUM(grade) as numeric) / CAST(Count(grade) as numeric) as avgGrade
FROM ENROLL
GROUP BY classid) t) Temp, (SELECT classid, CAST(SUM(grade) as numeric) / CAST(Count(grade) as numeric) as avgGrade
FROM ENROLL
GROUP BY classid) Temp2
WHERE Temp.maxavggrade=Temp2.avgGrade;