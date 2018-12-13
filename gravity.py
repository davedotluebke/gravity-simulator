"""Use Monte Carlo integration to compute the gravity acting on a person 
   standing on or inside a hollowed-out planet."""

import math
import random

class Vector3(): 
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.c = (x, y, z)  # coordinate tuple
    
    def __str__(self):
        return str(self.c)

    def length(self):
        sq = self.c[0]*self.c[0] + self.c[1]*self.c[1] + self.c[2]*self.c[2]
        return math.sqrt(sq)
    
    def normalize(self):
        """Return a unit vector with the same direction as this vector."""
        l = self.length()
        return Vector3(self.c[0]/l, self.c[1]/l, self.c[2]/l)
    
    def plus(self, other):
        return Vector3(self.c[0]+other.c[0], self.c[1]+other.c[1], self.c[2]+other.c[2])

    def subtract(self, other):
        return Vector3(self.c[0]-other.c[0], self.c[1]-other.c[1], self.c[2]-other.c[2])

    def scale(self, scalar: float):
        return Vector3(self.c[0]*scalar, self.c[1]*scalar, self.c[2]*scalar)

    
class Point3(Vector3):
    def __init__(self, x, y, z):
        self.c = (x, y, z)

    def vec_from_to(src, dest):
        """Return a vector between two points, pointing from src to dest."""
        return dest.subtract(src)

def random_point_on_sphere(r: float) -> Point3: 
    """Return a random point on the surface of a sphere of radius 'r'. """
    # pick a random 'height' (may be negative), then a random angle
    height = random.uniform(-r, r)
    theta = random.uniform(0, 2*math.pi)
    p = Point3(math.sin(theta), height, math.cos(theta))
    # TODO: verify that this code generates well-distributed points (it should)
    return p

def acceleration_from_point(loc: Point3, p: Point3, mass: float) -> Vector3: 
    """Compute the acceleration experienced by an object at location 'loc' due
       to the gravitational attraction of a point 'p' with mass 'mass'."""
    G = 6.67408e-11                 # universal gravitational constant
    V = Point3.vec_from_to(loc, p)  # vector from loc to point p
    dist = V.length()               # distance between loc and p
    V_unit = V.normalize()          # direction of acceleration (unit vector)
    accel_mag = G*mass / dist*dist  # magnitude of the acceleration
    accel_vec = V_unit.scale(accel_mag)  # vector of the acceleration
    return accel_vec


def accumulate_gravity_from_points(radius: float, location: Point3, numpoints: int, mass: float) -> Vector3:
    '''Compute and return total acceleration from `numpoints` points distributed on surface of sphere, 
       with TOTAL mass `mass`, acting on a person at `location`.'''
    ### generate 'numpoints' random points
    ### compute acceleration vectors due to those points 
    ### accumulate into total vector 
    ### (note: numerics may require re-ordering accumulation)
    point_mass = mass / numpoints
    l_points = [random_point_on_sphere(radius) for i in range(numpoints)] # list of random points
    l_accel = [acceleration_from_point(location, x, point_mass) for x in l_points] # list of acceleration vectors

    total_accel = Vector3(0,0,0)
    for a in l_accel:
        total_accel = total_accel.plus(a)
    return total_accel

planet_radius = 1.0                         # radius of planet
location = Point3(0.0, planet_radius, 0.0)  # location of person standing on planet
numpoints = 1000                            # number of points to integrate
planet_mass = 1.0e9                          # mass of individual point

gravity_accel = accumulate_gravity_from_points(planet_radius, location, numpoints, planet_mass)
print(gravity_accel)
gravity_accel = accumulate_gravity_from_points(planet_radius, location, numpoints*10, planet_mass)
print(gravity_accel)
gravity_accel = accumulate_gravity_from_points(planet_radius, location, numpoints*100, planet_mass)
print(gravity_accel)
gravity_accel = accumulate_gravity_from_points(planet_radius, location, numpoints*1000, planet_mass)
print(gravity_accel)

