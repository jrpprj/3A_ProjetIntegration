# 3A_ProjetIntegration
Projet d'intégration 3A sur hc10

# Cloner le git



# Fichiers urdf (xacro)

Tous les descripteurs se trouvent dans le répertoire "3A_ProjetIntegration/catkin_ws/urdf_backup/"
Pour lancer le tout, il faudra avoir le tout dans le répertoire "3A_ProjetIntegration/catkin_ws/src/motoman/motoman_hc10_support/urdf/"

# Lancer la demo Rviz depuis le terminal ainsi que le script python une fois avoir suivi le document pdf explicatif

Terminal 1 :
(n'importe quel chemin)$ . /opt/ros/noetic/setup.bash
(chemin)/catkin_ws$ catkin build
(chemin)/catkin_ws$ . devel/setup.bash
(chemin)/catkin_ws$ roslaunch hc10_moveit_config demo.launch

Terminal 2 :
(n'importe quel chemin)$ . /opt/ros/noetic/setup.bash
(chemin)/catkin_ws$ . devel/setup.bash
(chemin)/catkin_ws$ cd src
(chemin)/catkin_ws/src$ python3 traj_planner.py

# Lancer la demo Gazebo depuis le terminal une fois avoir suivi le document pdf explicatif

Terminal 1 :
(n'importe quel chemin)$ . /opt/ros/noetic/setup.bash
(chemin)/catkin_ws$ catkin build
(chemin)/catkin_ws$ . devel/setup.bash
(chemin)/catkin_ws$ roslaunch hc10_gazebo_config demo_gazebo.launch
