
-- RENAMING RELATIONS

--employees who make more money than their manager
SELECT  E1.ename, D.dname,E1.sal, D.mgr, E2.sal as manager_sal
FROM     Emp as E1, Dept as D, Emp as E2
WHERE    E1.dno = D.dno AND
	     D.mgr = E2.ename AND  E1.sal > E2.sal;
			 
-- Employees who earn the same sal,  
SELECT  E1.ssn, E1.ename, E1.sal, E2.ssn, E2.ename, E2.sal
FROM      Emp as E1, Emp as E2
WHERE    E1.sal = E2.sal AND E1.ssn<>E2.ssn;
--we get each pair twice 

SELECT  E1.ssn, E1.ename, E1.sal, E2.ssn, E2.ename, E2.sal
FROM      Emp as E1, Emp as E2
WHERE    E1.sal = E2.sal AND E1.ssn < E2.ssn;
--we get each pair once 

--the employees who work on the same project as their manager        
SELECT   E1.ename, D.dname, E2.ename, PE1.proj_id, PE2.proj_id,P.ptitle
FROM     Emp as E1, Dept D, Emp as E2, ProjectEmp as PE1, ProjectEmp as PE2, Proj as P
WHERE    E1.dno = D.dno AND PE1.ssn = E1.ssn AND PE2.ssn = E2.ssn 
         AND P.proj_id = PE1.proj_id
	     AND D.mgr = E2.ename AND E1.ename <> E2.ename  
         AND PE1.proj_id = PE2.proj_id;

---------------------------------------------------------
-- conditions on dates and strings
SELECT  *
FROM 	Emp, Dept, ProjectEmp, Proj
WHERE   Emp.dno = Dept.dno AND Emp.ssn = ProjectEmp.ssn AND ProjectEmp.proj_id = Proj.proj_id AND
		 ename >'J' AND sal < 70000 
         AND Proj.startdate> '1/1/2017' AND ptitle LIKE '%Software' AND ename <>'Mary';;

-- querying for NULL values
SELECT ename, sal
FROM    Emp
WHERE  sal<=50K     OR sal>50K; 

SELECT ename, sal
FROM    Emp
WHERE  sal<=50000 OR sal>50000 OR sal is NULL; 

-- ordering 
SELECT *
FROM    Emp
WHERE  sal<=50000
ORDER BY dno, sal desc, ename;

SELECT *
FROM    Emp
WHERE  sal<=50000 OR sal IS NULL
ORDER BY dno NULLS FIRST, sal desc, ename;

--set operations
(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname = 'Purchasing')
UNION
(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname ='HR')
 -- eliminates duplicates in the results
 
SELECT  ename  
FROM Emp, Dept 
WHERE Emp.dno=Dept.dno  AND (dname = 'Purchasing' OR dname='HR');
--have duplicates

(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname = 'Purchasing')
INTERSECT
(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname ='HR')
 
SELECT  ename,dname  
FROM Emp, Dept 
WHERE Emp.dno=Dept.dno  AND (dname = 'Purchasing' AND dname='HR');
-- no results


--NOT all systems support intersect operator. Alternative query for intersect.
SELECT  E1.ssn,E1.ename 
FROM Emp E1, emp E2
WHERE E1.ssn = E2.ssn AND E1.dno = 111 AND E2.dno=888;


(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname = 'Purchasing')
EXCEPT
(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname ='HR')

SELECT  E1.ssn,E1.ename 
FROM Emp E1, emp E2
WHERE E1.ssn = E2.ssn AND E1.dno = 111 AND E2.dno<>888;

---------------------------------------

--AGGREGATION

------------
-- When there is grouping aggregate functions applied to attribute value in each group. 
SELECT Dept.dno,SUM(sal), COUNT(ename)
FROM   Emp, Dept
WHERE  Emp.dno = Dept.dno 
GROUP BY Dept.dno;

SELECT Dept.dno,ename, SUM(sal), COUNT(ename)
FROM   Emp, Dept
WHERE  Emp.dno = Dept.dno 
GROUP BY Dept.dno,ename;

--------

SELECT dname, SUM(sal), COUNT(ssn)
FROM   Emp, Dept
WHERE  Emp.dno = Dept.dno 
GROUP BY dname
HAVING COUNT(ssn)>2;

--------------------------
-- Projects with employees from at least 6 different departments.   
SELECT proj_id, COUNT(distinct dno) as countDept
FROM  ProjectEmp, Emp		
WHERE  ProjectEmp.ssn = Emp.ssn 
GROUP BY proj_id
HAVING COUNT(distinct dno) >= 6
ORDER BY countDept
  
