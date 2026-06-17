# Farmer Game

Description:
My project is Farmer Game, a mostly UI clicker and simulation game. The user can level up by doing things such as planting crops, selling crops, and buying seeds. When you first boot up the game, one of only buttons you can click is the "Plant Potato" button. When you plant potatoes you get level points; level points are not shown to the user, but they are used as a universal points system that lets the user level up. At level 2 the user unlocks planting corn, and level 3 unlocks wheat.

There is a "Sell Crops" button which picks a random crop you have, removes one from storage, and gives money depending on crop type: $3 for potatoes, $5 for corn, and $7 for wheat. If a crop is unavailable, the game picks another until there are no crops left, then the button is disabled.

Next to "Sell Crops" is "Buy Seeds", which buys 5 seeds for $10. Planting a crop uses 2 seeds. The user starts with a balance of $20 and 20 seeds. In the top right corner there are four buttons: Upgrade Storage, Hire Farmers, Upgrade Tools, and Hire Marketers.

Upgrade Storage increases max crops, Hire Farmers plants one crop per second, Upgrade Tools increases plants per click, and Hire Marketers automatically sells one crop every second and buys two seeds for $3 every two seconds. You can only upgrade storage once per level. Upgrade Storage is available from level one. Upgrading Tools unlocks at level three, Farmers at four, and Marketers at five.

## Run locally

```bash
python project.py
```

## Build and publish

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine upload dist/*
```
