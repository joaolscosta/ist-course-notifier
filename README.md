# IST Courses Announcement Notifier Bot

This project is designed to monitor and notify students of new announcements for various courses at the Instituto Superior Técnico (IST), University of Lisbon. The notifications are delivered via a Discord bot that periodically checks for updates on the courses' announcement feeds.

### Features

The bot is configured to monitor multiple courses offered by IST and checks for new announcements in a set interval (default is every 10 minutes). The bot retrieves the announcements by fetching RSS feeds associated with the courses, ensuring that students are always up to date with important information.

Whenever a new announcement is found, the bot sends a message to a specified Discord channel, notifying the users with the latest update. The bot tracks the latest announcement for each course to avoid sending duplicate notifications.

### License

MIT License.
