
use InvestNest;

create table users(
    user_id int auto_increment primary key,     
    username varchar(100) not null unique,
    password varchar(255) not null ,
    cash_balance decimal(15,2) not null default 100000,
    created_at timestamp default current_timestamp 
);
create table stocks (
    stock_id int auto_increment primary key,
    ticker varchar(25) not null unique,         
    company_name varchar(80) not null ,
    current_price decimal(15,2) not null,
    last_updated timestamp default current_timestamp
);

create table transactions(
    txn_id int auto_increment primary key,   
    user_id int not null,
    stock_id int not null,
    txn_type enum('BUY','SELL') not null,  
    quantity int not null,
    price_per_share decimal(15,2) not null,
    txn_date timestamp default current_timestamp,

    foreign key (user_id) references users(user_id),
    foreign key (stock_id) references stocks(stock_id)
);
