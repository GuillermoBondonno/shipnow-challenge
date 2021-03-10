create table department (

dept_id int not null,
dept_name varchar(30) not null,
dept_location varchar(30) not null,
unique(dept_id)

);

create table employee (

emp_id integer not null,
emp_name varchar(50) not null,
dept_id int not null,
salary int not null,
unique(emp_id)

);

insert into department values (1, 'Contable', 'BA');
insert into department values (2, 'RRHH', 'NYC');
insert into department values (3, 'Produccion', 'BA');
insert into department values (4, 'Logistica', 'BA');
insert into department values (5, 'Administracion', 'Boston');

insert into employee values (1, 'Juan', 5, 12000);
insert into employee values (2, 'Maria', 2, 15000);
insert into employee values (3, 'Alice', 1, 12000);
insert into employee values (4, 'Bob', 1, 11000);
insert into employee values (5, 'Pedro', 3, 12100);
insert into employee values (6, 'Guillermo', 4, 13000);
insert into employee values (7, 'Domingo', 3, 10000);

select
a.dept_id,
count(b.dept_id) as cantidad,
sum(b.salary) as sum_of_salary
from employee b join department a on b.dept_id=a.dept_id
group by a.dept_id
having count(b.dept_id) > 0