---------
-- Employees working in departments with at least 2 employees
SELECT Emp.ssn, Emp.ename, count(*) 		
FROM  Emp, Dept 			
WHERE  Emp.dno = Dept.dno  
GROUP BY Emp.ssn,Emp.ename      			       
HAVING count(distinct Dept.dno) > 1      		       
ORDER BY Emp.ssn,Emp.ename; 

---------
--SUBQUERIES
-----------
-- Employees who work in the same department as Jack. 
SELECT E1.ssn, E1.ename
FROM Emp as E1, Emp as E2
WHERE E2.ename = 'Jack' AND E1.dno = E2.dno

SELECT ssn,ename
FROM Emp
WHERE dno IN
	(SELECT dno
	FROM Emp
	WHERE ename = 'Jack')

---------
--List departments which has employees with salaries more than 60K
SELECT dno,dname
FROM  Dept
WHERE dno IN
	( SELECT dno                              	
	  FROM Emp			
	  WHERE sal>60000); 
      
SELECT dno,dname
FROM   Emp E1, Dept D
WHERE  E1.dno=D.dno AND sal>60000;

---------
--List the department names which has more than 2 employees
    SELECT Emp.dno
    FROM Emp, Dept
    WHERE Emp.dno=Dept.dno
    GROUP BY Emp.dno
    HAVING COUNT(ssn)>2;

SELECT dname, dno 
FROM Dept 
WHERE dno IN
  (SELECT Dept.dno
    FROM Emp, Dept
    WHERE Emp.dno=Dept.dno
    GROUP BY Dept.dno
    HAVING COUNT(ssn)>2)

------
-- Employees who work in Purchasing department but not in HR department.
(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname = 'Purchasing')
EXCEPT
(SELECT  ename FROM Emp, Dept 
 WHERE Emp.dno=Dept.dno  AND dname ='HR')

SELECT  E.ename 
FROM emp E
WHERE E.ssn IN 
	(SELECT ssn FROM Emp,Dept where Emp.dno=Dept.dno AND dname='Purchasing') 
AND E.ssn NOT IN 
    (SELECT ssn FROM Emp,Dept where Emp.dno=Dept.dno AND dname='HR');


--Find employee(s) with the highest salary

SELECT  distinct ename, sal 
FROM    emp
WHERE sal >= ALL 
	(SELECT MAX(sal) 
	 FROM  Emp);

SELECT distinct ename,ssn
FROM Emp 
WHERE sal >= ALL
	(SELECT sal
	 FROM Emp
	 WHERE sal IS NOT NULL)

--------
--Who makes more than someone in the Hardware department?

SELECT ename,sal
FROM Emp
WHERE sal >= ANY
		(SELECT sal
		FROM Emp,  Dept
		WHERE Emp.dno = Dept.dno AND  Dept.dname = 'Hardware' sal IS NOT NULL);

SELECT ename,sal
FROM Emp
WHERE sal >= ALL
		(SELECT sal 
		FROM Emp,  Dept
		WHERE Emp.dno = Dept.dno AND  Dept.dname = 'Hardware' AND sal IS NOT NULL);
		
--------
--Who works in the 'Production' department?
SELECT   ename,dno
FROM     Emp
WHERE  Emp.dno =
		(SELECT dno
		 FROM  Dept
		 WHERE dname='Production');
    

--SUBQUERIES in FROM
SELECT dno, SUM(sal) as totalSal, COUNT(ename) as numEmp
FROM   Emp
GROUP BY dno
HAVING COUNT(ssn)>1;

SELECT Temp.dno, Temp.totalSal, Temp.numEmp
FROM   (
	SELECT dno, SUM(sal) as totalSal , COUNT(ename) as numEmp
	FROM   Emp
	GROUP BY dno
 ) AS Temp
WHERE Temp.numEmp > 1;

 -----
--Find the employees in the departments whose total salary amount is more than $200K
--- find the total salary in each department
--- return those whose total salary is > 200K
SELECT Emp.ename
FROM   Emp
WHERE Emp.dno IN (
	SELECT dno
	FROM   Emp
	GROUP BY dno
	HAVING SUM(sal) >200000);

SELECT Emp.ename
FROM   (
	SELECT dno, SUM(sal) as totalSal 
	FROM   Emp
	GROUP BY dno
 ) AS Temp, Emp
WHERE Temp.dno=Emp.dno  AND Temp.totalSal>200000;

