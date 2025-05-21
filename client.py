import time
import threading
from planet import planet
from cscomm import clientInitSocket, clientRecvString, clientSendPlanet

# Create the planets
sun = planet("Sun", 300, 300, 0, 0, 10e8, 10e8)
earth = planet("Earth", 200, 300, 0, 0.008, 1000, 10e8)

# Initialize the client socket
s = clientInitSocket()

def client_thread(s):
    while True:
        message = clientRecvString(s)
        print(f"\nMESSAGE FROM SERVER: {message}")
        time.sleep(0.1)

threading.Thread(target=client_thread, args=(s,), daemon=True).start()    

while True:
    choice = input("Would you like to create a new planet or choose from a preset? (c/p/END): ")
    if (choice == "c"):
        name = input("Enter the name of the planet: ")
        x = input("Enter the x coordinate of the planet: ")
        y = input("Enter the y coordinate of the planet: ")
        vx = input("Enter the x velocity of the planet: ")
        vy = input("Enter the y velocity of the planet: ")
        mass = input("Enter the mass of the planet: ")
        life = input("Enter the life of the planet: ")
        clientSendPlanet(s, planet(name, x, y, vx, vy, mass, life))
    elif (choice == "p"):
        print("Presets:")
        print("1. Earth and Sun")
        print("2. Comet")
        print("3. Oops")
        preset = input("Enter the number of the preset: ")
        if (preset == "1"):
            clientSendPlanet(s, sun)
            time.sleep(0.1)
            clientSendPlanet(s, earth)
        elif (preset == "2"):
            comet = planet("Comet", 500, 300, 0.1, 0, 1000, 10e8)
            clientSendPlanet(s, comet)
            time.sleep(0.1)
        elif (preset == "3"):
            comet = planet("Oops", 500, 400, 0, 0, 10e9, 100)
            clientSendPlanet(s, comet)
            time.sleep(0.1)
    elif (choice == "END"):
        break

# Close the socket
s.close()