# UpsetGG
## About
Python program that returns overall difference between seeds and final standings for each player on a specific smash.gg tournament.

Any 1v1 game should be supported (Smash Ultimate, Smash Melee, Rivals of Aether, Brawlhalla, etc) but it won't work for 2v2 and other team tournaments.

The difference is calculated based on the position the player was supposed to reach with his seed and his final standings. In a regular Top 32 DE bracket, seed 8 is supposed to end up 7th but if he actually ends up 4th, that's a +2 performance. Seed 31 is supposed to be 25th but if he ends up 13th, that's also a  +2 performance. And so on...

## How to use
You will need to add your own smash.gg API key in the code (look at the first few lines and add it to the relevant variable).

Overall, it's a very simple program that should be pretty self-explanatory once launched.

## Contact
Feel free to contact me on Twitter [@Pikanatox](https://twitter.com/Pikanatox) if you ever run into issues.
