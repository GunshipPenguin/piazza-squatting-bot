# Piazza Squatting Bot

Hate having the average response time of your class's Piazza forum be annoyingly
high?

This Python script uses the [Piazza API](https://github.com/hfaran/piazza-api)
python module to poll a Piazza forum for new posts and automatically notifies a
Slack channel when a new post is made so it can be quickly answered.

Using this script [Xyene](https://github.com/Xyene) and I managed to
bring down the average response time on the Piazza forum for the Winter 2018
offering of CSC209 at the University of Toronto from just under an hour to 4
minutes at one point.

Note that this script was thrown together very quickly (mainly as a joke at first) and as such, it's fairly messy.

## Usage

Ensure that you have the [Piazza API](https://github.com/hfaran/piazza-api)
and [pypandoc](https://pypi.python.org/pypi/pypandoc) modules installed.

Modify the global variables at the top of piazza_squatting_bot.py script to suit your needs. They should be pretty self explanatory.

Run the script with:

```
python piazza_squatting_bot.py
```

And you're good to go!

## License

[MIT](https://github.com/GunshipPenguin/piazza-squatting-bot/blob/master/LICENSE) © Rhys Rustad-Elliott, Tudor Brindus, Jason Pham
