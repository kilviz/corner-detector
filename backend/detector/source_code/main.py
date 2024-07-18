from boxdetector import ImageDetector
if __name__ == "__main__":

    path = 'source_code/images/4_Color.png'
    img = ImageDetector(path, 'orig', 2000, 50_000)
    img.run()
