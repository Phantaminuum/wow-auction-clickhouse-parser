CREATE DATABASE IF NOT EXISTS wow;
CREATE TABLE IF NOT EXISTS wow.auctions
(
    `id` UInt64,
    `item_id` UInt32,
    `bid` UInt32,
    `buyout` UInt32,
    `quantity` UInt8,
    `time_left` String,
    `found_at` DateTime,
    `sold_at` DateTime
) ENGINE = MergeTree() 
PARTITION BY toYYYYMM(found_at)
ORDER BY (found_at, item_id) 
SETTINGS index_granularity=8192;