import time
import gl


def test_gl():
    gl.count += 1


if __name__ == '__main__':
    while True:
        test_gl()
        print(gl.count)
        time.sleep(3)