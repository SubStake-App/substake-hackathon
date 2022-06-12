## Moonbase Alpha

# Create Table
create table dev_block_collator (blocknum bigint primary key,collator_addr varchar(100), auth_name varchar(100));

##
# DEV Collator List
#
# Create Table
drop table dev_collator_list;
create table dev_collator_list (
    collator_address varchar(100) primary key, 
    display_name varchar(100), 
    count_nominstors int,
    bonded_nominators numeric,
    bonded_owner numeric,
    bonded_total numeric,
    active_status boolean
    );
ALTER TABLE dev_collator_list ADD COLUMN minimun_bond numeric;
ALTER TABLE dev_collator_list ADD COLUMN average_bpr_week numeric;

##
# DEV Nominator_list
#
# Create Table
drop table dev_nominator_list;
create table dev_nominator_list (
    collator_address varchar(100),
    nominator_address varchar(100),
    rank_nominator int,
    bonded numeric,
    Primary Key(collator_address, nominator_address)
);
ALTER TABLE dev_nominator_list ADD COLUMN is_top boolean;