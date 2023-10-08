create table reward
(
    id                int         not null
        primary key,
    name              varchar(40) null comment 'Name of the reward',
    min_amount        int         null,
    max_amount        int         null,
    difficult_level   varchar(40) null comment 'This is the difficult level of the game. It consits of easy, normal and hard',
    passing_condition int         null comment 'This is the number of weapon needed to pass the level'
);

INSERT INTO zombiator.reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (1, 'money', 300, 500, 'easy', 50);
INSERT INTO zombiator.reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (2, 'money', 500, 700, 'normal', 150);
INSERT INTO zombiator.reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (3, 'money', 700, 2000, 'hard', 300);
INSERT INTO zombiator.reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (4, 'weapon', 50, 200, 'easy', 50);
INSERT INTO zombiator.reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (5, 'weapon', 200, 700, 'normal', 150);
INSERT INTO zombiator.reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (6, 'weapon', 700, 2500, 'hard', 300);
