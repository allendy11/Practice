create table users (
  `id` int primary key auto_increment,
  `name` varchar(255),
  `email` varchar(255),
  `password` varchar(255),
  `created_at` datetime default current_timestamp
)