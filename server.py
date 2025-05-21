# Planet lab in Python for DVA248 Datorsystem
#
#   author: Dag Nyström, 2020
#
import threading
import time
import os
from space import space
from cscomm import serverInitSocket, serverWaitForNewClient, serverRecvPlanet, serverSendString
from planet import planet
from math import sqrt

SPACEX = 800
'''Constant for width of the universe in pixels/coordinates'''
SPACEY = 600
'''Constant for height of the universe in pixels/coordinates'''

class universe:
    planet_list = []
    DT : int

    def __init__(self, dt=10):
        self.planet_list.clear()
        self.DT = dt
        self.lock = threading.Lock()

    def add_planet(self, p):
        with self.lock:
            self.planet_list.append(p)

    def remove_planet(self, p):
        with self.lock:
            self.planet_list.remove(p)

    def get_planets(self):
        with self.lock:
            return list(self.planet_list)

    def calculate_planet_pos(self, p: planet):
        '''Method to calculate the position of planet p, relative to all other planets in the system. The method updates the position and age of planet p'''
        Atotx = 0.0
        Atoty = 0.0
        G = 6.67259 * pow(10, -11)  # Gravitational constant

        for cur in self.planet_list:
            if cur != p:
                x = cur.sx - p.sx
                y = cur.sy - p.sy
                r = sqrt(pow(x, 2) + pow(y, 2))
                a = G * (cur.mass / pow(r, 2))
                Atotx += a * (x / r)
                Atoty += a * (y / r)

        p.vx += Atotx * self.DT
        p.vy += Atoty * self.DT
        p.sx += p.vx * self.DT
        p.sy += p.vy * self.DT
        p.life -= 1

def graphic_thread(universe, canvas):
    '''Dedicated thread for drawing all planets'''
    while True:
        # If there are no planets, sleep for 1 second and continue
        # This is to prevent unnecessary computations
        if (len(universe.planet_list) == 0):
            time.sleep(1)
            continue

        # Draw a black rectangle over the entire canvas to clear it
        canvas.c.create_rectangle(0, 0, SPACEX, SPACEY, fill="black", outline="black")
        
        # Draw all planets
        planets = universe.get_planets()
        for planet in planets:
            if planet.name == "Sun":
                canvas.putPlanet(int(planet.sx), int(planet.sy), rad=5, color="yellow")
            elif planet.name == "Oops":
                canvas.putPlanet(int(planet.sx), int(planet.sy), rad=5, color="red")
            elif planet.name == "Comet":
                canvas.putPlanet(int(planet.sx), int(planet.sy), rad=5, color="blue")
            elif planet.name == "Earth":
                canvas.putPlanet(int(planet.sx), int(planet.sy), rad=5, color="green")
            else:
                canvas.putPlanet(int(planet.sx), int(planet.sy), rad=5, color="white")
        
        time.sleep(0.1)

def main():
    # Create the universe (i.e., an empty set of planets)
    u = universe()
    # Create the window on which to draw the universe
    s = space(SPACEX, SPACEY)

    def planet_updater(p):
        '''Updates the position of a planet.'''
        while p.life > 0:
            # Calculate the position of the planet
            with u.lock:
                u.calculate_planet_pos(p)

            # Check if the planet has left the universe
            if (p.sx >= SPACEX or p.sx <= 0):
                serverSendString(p.cSock, f"Planet {p.name} lämnade det kända universum (X)")
                u.remove_planet(p)
                return
            elif (p.sy >= SPACEY or p.sy <= 0):
                serverSendString(p.cSock, f"Planet {p.name} lämnade det kända universum (Y)")
                u.remove_planet(p)
                return
                
            # Decrease the life of the planet after each update
            p.life -= 1
        
            if (p.life <= 0): # If the planet has no life left, send a message to the client
                serverSendString(p.cSock, f"Planet {p.name} har dött av ålder")
                u.remove_planet(p)
                return
            
            time.sleep(0.1)

    def planet_handler(client_socket):
        '''Handles communication with a single client.'''
        while True:
            try:
                p = serverRecvPlanet(client_socket)
                if p is None:
                    break
                p.cSock = client_socket # Set the planet socket to the client socket for later use
                if type(p.life) != int: # If the life is not an integer, convert it to an integer
                    p.life = int(p.life)
                print(f"Received Planet: {p.name}")
                u.add_planet(p)
                threading.Thread(target=planet_updater, args=(p,), daemon=True).start()
            except Exception as e:
                print(f"Error in client handler: {e}")
                break
        client_socket.close()

    def server_thread():
        '''Handles incoming client connections.'''
        server_socket = serverInitSocket()
        while True:
            try:
                client_socket = serverWaitForNewClient(server_socket)
                threading.Thread(target=planet_handler, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print(f"Error in server thread: {e}")
                break
        server_socket.close()

    # Start the drawing thread
    threading.Thread(target=graphic_thread, args=(u, s), daemon=True).start()

    # Start the server thread
    threading.Thread(target=server_thread, daemon=True).start()

    # Last part of main function is the window management loop, will terminate when window is closed
    s.mainLoop()


if __name__ == "__main__":
    main()