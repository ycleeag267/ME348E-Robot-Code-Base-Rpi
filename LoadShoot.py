import time

class LoadShoot:
    def __init__(self, ShootCommand):
        self.ShootCommand = ShootCommand
        
    def shoot(self):
        self.ShootCommand.value +=1
        
        
            