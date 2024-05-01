import math

class RollerDerbyElo:

    def __init__(self, initial_ratings=None):
        self.ratings = initial_ratings if initial_ratings else {}

    def add_team(self, team_name, initial_rating=1000):
        if team_name not in self.ratings:
            self.ratings[team_name] = initial_rating

    def set_rating(self, team_name, rating):
        self.ratings[team_name] = rating

    def expected_score(self, ra, rb):
        return 1 / (1 + 10 ** ((rb - ra) / 200))

    def update_ratings(self, games):

        print(f"Gameday --------------------------------------------------------------------------")

        # Store initial rankings
        initial_rankings = sorted(self.ratings.items(), key=lambda item: item[1], reverse=True)
        initial_positions = {team: idx + 1 for idx, (team, _) in enumerate(initial_rankings)}

        adjustments = {team: 0 for team in self.ratings}

        for game in games:
            team_a, score_a, team_b, score_b = game
            self.add_team(team_a)
            self.add_team(team_b)

            if team_a not in adjustments:
                adjustments[team_a] = 0
            if team_b not in adjustments:
                adjustments[team_b] = 0

            ra = self.ratings[team_a]
            rb = self.ratings[team_b]

            ea = self.expected_score(ra, rb)
            eb = self.expected_score(rb, ra)

            score_diff = int(score_a) - int(score_b)
            sa = 1 / (1 + math.exp(-0.015 * score_diff))  # Sigmoid function for proportional scores
            sb = 1 - sa  # Complementary probability for team B

            k = 96

            adjustments[team_a] += k * (sa - ea)
            adjustments[team_b] += k * (sb - eb)

            # Use full team names for output
            full_name_a = team_names.get(team_a, "Unknown Team")
            full_name_b = team_names.get(team_b, "Unknown Team")


            print(f"Game: {full_name_a} vs {full_name_b}")
            print(f"Ratings - {team_a}: {self.ratings[team_a]}, {team_b}: {self.ratings[team_b]}")
            print(f"Expected Score: {ea:.2f} - {eb:.2f}, Actual Score: {sa:.2f} - {sb:.2f}")
            print(f"Initial Positions - {team_a}: {initial_positions[team_a]}, {team_b}: {initial_positions[team_b]}")
            print(f"Adjustment: {team_a}: {k * (sa - ea):.2f}, {team_b}: {k * (sb - eb):.2f}")

            print("\n")

        # Apply adjustments
        for team, adjustment in adjustments.items():
            self.ratings[team] += adjustment

        # Calculate final rankings
        final_rankings = sorted(self.ratings.items(), key=lambda item: item[1], reverse=True)
        final_positions = {team: idx + 1 for idx, (team, _) in enumerate(final_rankings)}

        # Print the adjustments with initial and final positions
        for team, adjustment in adjustments.items():
            if adjustment != 0:
                initial_position = initial_positions[team]
                final_position = final_positions[team]
                print(f"{team} Adjustment: {adjustment:.2f}, Initial Position: {initial_position}, New Position: {final_position}")





    def get_rating(self, team_name):
        return self.ratings.get(team_name, "Team not found")


#Usage
initial_ratings_e = {'BOR': 800, 'CTB': 636, 'DHR': 515.5, 'KEM': 689,
                     'MRD': 861, 'MRD(B)': 600, 'PAN': 619.4,  'TIL': 758.6,
                     'TNF': 806, 'TNF(B)': 550, 'SWS': 647.6,
                     }
initial_ratings_w = {
    'AUA': 749.3, 'CWB': 781.7, 'CAB': 722.2,
    'CBB': 817.3, 'CHC': 719.1, 'CLM': 573.4,
    'DGC': 902.5, 'DEM': 600.6, 'DIS': 792.0,
    'FLC': 663.4, 'LCC': 750.6, 'MCM': 973.6,
    'PHH': 766.7, 'PIT': 787.3, 'PITB': 480.0,
    'PSO': 792.4, 'RCR': 794.1, 'SDA': 809.8,
    'SLG': 962.4, 'TRD': 610.0, 'TOM': 762.7
}

