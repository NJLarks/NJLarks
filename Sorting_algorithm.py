def sort_scores():
    scores = []
    # Open the scoreboard file and read the scores
    with open("scoreboard.txt", "r") as file:
        for line in file:
            name, time_str = line.strip().split(": ")
            if time_str:  # Check if time_str is not empty
                time = int(time_str)
                scores.append((name, time))
                print (scores)
    
sort_scores()