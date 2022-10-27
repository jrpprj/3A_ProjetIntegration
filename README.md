# 3A_ProjetIntegration
Projet d'intégration 3A sur hc10

# Cloner le git

<em>git clone https://github.com/jrpprj/3A_ProjetIntegration.git</em>  

# Fichiers urdf (xacro)

Tous les descripteurs se trouvent dans le répertoire "3A_ProjetIntegration/catkin_ws/urdf_backup/"  
Pour lancer le tout, il faudra avoir le tout dans le répertoire "3A_ProjetIntegration/catkin_ws/src/motoman/motoman_hc10_support/urdf/"  
Pour obtenir le répertoire motoman, il faut cloner le git motoman dans le répertoire "3A_ProjetIntegration/catkin_ws/src/"  

Après s'être placé dans le répertoire "3A_ProjetIntegration/catkin_ws/src/", faire :  
<em>git clone https://github.com/ros-industrial/motman</em>  
Ensuite, pour retourner dans le répértoire "3A_ProjetIntegration/catkin_ws/" faire :  
<em>cd ../</em>  
Et pour bouger les fichiers urdf dans le bon répértoire, faire :  
<em>mv urdf_backup/* src/motoman/motoman_hc10_support/urdf/</em>  

# Lancer la demo Rviz depuis le terminal ainsi que le script python une fois avoir suivi le document pdf explicatif

Terminal 1 :  
<em>(n'importe quel chemin)$ . /opt/ros/noetic/setup.bash</em>  
<em>(chemin)/catkin_ws$ catkin build</em>  
<em>(chemin)/catkin_ws$ . devel/setup.bash</em>  
<em>(chemin)/catkin_ws$ roslaunch hc10_moveit_config demo.launch</em>  

Terminal 2 :  
<em>(n'importe quel chemin)$ . /opt/ros/noetic/setup.bash</em>  
<em>(chemin)/catkin_ws$ . devel/setup.bash</em>  
<em>(chemin)/catkin_ws$ cd src</em>  
<em>(chemin)/catkin_ws/src$ python3 traj_planner.py</em>  

# Lancer la demo Gazebo depuis le terminal une fois avoir suivi le document pdf explicatif

Terminal 1 :  
<em>(n'importe quel chemin)$ . /opt/ros/noetic/setup.bash</em>  
<em>(chemin)/catkin_ws$ catkin build</em>  
<em>(chemin)/catkin_ws$ . devel/setup.bash</em>  
<em>(chemin)/catkin_ws$ roslaunch hc10_gazebo_config demo_gazebo.launch</em>  
