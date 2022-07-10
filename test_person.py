import unittest
import person
import matplotlib.pyplot as plt

class MyTestCase(unittest.TestCase):
	def test_something(self):
		shalev = person.Person(50, 50, 0, 10, 30)
		print(shalev)
		arc_points = shalev.ten_point_arc()
		print(arc_points)
		self.assertEqual(len(arc_points), 10)
		fig, axs = plt.subplots()
		axs.set_aspect('equal', 'box')
		fig.tight_layout()
		plt.plot([shalev.x], [shalev.y], 'b.')
		plt.plot([point[0] for point in arc_points], [point[1] for point in arc_points], 'r.')
		plt.show()
		# tuple in arc_points

if __name__ == '__main__':
	unittest.main()
