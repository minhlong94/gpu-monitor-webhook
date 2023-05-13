# Python GPU Monitor with Webhook Notification

## Why this script?
If we search on Google with the term "Monitor GPU usage", it will give [gputil](https://github.com/anderskm/gputil) or [gpustat](https://github.com/wookayin/gpustat). However, *it requires SUDO privilege* to be installed properly, which sucks. I want a script that can be run without SUDO privilege, plus can notify me somehow, so here we are.

Tested with Python 3.9. Example usage:
```commandline
python3 monitor.py --webhook_url <your_webhook_url> --seconds <interval_sec_to_notify> --max_usage_by_others_gb <max_gb_to_notify>
```

For example:
```commandline
python3 monitor.py --webhook_url https://discord.com/api/webhooks/1234567890/1234567890 --seconds 60 --max_usage_by_others_gb 1.0
```

It will send a notification to your Discord channel every 60 seconds if the GPU VRAM usage is UNDER 1GB.

Sample message format:
```
GPU free: ['0', '1', '2', '3']
```
## Requirements
- Python 3.9 but should work with other versions

That's all

## License
[MIT](https://choosealicense.com/licenses/mit/)