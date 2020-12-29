CREATE TABLE IF NOT EXISTS sport_event
(
    timestamp varchar(16),
    sport varchar(32),
    match_title text,
    data_event text 
);
CREATE TABLE IF NOT EXISTS execution
(
    timestamp varchar(16),
    symbol varchar(255),
    market varchar(64),
    price varchar(32),
    quantity varchar(32),
    executionEpoch varchar(16),
    stateSymbol varchar(2)
);

