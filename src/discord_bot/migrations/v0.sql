PRAGMA foreign_keys = ON;
-- Schema V0

-- Guilds
CREATE TABLE IF NOT EXISTS "guilds" (
	"guild_id"	INTEGER,
	"prefix"	TEXT,
	"botlog"	INTEGER,
	PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS users (
  user_id integer,
  guild_id integer,  FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (user_id, guild_id)
);

CREATE TABLE IF NOT EXISTS roles (
  role_id integer,
  guild_id integer,
  FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (role_id, guild_id)
);

CREATE TABLE IF NOT EXISTS user_role (
  user_id integer,
  role_id integer,
  guild_id integer,
  FOREIGN KEY (role_id, guild_id) REFERENCES roles (role_id, guild_id) 
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (user_id, guild_id) REFERENCES users (user_id, guild_id) 
    ON UPDATE CASCADE ON DELETE CASCADE,
PRIMARY KEY (user_id, role_id, guild_id)
);

CREATE TABLE IF NOT EXISTS polls (
  message_id integer,
  channel_id integer,
  guild_id integer,
  name text,
  time datetime,
  FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (message_id, channel_id, guild_id)
);

CREATE TABLE IF NOT EXISTS options (
  emote_id integer,
  message_id integer,
  channel_id integer,
  guild_id integer,
  FOREIGN KEY (message_id, channel_id, guild_id)
    REFERENCES polls (message_id, channel_id, guild_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (emote_id, message_id, channel_id, guild_id)
);

CREATE TABLE IF NOT EXISTS votes (
  user_id integer,
  emote_id integer,
  message_id integer,
  channel_id integer,
  guild_id integer,
  FOREIGN KEY (emote_id, message_id, channel_id, guild_id)
    REFERENCES options (emote_id, message_id, channel_id, guild_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (user_id, emote_id, message_id, channel_id, guild_id)
);
