PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

DELETE FROM drivers;

DELETE FROM results;

COMMIT;

PRAGMA foreign_keys=on;