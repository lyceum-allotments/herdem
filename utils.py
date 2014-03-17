import math


def allowed_directions(theta, allowed_directions):
    """Given you're colliding with an object located in a direction 'theta'
    from your centre, calculate the allowed directions (up, down, left, right)
    where movement is possible."""
    if theta >= 45 and theta < 135:
        allowed_directions['DOWN'] = False
    elif theta >= 135 and theta < 225:
        allowed_directions['RIGHT'] = False
    elif theta >= 225 and theta < 315:
        allowed_directions['UP'] = False
    elif theta >= 315 or theta < 45:
        allowed_directions['LEFT'] = False

    return allowed_directions

def distance(p0, p1):
    ''' Calculates the distance between 2 points'''
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)