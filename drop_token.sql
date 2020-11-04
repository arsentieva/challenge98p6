CREATE TABLE "games" (
  "id" int PRIMARY KEY,
  "playerOneId" int,
  "playerTwoId" int,
  "playerQuit" int,
  "status" varchar,
  "board" varchar,
  "winner" varchar
);

CREATE TABLE "moves" (
  "id" int PRIMARY KEY,
  "playerId" int,
  "gameId" int,
  "column" int,
  "type" varchar,
  "movedOn" timestamp
);

CREATE TABLE "players" (
  "id" int PRIMARY KEY,
  "type" string
);

ALTER TABLE "games" ADD FOREIGN KEY ("playerOneId") REFERENCES "players" ("id");

ALTER TABLE "games" ADD FOREIGN KEY ("playerTwoId") REFERENCES "players" ("id");

ALTER TABLE "moves" ADD FOREIGN KEY ("gameId") REFERENCES "games" ("id");

ALTER TABLE "moves" ADD FOREIGN KEY ("playerId") REFERENCES "players" ("id");
