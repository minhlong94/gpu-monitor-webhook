# Simple Python script to monitor GPU usage and send notification via Webhook
Tested with Python 3.9. Example usage:
```commandline
python3 monitor.py <your_webhook_url> <interval_sec_to_notify>
```

For example:
```commandline
python3 monitor.py https://discord.com/api/webhooks/1234567890/1234567890 60
```

It will send a notification to your Discord channel every 60 seconds if the GPU VRAM usage is under 1GB.

Sample message
```
GPU free: ['0', '1', '2', '3']
```
## Requirements
- Python 3.9 but should work with other versions

That's all

## License
[MIT](https://choosealicense.com/licenses/mit/)