games_e = [
    [
        ('KEM', 81, 'TIL', 197),
        ('SWS', 66, 'TIL', 250),
        ('CTB', 109, 'SWS', 108),
        ('CTB', 107, 'KEM', 210),
    ],

    [
        ('CTB', 70, 'TIL', 279),
        ('KEM', 224, 'SWS', 128)
    ],

    [
        ('MRD', 274, 'TNF', 261)
    ],

    [
        ('MRD', 300, 'TNF', 147)
    ],

    [
        ('TIL', 217, 'TNF', 299)
    ],
    [
        ('TIL', 193, 'KEM', 106)
    ],
#    [
#        ('DHR', 82, 'BOR', 256),
#        ('PAN', 111, 'BOR', 193),
#        ('DHR', 103, 'PAN', 158)
#    ],
    [
        ('TIL', 91, 'MRD', 219)
    ],
    [
        ('BOR', 197, 'TIL', 193),
        ('TNF', 484, 'KEM', 103),
    ],

    [
        ('SWS', 257, 'TNF(B)', 165),
        ('MRD(B)', 129, 'SWS', 219),
    ],

    [
        ('MRD', 239, 'TNF', 249),
        ('TNF', 291, 'TIL', 246)
    ],

    #[
    #    ('CTB', 300, 'TNF(B)', 246),
    #],

    #[
    #    ('BOR', 521, 'KEM', 66),
    #    ('MRD', 264, 'TIL', 116),
    #],
    #[
    #    ('BOR', 100, 'TNF', 136),
    #]
]

games_w = [

    [
        ('PHH', 152, 'PIT', 172),
    ],
    [
        ('TOM', 168, 'CHC', 176),
    ],
    [
        ('CHC', 148, 'TOM', 173),
    #   ('RCR', 100, 'SLG', 0),
        ('TRD', 66, 'PIT', 533),
    ],
    [
        ('TRD', 169, 'CLM', 115),
    ],
    [
        ('CAB', 353, 'DEM', 56),
        ('CAB', 334, 'CLM', 46),
        ('CLM', 137, 'DEM', 206),
    ],
    [
        ('CLM', 37, 'PHH', 208),
        ('PHH', 96, 'TOM', 91),
    ],
    [
        ('CLM', 51, 'TOM', 364),
    ],
    [
        ('DEM', 59, 'RCR', 339),
    ],
    [
        ('CAB', 113, 'SDA', 236),
    ],
    [
        ('DGC', 230, 'SDA', 120),
        ('DGC', 113, 'SLG', 168),
        ('SLG', 284, 'CAB', 77),
    ],
    [
        ('CAB', 55, 'DGC', 413),
        ('SDA', 75, 'SLG', 290),
    ],
    [
        ('AUA', 135, 'PIT', 121),
        ('AUA', 43, 'CBB', 173),
        ('CWB', 172, 'DIS', 175),
        ('CWB', 147, 'LCC', 136),
        ('CBB', 124, 'PIT', 135),
        ('DIS', 180, 'LCC', 96),
    ],
    [
        ('CWB', 232, 'AUA', 91),
        ('CBB', 102, 'DIS', 142),
        ('PIT', 122, 'LCC', 115),
    ],
    [
        ('CWB', 386, 'CLM', 85),
        ('CWB', 200, 'PHH', 147),
    ],
    [
        ('CLM', 72, 'PHH', 252),
    ],
    [
        ('CHC', 173, 'PSO', 163),
        ('CHC', 81, 'LCC', 208),
        ('LCC', 176, 'PSO', 175),
        ('RCR', 145, 'CBB', 132),
    ],
    [
        ('CLM', 35, 'RCR', 313),
    ],
    [
        ('CWB', 167, 'RCR', 134),
        ('CWB', 123, 'SDA', 279),
        ('CWB', 43, 'SLG', 291),
        ('CBB', 154, 'PHH', 44),
        ('CBB', 49, 'SLG', 278),
        ('DGC', 151, 'SLG', 130),
        ('DGC', 243, 'SDA', 128),
        ('DGC', 228, 'LCC', 118),
        ('DIS', 130, 'SDA', 169),
        ('DIS', 162, 'PHH', 92),
        ('LCC', 201, 'PIT', 79),
        ('PIT', 115, 'RCR', 191),
    ],
    [
        ('CWB', 213, 'PIT', 132),
        ('CWB', 97, 'MCM', 230),
        ('LCC', 202, 'PSO', 106),
        ('LCC', 120, 'MCM', 197),
        ('PIT', 169, 'PSO', 175),
    ],
    [
        ('CWB', 171, 'PSO', 239),
        ('CWB', 149, 'LCC', 161),
        ('LCC', 228, 'PIT', 77),
        #('MCM', 400, 'PIT', 0),
        ('MCM', 331, 'PSO', 85),
    ],
    [
        ('CLM', 287, 'PITB', 73),
    ],
    [
        ('CLM', 125, 'DEM', 226),
        ('CLM', 123, 'TRD', 208),
        ('DEM', 192, 'TRD', 160),
    ],
    [
        ('FLC', 53, 'TOM', 234)
    ],
]

