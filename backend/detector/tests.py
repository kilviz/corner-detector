# tests.py
import unittest
from detector.source_code.boxdetector import ImageDetector


class ImageDetectorTest(unittest.TestCase):
    def setUp(self):
        self.image_path = 'detector/source_code/images/4_Color.png'
        self.detector = ImageDetector(self.image_path)

    def test_remove_shadow(self):
        self.detector.remove_shadow()
        self.assertTrue(hasattr(self.detector, 'img_without_shadow'))
        self.assertTrue(hasattr(self.detector, 'img_norm'))

    def test_image_processing(self):
        self.detector.remove_shadow()
        self.detector.image_processing()
        self.assertTrue(hasattr(self.detector, 'edged'))
        self.assertTrue(hasattr(self.detector, 'img_after_morph'))

    def test_get_contour(self):
        self.detector.remove_shadow()
        self.detector.image_processing()
        self.detector.get_contour()
        self.assertTrue(hasattr(self.detector, 'contours'))
        self.assertTrue(len(self.detector.contours) > 0)

    def test_draw_contour(self):
        self.detector.remove_shadow()
        self.detector.image_processing()
        self.detector.get_contour()
        initial_boxes_count = len(self.detector.boxes)
        self.detector.draw_contour()
        self.assertGreater(len(self.detector.boxes), initial_boxes_count)

    def test_create_json(self):
        self.detector.remove_shadow()
        self.detector.image_processing()
        self.detector.get_contour()
        self.detector.draw_contour()
        result = self.detector.create_json()
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
