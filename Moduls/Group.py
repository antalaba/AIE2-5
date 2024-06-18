import numpy as np


class Cluster():
    def __init__(self,points) -> None:
        self.points = points #a list of lists all the points that are clustered togheter
        self.mid = self.mid() #float middle point of the cluster

    def mid(self):
        x = 0
        y = 0
        z = 0
        for i in self.points:
            x += i[0] #sum of the coordinates of the points in a cluster FLOAT
            y += i[1]
            z += i[2]
        return (x / len(self.points), y / len(self.points), z / len(self.points))


class Points():
    def  __init__(self,xyz : list) -> None:
        self.xyz_lixt = xyz  # Matrix of all the points currently seen by the radar 
        self.max_distance = 0.05

    def distance(self,xyz1, xyz2):
        return np.sqrt((xyz1[0] - xyz2[0])**2 + (xyz1[1] - xyz2[1])**2 + (xyz1[2] - xyz2[2])**2)

    def make_cluster(self) -> list:
        clusters = [] #list of clusters which contain points that are lists of coordinates
        explored = [] #list of points that have been alraedy clustered
        for parent in self.xyz_lixt:
            points = [] #buffer of clusters that ou need in order to not have empty clusters
            
            for child in self.xyz_lixt:
                if (child in explored):
                    pass
                else:
                    if self.distance(parent,child) <= self.max_distance:
                        points.append(child)
                        explored.append(child)
                    
            if not points: #if points is empty
                pass
            else:
                clusters.append(points)
            
        return clusters

    def get_cluster(self) -> Cluster: #function that creates a cluster object from the clusters so that you have a mid oint
        clusters = []
        for i in self.make_cluster():
            clusters.append(Cluster(i))

        return clusters


def get_closest_cluster(xyz_list : np.array, offset= np.array([0, 0, 0, 0])) -> Cluster:
    ''' Takes offset as an optonal argument (np.array([0, 0, 0, 0]) [x, y, z, Doppler])  
    Returns the closest cluster object'''
    xyz_list = xyz_list - offset
    xyz_list = np.delete(xyz_list, obj=-1, axis=1)
    xyz_list = xyz_list.tolist()
    point = Points(xyz_list)
    closest = Cluster([[float('inf'),float('inf'),float('inf')]])
    clusters = point.get_cluster()
    cluster_distance = point.distance(closest.mid, [0,0,0])
    for i in clusters:
        if (point.distance(i.mid, [0,0,0]) < cluster_distance):
            closest = i

    return closest

def rotate_xy(Cluster : Cluster, angle: np.degrees) -> tuple:
    """"Takes the closest Cluster obeject and rotates it with angle along the Z-axis"""
    angle = np.deg2rad(angle)
    new_x = Cluster.mid[0] * np.cos(angle) - Cluster.mid[1] * np.sin(angle)
    new_y = Cluster.mid[0] * np.sin(angle) + Cluster.mid[1] * np.cos(angle)
    
    return (new_x, new_y, Cluster.mid[2])

def distance(xyz1: list, xyz2: list):
        return np.sqrt((xyz1[0] - xyz2[0])**2  + (xyz1[1] - xyz2[1])**2 + (xyz1[2] - xyz2[2])**2)


if __name__ == '__main__':
    import random
    a = []
    for i in range(5):
        a.append([random.random() for _ in range(3)])

    point = Points(a)
    print(len(point.get_cluster()))
    for i in point.get_cluster():
        print(i.points)
        print()
    print(get_closest_cluster(a).mid)
