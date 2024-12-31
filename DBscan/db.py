import pygame
import numpy as np

def dist(A, B):
    return np.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

def get_neighbors(points, point_idx, epsilon):
    neighbors = []
    for i, p in enumerate(points):
        if dist(p, points[point_idx]) <= epsilon:
            neighbors.append(i)
    return neighbors

def expand_cluster(points, labels, point_idx, cluster_id, epsilon, minPts):
    seeds = get_neighbors(points, point_idx, epsilon)

    if len(seeds) < minPts:
        labels[point_idx] = -1
        return False
    else:
        labels[point_idx] = cluster_id
        seeds.remove(point_idx)

        while seeds:
            current_point = seeds.pop()
            if labels[current_point] == 0:
                labels[current_point] = cluster_id
                neighbors = get_neighbors(points, current_point, epsilon)

                if len(neighbors) >= minPts:
                    seeds.extend(neighbors)
            elif labels[current_point] == -1:
                labels[current_point] = cluster_id
        return True


def dbscan(points, epsilon, minPts):
    labels = [0] * len(points)
    cluster_id = 1

    for point_idx in range(len(points)):
        if labels[point_idx] == 0:
            if expand_cluster(points, labels, point_idx, cluster_id, epsilon, minPts):
                cluster_id += 1
    return labels


def brush(pos):
    near_points = []
    for i in range(np.random.randint(1, 7)):
        x = pos[0] + np.random.randint(-20, 20)
        y = pos[1] + np.random.randint(-20, 20)
        near_points.append((x, y))
    return near_points


def colors(k):
    colors = []
    for i in range(k + 1):
        colors.append((np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
    colors.append((255, 0, 0))
    return colors


def main():
    epsilon = 35
    minPts = 5
    radius = 3
    points = []
    labels = []
    is_pressed = False

    pygame.init()
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    screen.fill("#FFFFFF")
    pygame.display.update()

    clrs = ["black"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.WINDOWRESIZED:
                screen.fill("#FFFFFF")
                for i in range(len(points)):
                    pygame.draw.circle(screen, clrs[labels[i]], points[i], radius)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_pressed = False

            if event.type == pygame.MOUSEMOTION and is_pressed:
                pos = event.pos
                if len(points) == 0 or dist(pos, points[-1]) > 20:
                    near_points = brush(pos)
                    for point in near_points:
                        pygame.draw.circle(screen, "black", point, radius)
                        labels.append(0)
                        points.append(point)
                    pygame.draw.circle(screen, "black", pos, radius)
                    points.append(pos)
                    labels.append(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    labels = dbscan(points, epsilon, minPts)

                    k = np.max(labels)

                    clrs = colors(k)
                    for i in range(len(points)):
                        pygame.draw.circle(screen, clrs[labels[i]], points[i], radius)

                if event.key == pygame.K_ESCAPE:
                    points = []
                    labels = []
                    screen.fill('#FFFFFF')

            pygame.display.flip()

if __name__ == "__main__":
    main()
