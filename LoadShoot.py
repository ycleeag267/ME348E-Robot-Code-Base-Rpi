import time

class LoadShoot:
    def __init__(self, ShootCommand, currentShoot):
        self.ShootCommand = ShootCommand
        self.currentShoot = currentShoot
        
    def shoot(self):
        self.ShootCommand.value = 1
        
        
            