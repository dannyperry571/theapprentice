CREATE TABLE IF NOT EXISTS "version" (
	"db_version" INTEGER DEFAULT 1 UNIQUE,
	PRIMARY KEY(db_version)
);

DROP TABLE "playback_states";

DROP TABLE "search_cache";

DROP TABLE "search_results";

DROP TABLE "tvshow_favorites";

DROP TABLE "movie_favorites";

DROP VIEW "fresh_cache";

DROP VIEW "stale_cache";

CREATE TABLE IF NOT EXISTS "search_results" (
    "cache_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "hash" TEXT,
    "service" TEXT,
    "result" TEXT,
    "ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "scraper_states" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" TEXT UNIQUE,
	"enabled" INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS "scraper_stats" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"service" TEXT,
	"host" TEXT,
	"attempts" FLOAT DEFAULT (0),
	"resolved" FLOAT DEFAULT (0),
	"success" FLOAT DEFAULT (0),
	UNIQUE ("service", "host") ON CONFLICT REPLACE
);

CREATE TABLE IF NOT EXISTS "playback_states" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"hash_id" TEXT,
	"current" TEXT,
	"total" TEXT,
	UNIQUE ("hash_id") ON CONFLICT REPLACE
);

CREATE TABLE IF NOT EXISTS "host_weights" (
	"id" INTEGER PRIMARY KEY NOT NULL,
	"host" TEXT,
	"weight" INTEGER DEFAULT (1000),
	"disabled" INTEGER DEFAULT (0),
	UNIQUE ("host") ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS "my_favorites"(
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"media" TEXT,
	"imdb_id" TEXT,
	"tmdb_id" TEXT,
	"tvdb_id" TEXT,
	"trakt_id" TEXT,
	"slug" TEXT,
	"title" TEXT,
	"cache" TEXT,
	UNIQUE (imdb_id, tmdb_id, media, title)
);

CREATE VIEW IF NOT EXISTS "fresh_cache" AS
	SELECT cache_id, 
	hash, 
	service, 
	result,
	strftime("%s",'now') -  strftime("%s",ts) < (3600 * 4) AS fresh 
	FROM search_results 
	WHERE fresh = 1
;

CREATE VIEW IF NOT EXISTS "stale_cache" AS
	SELECT cache_id, 
	hash, 
	strftime("%s",'now') -  strftime("%s",ts) > (3600 * 4) AS stale 
	FROM search_results 
	WHERE stale = 1
;

CREATE VIEW IF NOT EXISTS "host_ranks" AS
	SELECT host, 
	((1000 - weight) - (10000 * disabled)) as rank, 
	weight 
	FROM host_weights 
	WHERE rank >= 0 
	ORDER BY weight, host ASC
;
