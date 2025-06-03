import json

settings = \
    [
        {
            'connected_channels':
                [
                    'sowiiaxi_',
                    'real_anq',
                    'mandellshtam'
                ]
        },
        {
            'channel': 'sowiiaxi_',
            'aigirl': False,
        },
        {
            'channel': 'real_anq',
            'aigirl': False,
        },
        {
            'channel': 'mandellshtam',
            'aigirl': False
        }
    ]

with open('settings.json', 'w') as f:
	json.dump(settings, f, indent=4)