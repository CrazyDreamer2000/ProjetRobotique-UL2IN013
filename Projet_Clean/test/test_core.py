import unittest
import math
from core import geom, robot, types, cinematique

class TestGeom(unittest.TestCase):

    def test_normaliser_angle(self):
        self.assertAlmostEqual(geom.normaliser_angle(0), 0)
        self.assertAlmostEqual(geom.normaliser_angle(math.pi), -math.pi)
        self.assertAlmostEqual(geom.normaliser_angle(-math.pi), -math.pi)
        self.assertAlmostEqual(geom.normaliser_angle(3 * math.pi), -math.pi)
        self.assertAlmostEqual(geom.normaliser_angle(-3 * math.pi), -math.pi)

    def test_erreur_angle(self):
        self.assertAlmostEqual(geom.erreur_angle(math.pi, 0), -math.pi)
        self.assertAlmostEqual(geom.erreur_angle(0, math.pi), -math.pi)
        self.assertAlmostEqual(geom.erreur_angle(math.pi / 2, math.pi / 4), math.pi / 4)
        self.assertAlmostEqual(geom.erreur_angle(-math.pi / 2, math.pi / 2), -math.pi)

    def test_transformer_point_local_vers_monde(self):
        x, y = geom.transformer_point_local_vers_monde(1, 0, 0, 0, math.pi / 2)
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 1)

    def test_polygone_rectangle_local(self):
        points = geom.polygone_rectangle_local(2, 1)
        expected = [(-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5)]
        for p, e in zip(points, expected):
            self.assertAlmostEqual(p[0], e[0])
            self.assertAlmostEqual(p[1], e[1])

class TestRobot(unittest.TestCase):

    def test_initialisation(self):
        r = robot.Robot(10, 20, 0, 50, 50)
        self.assertEqual(r.rayon_roue, 10)
        self.assertEqual(r.ecartement_roues, 20)
        self.assertEqual(r.pos.x, 50)
        self.assertEqual(r.pos.y, 50)
        self.assertEqual(r.pos.orientation, 0)

class TestTypes(unittest.TestCase):

    def test_pos2d(self):
        p = types.Pos2D(1, 2, math.pi / 4)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.orientation, math.pi / 4)

    def test_roue(self):
        r = types.Roue(5, 10)
        self.assertEqual(r.vitesse_rotation, 5)
        self.assertEqual(r.rotation_totale, 10)

    def test_capteurs(self):
        c = types.Capteurs(0.5, 100)
        self.assertEqual(c.accelerometre, 0.5)
        self.assertEqual(c.capteur_distance, 100)
    
class TestCinematique(unittest.TestCase):

    def setUp(self):
        self.c = cinematique.CinematiqueDeuxRoues(10, 20)

    def test_vitesses_robot_depuis_roues(self):
        v_avant, v_rot = self.c.vitesses_robot_depuis_roues(1, 1)
        self.assertAlmostEqual(v_avant, 10)
        self.assertAlmostEqual(v_rot, 0)

        v_avant, v_rot = self.c.vitesses_robot_depuis_roues(1, -1)
        self.assertAlmostEqual(v_avant, 0)
        self.assertAlmostEqual(v_rot, -1)

    def test_avance_pos(self):
        pos = types.Pos2D(0, 0, 0)
        new_pos = self.c.avance_pos(pos, 10, 0, 1)
        self.assertAlmostEqual(new_pos.x, 10)
        self.assertAlmostEqual(new_pos.y, 0)
        self.assertAlmostEqual(new_pos.orientation, 0)

        new_pos = self.c.avance_pos(pos, 0, math.pi / 2, 1)
        self.assertAlmostEqual(new_pos.x, 0)
        self.assertAlmostEqual(new_pos.y, 0)
        self.assertAlmostEqual(new_pos.orientation, math.pi / 2)
            
if __name__ == '__main__':
    unittest.main()