import threading
import time



class IA(threading.Thread):

    def __init__(self, proxy, action):

        threading.Thread.__init__(self)
        self.action = action
        self.proxy  = proxy

    def start(self):
        return self.action.start()
    
    def update(self):
        self.action.update()

    def done(self):
        return self.action.done()

    def run(self):
        self.start()
        while not (self.done()):
            self.update()
            time.sleep(0.0001)





class IAifte:

    def __init__(self, proxy, main_action, secondary_action, condition):

        self.proxy             = proxy
        self.main_action       = main_action         #example: ParcourirDistance
        self.secondary_action  = secondary_action    #example: TournerDroite
        self.condition         = condition
        self.started_secondary = False


    def start(self):

        self.main_action.start()


    def update(self):
        print(self.proxy.proche_obstacle())
        print("dist: ", self.proxy.env.get_distance())
        if self.done():
            self.main_action.running      = False 
            self.secondary_action.running = False
            return

        if self.condition(self.proxy):
            if not self.started_secondary:
                self.secondary_action.start()
                self.started_secondary = True
            self.secondary_action.update()
        else:
            self.main_action.update()

    def done(self):
        return (self.main_action.done() or (self.started_secondary and self.secondary_action.done()))


    

class IAseq:

    def __init__(self, proxy, list):
        self.proxy   = proxy
        self.list    = list
        self.index   = 0

    def start(self):
        self.index   = 0
        self.list[self.index].start()

    def update(self):
        if self.list[self.index].done():
            self.index += 1
            if self.done():
                return
            self.list[self.index].start()
        self.list[self.index].update()

    def done(self):
        return self.index >= len(self.list)

    


class IAloop:

    def __init__(self, proxy, loop_action):

        self.proxy            = proxy
        self.loop_action      = loop_action

    def start(self):

        self.loop_action.start()

    def update(self):

        if self.done():
            return

        if self.loop_action.done():
            self.loop_action.start()

        else:
            self.loop_action.update()

    def done(self):
        return False 



class ParcourirDistance:

    def __init__(self, proxy, distance, dps):
        self.proxy    = proxy
        self.distance = distance
        self.dps      = dps

    def start(self):
        self.proxy.reset()

    def update(self):
        if self.done(): 
            return
        self.proxy.avance_droit(self.dps)
        
    def done(self):
        distance_parcourue = self.proxy.dist_parcourue()
        return distance_parcourue >= self.distance
    

class TestCercle:

    def __init__(self, proxy, distance, dps1, dps2):
        self.proxy    = proxy
        self.distance = distance
        self.dps1     = dps1
        self.dps2     = dps2

    def start(self):
        self.proxy.reset()

    def update(self):
        if self.done(): 
            return
        self.proxy.test_cercle(self.dps1, self.dps2)
        
    def done(self):
        distance_parcourue = self.proxy.dist_parcourue()
        return distance_parcourue >= self.distance


class Arrete:
    def __init__(self, proxy):
        self.proxy   = proxy

    def start(self):
        self.proxy.reset()

    def update(self):
        self.proxy.stop()
        if self.done(): return

    def done(self):
        return True


class TournerDroiteAngle:
    def __init__(self, proxy, angle, dps):
        self.proxy    = proxy
        self.angle    = angle
        self.dps      = dps

    def start(self):
        self.proxy.reset()


    def update(self):
        if self.done():
            return
        self.proxy.tourne_droite(self.dps)

    def done(self):
        angle_parcouru = self.proxy.angle_parcouruD()
        #print("DIRECTION = ",self.proxy.robot.dirr)
        return angle_parcouru >= self.angle
    

class TournerGaucheAngle:
    def __init__(self, proxy, angle, dps):
        self.proxy    = proxy
        self.angle    = angle
        self.dps      = dps

    def start(self):
        self.proxy.reset()

    def update(self):
        if self.done():
            return
        self.proxy.tourne_gauche(self.dps)

    def done(self):
        angle_parcouru = self.proxy.angle_parcouruG()
        return angle_parcouru >= self.angle 
    

class Carre(IAseq):
    def __init__(self,proxy, distance, dps):
        IAseq.__init__(self,proxy,list)
        self.act1 = ParcourirDistance(self.proxy,distance,dps)
        self.act2 = TournerDroiteAngle(self.proxy,90,dps)
        self.act3 = Arrete(self.proxy)
        self.list = [self.act1,self.act2,self.act3]*4

    def start(self):
        IAseq.start(self)

    def update(self):
        IAseq.update(self)

    def done(self):
        if(IAseq.done(self)):
            return True    
        return False

def obstacle_proche(proxy):
    return proxy.proche_obstacle()
