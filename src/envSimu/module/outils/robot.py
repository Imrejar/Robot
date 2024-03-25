import math
import time

class Robot:
	""" 
	initialisation de notre robot avec ses différents paramètres
	
	:param posx: position en x du robot
	:param posy: position en y du robot
	:param dirr: direction du robot, angle en degré
	:param rayon: rayon du robot, qui est un cercle
	:param diamR: float representant le diametre des roues
	:param distR: float representant la distance entre les deux roues
	:param dpsG: dps de la roue gauche
	:param dpsD: dps de la roue droite
	"""


	def __init__(self,posx, posy, dirr,rayon,diamR):

		self.posx = posx					
		self.posy = posy
		self.lastposx = posx
		self.lastposy = posy					
		self.dirr = dirr%360	
		self.lastdirr = dirr			
		self.rayon=rayon					
		self.diamR=diamR
		self.last_update = 0					
		self.distR=rayon*2
		self.dpsG=0
		self.dpsD=0	


	def getPos(self):
		""" retourne la position
		:retour: tuple (posx,posy)
		"""
		return (self.posx, self.posy)
		
	def getPosRd(self):
		""" retourne la pos de la roue droite
		"""
		x,y = self.getPos()
		dirr=math.radians(self.dirr)
		return x+self.rayon*math.cos(dirr-math.radians(90)),y+self.rayon*math.sin(dirr-math.radians(90))

	def getPosRg(self):
		""" retourne la pos de la roue droite
		"""
		x,y = self.getPos()
		dirr=math.radians(self.dirr)
		return x+self.rayon*math.cos(dirr+math.radians(90)),y+self.rayon*math.sin(dirr+math.radians(90))

	def augDPSg(self):
		"""augmente de dps de la roue gauche de 45
		"""
		self.dpsG +=45
	def augDPSd(self):
		"""augmente de dps de la roue droite de 45
		"""
		self.dpsD +=45
	def dimDPSg(self):
		"""diminue de dps de la roue gauche de 45
		"""
		self.dpsG +=-45
	def dimDPSd(self):
		"""diminue de dps de la roue droite de 45
		"""
		self.dpsD +=-45
	
	def set_motor_dps(self,dpsG,dpsD):
		""" modifie le dpsG et dpsD du robot
			:param dpsG: dpsG du robot
			:param dpsD: dpsD du robot
			:retour: rien 
		"""
		self.lastposx = self.posx
		self.lastposy = self.posy
		self.dpsG = dpsG
		self.dpsD = dpsD


	def rotation(self, angle):		#ANCIENNE METHODE				
		"""fait tourner le robot (angle positif pour tourner a gauche, negatif pour a droite)
			:param angle: angle en degré du quel on veut faire tourner le robot
			:retour: rien, modifie la direction du robot
		"""
		if angle==None:
			return
		angle     = math.radians(angle % 360)
		cos       = math.cos(angle) 
		sin       = math.sin(angle)
		direction = math.radians(self.dirr)
		x, y      = math.cos(direction), math.sin(direction) 
		x         = x*cos-y*sin
		y         = x*sin+y*cos
		if(math.degrees(angle)+self.dirr) % 360 > 180:
			self.dirr = 360 - math.degrees(math.acos(x))
		elif(math.degrees(angle)+self.dirr) % 360 < (-180):
			self.dirr = 360 - math.degrees(math.acos(x))
		else:
			self.dirr = math.degrees(math.acos(x))
	
	def velocityD(self):
		"""
		retourne la vitesse de la roue droite en fonction du dps de celle-ci
		"""
		return self.rayon*(self.dpsD/360)*60*0.10472		#formule pour passer de vitesse angulaire à vitesse linéaire roue droite

		
	def velocityG(self):
		"""
		retourne la vitesse de la roue droite en fonction du dps de celle-ci
		"""
		return self.rayon*(self.dpsG/360)*60*0.10472		#formule pour passer de vitesse angulaire à vitesse linéaire roue gauche

	def getDistance(self,x,y):
		""" rôle du capteur, retourne la distance entre le robot et un point x,y devant lui
		"""
		return math.sqrt((self.posx - x)**2 + (self.posy - y)**2)            
	
		
	def distance_parcourue(self,lastposx,lastposy):
		"""
        Retourne la distance parcourue par le robot depuis la derniere position
        """
		
		return math.sqrt((self.posx-lastposx)**2+(self.posy-lastposy)**2)
	
	"""def angle_parcouruD(self, last_dirr):
		angle = (last_dirr - self.dirr)%360			
		if angle%360 > 180:
			return 360 - angle
		elif angle%360 < (-180):
			return 360 - angle
		else:
			return angle

	def angle_parcouruG(self, last_dirr):
		angle = (last_dirr - self.dirr)%360
		if angle % 360 > 180:
			return angle
		elif angle % 360 < (-180):
			return angle
		else:
			return 360 - angle"""

	def angle_parcouru_droit(self, last_dirr):
		""" retourne l'angle parcouru par le robot à droite
			:param last_dirr: ancienne direction avec laquelle comparer
			:retour: angle parcouru à droite
		"""
		last_dirr_rad = math.radians(last_dirr)
		x1, y1        = math.cos(last_dirr_rad), math.sin(last_dirr_rad)		#points du vecteur a partir de la derniere direction
		dirr_rad      = math.radians(self.dirr)
		x2, y2        = math.cos(dirr_rad), math.sin(dirr_rad)					#points du vecteur a partir de la direction actuelle
		scalaire      = x1*x2 + y1*y2											#calcule produit le produit scalaire
		determinant   = x1*y2 - y1*x2											#calcule le determinant
		angle         = math.atan2(determinant, scalaire)						#calcule l'angle parcouru
		return (360 - math.degrees(angle))%360									#retourne l'angle positif (dans le sens des aiguilles d'une montre)

	def angle_parcouru_gauche(self, last_dirr):
		""" retourne l'angle parcouru par le robot à gauche
		:param last_dirr: ancienne direction avec laquelle comparer
		:retour: angle parcouru à gauche
		"""
		last_dirr_rad = math.radians(last_dirr)
		x1, y1        = math.cos(last_dirr_rad), math.sin(last_dirr_rad) 
		dirr_rad      = math.radians(self.dirr)
		x2, y2        = math.cos(dirr_rad), math.sin(dirr_rad) 
		scalaire      = x1*x2 + y1*y2
		determinant   = x1*y2 - y1*x2
		angle         = math.atan2(determinant, scalaire)
		return math.degrees(angle)%360											#retourne l'angle positif (dans le sens inverse des aiguilles d'une montre)
		
			
def angleVecteur(vecteur):		#ANCIENNE METHODE
	"""calcul l'angle positif du vecteur (par rapport a l'axe des abscisse)
		:param vecteur: vecteur (x,y)
		:retour: angle du vecteur
	"""
	if vecteur==(0,0):
		return None									
	x1, y1     = vecteur
	x2, y2     = 1, 0
	norme1     = math.sqrt(x1**2 + y1**2)
	norme2     = math.sqrt(x2**2 + y2**2)
	scalaire   = x1*x2 + y1*y2
	angle      = math.degrees(math.acos(scalaire / (norme1*norme2)))
	if y1 < 0:								# permet de calculer l'angle positif
		return 360-angle
	else:
		return angle
		

rbt = Robot(0,0,350,0,0)
#print(rbt.angle_parcouruD(350))
print(rbt.angle_parcouru_droit(90))
#print(rbt.angle_parcouruG(350))
print(rbt.angle_parcouru_gauche(90))