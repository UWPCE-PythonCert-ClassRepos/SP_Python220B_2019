/* set up sqlite */
.mode column
.header on
-- .width 30 30 30 30 30 30 30 -- uncomment if you want to view untruncated columns

/* Preview data in all tables */
select * from person;

select * from job;

select * from department;

select * from persontojob;

select * from persontodepartment;

/* Example of joining tables */
select pj.person_name_id, p.lives_in_town, p.nickname, pd.department_id, d.department_name, d.manager_id,
       pj.job_id, j.job_name, pj.start_date, pj.end_date, pj.salary, pj.duration_days from persontojob pj
left join person p on p.person_name == pj.person_name_id
left join persontodepartment pd on pj.person_name_id == pd.person_id
left join department d on pd.department_id == d.department_id
left join job j on pj.job_id == j.job_id
;
