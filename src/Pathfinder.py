import pygame
import sys
import time
import tree

pygame.init()

display_width = 1000
display_height = 1000

black = (0,0,0) # declaring colours
white = (255,255,255)
grey = (169,169,169)
red = (255,0,0)
green = (0, 255, 0) 
blue = (0, 0, 128)
lblue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pathfinder')
clock = pygame.time.Clock()

v = 50 # number of rows/columns

# Returns a text object of a given font and colour
def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

# Displays text at a given position and colour
def message_display(text, x, y, colour):
    largeText = pygame.font.Font('freesansbold.ttf',12)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect.center = ((x*20+10),(y*20+10))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

# Draws a rectangle at a given position
# The width is always 20 pixels
def draw_rect(x_v, y_v, colour):
  pygame.draw.rect(gameDisplay, colour, 
    (x_v*20+1, y_v*20+1, 19, 19))

# Draws a line between two given points
def draw_line(xi, yi, xf, yf):
  pygame.draw.line(gameDisplay, black, (xi,yi), (xf,yf), 1)

# sets up the initial state of the program
def setup():
  gameDisplay.fill(white)
  for i in range(v+1):
    draw_line(0, 20*i, 20*v, 20*i)
    draw_line(20*i, 0, 20*i, 20*v)
  pygame.display.update()
  pass


# Interprets the grid into a graph, allowing the squares to be put into an array of vertices
class Graph:

  # Creates an array to represent the graph with each location numbered as a vertex
  def __init__(self, vertices):
    self.V = vertices
    self.graph = [[0 for x in range(vertices)]  
                    for y in range(vertices)]

  # Finds the neighbors of a given vertex on the graph
  def getNeighbors(self, p):
    n1 = (p[0]-1, p[1]) #left
    n2 = (p[0]+1, p[1]) #right
    n3 = (p[0], p[1]-1) #up
    n4 = (p[0], p[1]+1) #down
    return [n1, n2, n3, n4]

  # Determines if the points p1 and p2 share an edge
  def isEdge(self,p1,p2):
    g = self.graph
    if ( ((p1[0] < 0) | (p1[0] == self.V)) | ((p1[1] < 0) | (p1[1] == self.V)) ):
      return False
    elif ( ((p2[0] < 0) | (p2[0] == self.V)) | ((p2[1] < 0) | (p2[1] == self.V)) ):
      return False
    elif (g[p1[1]][p1[0]] == 1) | (g[p2[1]][p2[0]] == 1):
      return False
    elif abs(p1[0]-p2[0] + p1[1]-p2[1]) == 1:
      return True
    else:
      return False

  # Finds the minimum manhattan distance between two points on the graph
  def minDistance(self, dist, set):
    min = 1000
    for p in set:
      if (dist[p[1]][p[0]] <= min):
        min = dist[p[1]][p[0]]
        min_i = (p[0], p[1])

    return min_i
  
  # Finds the shortest path between a start and end point if it exists
  def dijkstra(self, start, end):
    Q = [] # Q - Elements that have not been "burned"
    burn = [] # burn - Points on the graph that are "burning"
    Tree = tree.Tree(start) # Initializes the tree object
    dist = [[1000 for x in range(self.V)]  ###dist[y][x]
                    for y in range(self.V)]
    # Inputs every element on the graph into the array Q
    for x in range(self.V):
      for y in range(self.V):
        Q.append((x,y))
    burn.append(start)
    dist[start[1]][start[0]] = 0

    # Only runs while there are elements left that have not been "burned"
    # This will only stop if there are no elements left that are reachable, or the end has beeen found
    # Returns the array of distances from the initial point
    while Q and burn:
      q = self.minDistance(dist, burn)
      if (q != start) & (q != end):
        draw_rect(q[0], q[1], blue)
        pygame.display.update()

      # Removes the element that has been calculated from Q and burn because it has "burned" out
      burn.remove(q)
      Q.remove(q)

      # Determines if the end has been found
      if q == end:
        path = Tree.shortestPath(start, end)
        for node in path:
          if node != end:
            draw_rect(node[0], node[1], green)
            pygame.display.update()
        return dist

      neighbors = self.getNeighbors(q)

      # Calculates the distance from the start and the neighbors of the current element
      for i in neighbors:
        if self.isEdge(q, i):
          if (burn.count(i) == 0) & (Q.count(i) > 0):
            burn.append(i)
          newdist = dist[q[1]][q[0]] + 1
          if newdist < dist[i[1]][i[0]]:
            dist[i[1]][i[0]] = newdist
            Tree.addBranch(i, q)
            if (i != start) & (i != end):
              draw_rect(i[0], i[1], lblue)
              pygame.display.update()

#####################################################################

# The game loops that occurs after dijkstras has concluded
def end_loop(dist):
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: # Processes exit
          pygame.quit()
          quit()

      if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Restart
              setup()
              game_loop()

            elif event.key == pygame.K_d: # Show Distances
              for y in range(v):
                for x in range(v):
                  if dist[y][x] != 1000:
                    message_display(str(dist[y][x]), x, y, white)
                  else:
                    #message_display("X", x, y, black)
                    pass

# The basic game loop, allowing the user to select start and end points, as well as draw walls
# and initialize the algorithm.
def game_loop():
  gameExit = False
  chooseStart = True
  chooseEnd = False
  drawWall = False
  g = Graph(v)
  while not gameExit:
      for event in pygame.event.get(): # event handler
          if event.type == pygame.QUIT: #processes exit
              pygame.quit()
              quit()

          if event.type == pygame.MOUSEBUTTONDOWN:
            if chooseStart == True: ################# start
              (x,y) = pygame.mouse.get_pos()
              start = (x//20, y//20)
              draw_rect(start[0], start[1], green)
              chooseStart = False
              chooseEnd = True
            elif chooseEnd == True: ################# end
              (x,y) = pygame.mouse.get_pos()
              end = (x//20, y//20)
              draw_rect(end[0], end[1], red)
              chooseEnd = False
            else: # Draw walls
              drawWall = True

          if event.type == pygame.MOUSEBUTTONUP: # Stop drawing walls
            drawWall = False

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # Begin the algorithm
              dist = g.dijkstra(start, end)
              end_loop(dist)

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Restart
              setup()
              game_loop()
          
          if drawWall:
            (x,y) = pygame.mouse.get_pos() # gets the current mouse position
            x_v = x // 20
            y_v = y // 20
            if (([x_v, y_v] != start) 
              & ([x_v, y_v] != end)):
              draw_rect(x_v, y_v, grey)
              g.graph[y_v][x_v] = 1


          #print(event)

      pygame.display.update() #updates display
      clock.tick(60)



if __name__ == "__main__":
  setup()
  game_loop()
  pygame.quit()
  quit()