team_names = {
    'AUA': 'Austin Anarchy',
    'CWB': 'Carolina Wreckingballs',
    'CAB': 'Casco Bay Roller Derby',
    'CBB': 'Chicago Bruise Brothers',
    'CHC': 'Chinook City Roller Derby',
    'CLM': 'Cleveland Guardians Roller Derby',
    'DGC': 'Denver Ground Control',
    'DEM': 'Detroit Men\'s Roller Derby',
    'DIS': 'Disorder',
    'FLC': 'Flour City Roller Derby',
    'LCC': 'Lane County Concussion',
    'MCM': 'Magic City Misfits',
    'PHH': 'Philadelphia Hooligans',
    'PIT': 'Pittsburgh Roller Derby',
    'PITB': 'Pittsburgh Roller Derby (B)',
    'PSO': 'Puget Sound Outcast Derby',
    'RCR': 'Race City Rebels',
    'SDA': 'San Diego Aftershocks',
    'SLG': 'St. Louis Gatekeepers',
    'TRD': 'Terminus Roller Derby',
    'TOM': 'Toronto Men\'s Roller Derby',
    'BOR': 'Borderland Bandits Roller Derby',
    'CTB': 'Crash Test Brummies',
    'DHR': 'DHR Men\'s Roller Derby',
    'KEM': 'Kent Men\'s Roller Derby',
    'MRD': 'Manchester Roller Derby',
    'MRD(B)': 'Manchester Roller Derby (B)',
    'PAN': 'Panam Squad',
    'TIL': 'The Inhuman League',
    'TNF': 'Tyne and Fear Roller Derby',
    'TNF(B)': 'Tyne and Fear Roller Derby (B)',
    'SWS': 'South Wales Silures',
}


elo_system_w = RollerDerbyElo(initial_ratings_w)
elo_system_e = RollerDerbyElo(initial_ratings_e)

for gameday_w in games_w:
    print("\n")
    elo_system_w.update_ratings(gameday_w)

for gameday_e in games_e:
    print("\n")
    elo_system_e.update_ratings(gameday_e)


# Retrieve and print ratings
ratings_e = {team: elo_system_e.get_rating(team) for team in
             ['BOR', 'CTB', 'KEM', 'MRD', 'MRD(B)', 'TIL', 'TNF', 'TNF(B)', 'SWS']}

ratings_w = {team: elo_system_w.get_rating(team) for team in
             ['AUA', 'CWB', 'CAB', 'CBB', 'CHC', 'CLM', 'DGC', 'DEM', 'DIS', 'FLC', 'LCC', 'MCM', 'PHH', 'PIT', 'PITB',
              'PSO', 'RCR', 'SDA', 'SLG', 'TRD', 'TOM']}

#print(ratings)

# Retrieve and sort ratings
sorted_ratings_e = sorted(elo_system_e.ratings.items(), key=lambda item: item[1], reverse=True)
sorted_ratings_w = sorted(elo_system_w.ratings.items(), key=lambda item: item[1], reverse=True)

print("\n")
print("\n")
# Print the ratings in a formatted table
print("MRDA West")
print("Position\tTeam\t\t\tRating")
position = 1
for code, rating in sorted_ratings_w:
    full_name = team_names.get(code, "Unknown Team")
    print(f"{position}\t\t{full_name}\t{rating:.2f}")
    position += 1
print("\n")
print("MRDA East")
print("Position\tTeam\t\t\tRating")
position = 1
for code, rating in sorted_ratings_e:
    full_name = team_names.get(code, "Unknown Team")
    print(f"{position}\t\t{full_name}\t{rating:.2f}")
    position += 1