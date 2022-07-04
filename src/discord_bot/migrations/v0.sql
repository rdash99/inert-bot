-- Schema version: 0
CREATE TABLE IF NOT EXISTS meta (
    version INTEGER PRIMARY KEY
);

-- Initialise the schema version
insert into meta (version) values (0);

-- Used to store information about servers
CREATE TABLE IF NOT EXISTS guilds (
  guild_id BIGINT PRIMARY KEY,
  prefix text, -- Stores the default bot prefix
  botlog BIGINT 
);

-- Stores information about the user. Used referentially
CREATE TABLE IF NOT EXISTS users (
  user_id BIGINT,
  PRIMARY KEY (user_id)
);

-- Links users to guilds and allows user specific guild specific information to be stored
CREATE TABLE IF NOT EXISTS user_guilds (
  user_id BIGINT,
  guild_id BIGINT,
  FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (user_id, guild_id)
);

-- Stores user message count for mee6 exp
CREATE TABLE IF NOT EXISTS messages (
  guild_id BIGINT,
  user_id BIGINT,
  count BIGINT, -- The number of messages sent by a user in a server
  FOREIGN KEY (guild_id, user_id) REFERENCES user_guilds (guild_id, user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (user_id, guild_id)
);

-- Stores roles id per server
CREATE TABLE IF NOT EXISTS roles (
  role_id BIGINT,
  guild_id BIGINT,
  FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (role_id, guild_id)
);

-- Links users to their roles on specific servers
CREATE TABLE IF NOT EXISTS user_role (
  user_id BIGINT,
  role_id BIGINT,
  guild_id BIGINT,
  FOREIGN KEY (role_id, guild_id) REFERENCES roles (role_id, guild_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (user_id, guild_id) REFERENCES user_guilds (user_id, guild_id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id, guild_id)
);

-- Stores deault information about a poll 
CREATE TABLE IF NOT EXISTS polls (
  message_id BIGINT,
  channel_id BIGINT,
  guild_id BIGINT,
  name text,
  time datetime,
  FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (message_id, channel_id, guild_id)
);

-- Stores the different voting option for polls
CREATE TABLE IF NOT EXISTS options (
  message_id BIGINT,
  channel_id BIGINT,
  guild_id BIGINT,
  emote_id BIGINT,
  name text,
  FOREIGN KEY (message_id, channel_id, guild_id) REFERENCES polls (message_id, channel_id, guild_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (emote_id, message_id, channel_id, guild_id)
);

-- Stores the votes on these options
CREATE TABLE IF NOT EXISTS votes (
  user_id BIGINT,
  emote_id BIGINT,
  message_id BIGINT,
  channel_id BIGINT,
  guild_id BIGINT,
  FOREIGN KEY (emote_id, message_id, channel_id, guild_id) REFERENCES options (emote_id, message_id, channel_id, guild_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id, guild_id) REFERENCES user_guilds (user_id, guild_id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (
    user_id,
    emote_id,
    message_id,
    channel_id,
    guild_id
  )
);
