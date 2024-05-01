TL;DR Elo algorthims with a bit of common sense, hopefully paving the way for a more transparent ranking system in the future.

So we actually used an Elo type algorithm that uses expected values from the games to come up with rating changes based on the final score vs the expected score. I'm quite happy to share the full script that has come up with this as an exersize of transparency. On how the actual script works, let me go into a bit of detail and background first.

The Elo rating system is a method used to calculate the relative skill levels of teams in competitor-versus-competitor games. Originally devised for chess, it's applicable to any game or sport where matches provide a clear winner and loser, including roller derby. Each team starts with a base rating, this was taken using rankings from Q1 2023 as the current rankings period is 12 months up to March 31st 2024, and this rating adjusts over time based on game outcomes. The initial rating is effective for giving us our best starting point using historical data.

Expected Score Calculation:
Before each game, the system calculates the expected score for each team based on their current ratings. This is determined using a logistic function:
Ea = (1) / (1+10(Rb−Ra)/400)
Here, Ra and Rb are the ratings of Team A and Team B, respectively. The expected score indicates the probability of Team A defeating Team B. A higher rating difference increases the elo loss and gain accordingly.

Game Results:
Actual game results are compared to the expected results. If a team performs as expected (e.g., a higher-rated team wins), the rating adjustment is smaller. However, if an upset happens (e.g., a lower-rated team wins), the adjustment is larger.

Adjustments:
Adjustments are made using the formula:
R′a = Ra + K ×(Sa−Ea)

K is a constant known as the K-factor (set to 64 for our ranking), which determines how much a single game can affect the ratings. Sa is the actual score from the game (1 for a win, 0.5 for a draw, and 0 for a loss).
The difference (Sa−Ea) shows whether the team performed better or worse than expected. Ratings increase if the team performed better than expected and decrease otherwise.

Batch Processing:
In a tournament setting, all games are processed before any rating adjustments are applied. This ensures that results from earlier in the tournament don't unfairly influence games a month or two later.

Practical Example

Suppose 'Race City Rebels' (RCR) and 'Tyne & Fear' (TNF) are competing in a roller derby tournament. If RCR, initially rated higher, wins against TNF as expected, the adjustment to RCR's rating will be small. However, if TNF defeats RCR against the odds, TNF's rating will significantly increase, reflecting their unexpected performance.

As a caveat whilst forefeits count for other reasons, they have not been counted for these calculations. Also as mentioned any games which have happened but after the cut-off have also been discounted. Both are in the source code for anyone who is willing's interest, just commented out.
The source code also prints out how elo has been affected by each result. I'm looking for a good way to share this source with you all but the forum wont just let me throw python at it...

Good news also is if the data set the rankings comittee has for games is incorrect, please let it be known and it can be rerun. 
