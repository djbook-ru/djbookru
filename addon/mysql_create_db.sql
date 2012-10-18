create database `djbookru`;
create database `test_djbookru`;
create user `djbookru`@`localhost` identified by 'q1';
grant all on `djbookru`.* to `djbookru`@`localhost`;
grant all on `test_djbookru`.* to `djbookru`@`localhost`;
exit
