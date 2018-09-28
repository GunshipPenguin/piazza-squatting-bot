# Piazza Squatting Bot

Hate having the average response time of your class's Piazza forum be annoyingly
high?

This Python script uses the [Piazza API](https://github.com/hfaran/piazza-api)
Python module to poll a Piazza class for new posts and notify a list of
subscribers in Slack when a post is made so it can be quickly answered.

Using this script [Xyene](https://github.com/Xyene) and I managed to
bring down the average response time on the Piazza forum for the Winter 2018
offering of CSC209 at the University of Toronto from just under an hour to 4
minutes.

## Usage

Ensure that you have the [Piazza API](https://github.com/hfaran/piazza-api),
[Pypandoc](https://pypi.python.org/pypi/pypandoc) and
[PyYAML](https://pyyaml.org/) modules installed.

Modify the provided config.yml to suit your needs.

Run the script with:

```
python piazza_squatting_bot.py
```

And you're good to go!

## License

[MIT](https://github.com/GunshipPenguin/piazza-squatting-bot/blob/master/LICENSE) © Rhys Rustad-Elliott, Tudor Brindus, Jason Pham