-----------------------------------
--- Addtional Subquery Examples  (SLide # 14) 
-----------------------------------
--Employees who work on some project
SELECT distinct Emp.ssn, ename 
FROM projectEmp, Emp
WHERE ProjectEmp.ssn=Emp.ssn;

SELECT distinct ssn, ename 
FROM Emp
WHERE ssn IN (SELECT ssn FROM projectEmp);

SELECT distinct ssn, ename 
FROM Emp as E
WHERE EXISTS (SELECT * FROM projectEmp as PE
               WHERE E.ssn = PE.ssn);

------------------------------------------

--Employees who doesn't work on any projects
SELECT distinct ssn, ename 
FROM Emp
WHERE ssn NOT IN (SELECT ssn FROM projectEmp);

SELECT ssn, ename 
FROM Emp as E
WHERE NOT EXISTS (SELECT * FROM projectEmp as PE
                   WHERE E.ssn = PE.ssn);
				   
-----------
--Find the employee with highest salary 
SELECT  distinct ename, sal 
FROM emp
WHERE sal >= ALL 
	(SELECT MAX(sal) 
	 FROM  Emp);

 
SELECT distinct ename, sal 
FROM Emp as E1
WHERE NOT EXISTS (SELECT * FROM Emp as E2
                   WHERE E1.sal < E2.sal) AND 
                   E1.sal IS NOT NULL;


-- “Find the employees whose salary is greater than overall average salary”.
select *
from Emp E
where sal > 
		(SELECT AVG(sal) 
		 FROM Emp E2);

-- “Find the employees whose avg salary is greater than the average salary in the department they work in”.
select *
from Emp E1
where sal > 
		(SELECT AVG(sal) 
		 FROM Emp E2
         WHERE E1.dno = E2.dno);
   

 ---Find the employees that work on all projects
SELECT * 
FROM Emp as E
WHERE NOT EXISTS (
   SELECT *
   FROM Proj
	WHERE proj_id NOT IN 
     	(SELECT proj_id 
	 	 FROM ProjectEmp
		 WHERE ssn = E.ssn)
)

------
--Find the department names that has the max total salary amount among all departments
-- 1. find the total sal in each dept
-- 2. find the max among the total sal.


SELECT *
FROM (SELECT dno, SUM(sal) as totalSal 
      FROM   Emp
      GROUP BY dno ) as Temp2, Dept as D
      WHERE Temp2.dno = D.dno AND
            totalSal = 
        	(SELECT max(Temp1.totalSal)
	         FROM (SELECT dno, SUM(sal) as totalSal 
	 	           FROM   Emp
		           GROUP BY dno) as Temp1)      

-------------------------------------------------------------------
-- More Subquery Examples
-------------------------------------------------------------------

--Suppliers(sid, sname, address)  
--Parts(pid, pname, color)  
--Catalog(sid, pid, cost)

--Query 1: Find the distinct  sids of suppliers who charge more for some part 
--than the average cost of that part 
--(averaged over all the suppliers who supply that part).

SELECT distinct sid
FROM Catalog as C1
WHERE cost > 
	(SELECT avg(cost)
     FROM Catalog as C2
	 WHERE C1.pid=C2.pid
     GROUP BY pid)
	 
	 
--Suppliers(sid, sname, address)  
--Parts(pid, pname, color)  
--Catalog(sid, pid, cost)

--Query 2: Find the distinct sids of suppliers who supply only red parts.

SELECT distinct C.sid
FROM Catalog C1, Parts P1
WHERE C1.pid = P1.pid AND
	  P1.color='Red' AND
      NOT EXISTS (SELECT * FROM Catalog C2, Parts P2
                   WHERE C2.pid=P2.pid AND
                 	     P2.color<>'Red' AND
                         C1.sid=C2.sid);
                         
SELECT distinct sid
FROM Catalog 
WHERE sid IN 
	(SELECT sid 
     FROM Catalog C1, Parts P1
     WHERE C1.pid=P1.pid AND
           P1.color='Red') 
    AND sid NOT IN 
	(SELECT sid 
     FROM Catalog C2, Parts P2
     WHERE C2.pid=P2.pid AND
           P2.color<>'Red'); 
    


	
	(SELECT sid 
     FROM Catalog C1, Parts P1
     WHERE C1.pid=P1.pid AND
           P1.color='Red') 
    EXCEPT
	(SELECT sid 
     FROM Catalog C2, Parts P2
     WHERE C2.pid=P2.pid AND
           P2.color<>'Red'); 