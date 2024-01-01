# import cProfile, pstats

from crime_game import CrimeGame

if __name__ == "__main__":
#    with cProfile.Profile() as profile:
    game = CrimeGame()
    game.play()
    
    '''
    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.dump_stats("results.prof")
    '''
