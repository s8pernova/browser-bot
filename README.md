# Browser Bot

Quick, free, self-hosted browser workflow.

It uses YAML files to describe browser actions, then runs them with Python and Playwright. 

## Purpose

It's meant for simple scheduled website tasks, like logging into a site, clicking buttons, filling forms, waiting for pages, and saving screenshots.

For example, I'm using this to vote for a friend where the voting period refreshes daily.

## Scheduling with systemd

### Installation

To set up a daily scheduled task for a specific workflow, use the `install-systemd.sh` script. It takes two arguments:

```bash
./ops/install-systemd.sh <service-prefix-name> <workflow-file.yaml>
```

**Example:**
```bash
./ops/install-systemd.sh brianna-voting-browser-bot workflows/vote-for-brianna.yaml
```

By default, the template triggers every day at 8:00 AM local time.

### Checking Status & Logs

Manage your scheduled workflows without `sudo` by using the `--user` flag:

```bash
# Check if the timer is active and when it runs next
systemctl --user status brianna-voting-browser-bot.timer

# View the live execution logs of the bot
journalctl --user -u brianna-voting-browser-bot.service -f
```

### Uninstallation

To completely remove the timer and the systemd files for a specific workflow, use the `uninstall-systemd.sh` script with your service name:

```bash
./ops/uninstall-systemd.sh <service-prefix-name>
```

**Example:**
```bash
./ops/uninstall-systemd.sh brianna-voting-browser-bot
```