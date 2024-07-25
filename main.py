import cv2
import numpy as np
import pathlib

FACTOR = 0.2

def process_image(file_path):
    img = cv2.imread(file_path)

    height, width, _ = img.shape
    w = int(width * FACTOR)
    h = int(height * FACTOR)

    img = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)

    images = [("original", img)]

    # ---------------------------------------------------------------------------

    oil = cv2.xphoto.oilPainting(img, 3, 1)
    images.append(("oil", oil))

    # ---------------------------------------------------------------------------

    gaussian_blur = cv2.GaussianBlur(img, (3, 3), 0, 0)
    # images.append(("gaussian_blur", gaussian_blur))

    # ---------------------------------------------------------------------------

    # canny_edges = cv2.Canny(gaussian_blur, threshold1=100, threshold2=200)
    canny_edges = cv2.Canny(oil, threshold1=100, threshold2=200)
    images.append(("canny", canny_edges))

    # ---------------------------------------------------------------------------

    embossed_edges_kernel = np.array([[0, -3, -3],
                                      [3, 0, -3],
                                      [3, 3, 0]])
    embossed_edges = cv2.filter2D(img, -1, kernel=embossed_edges_kernel)
    images.append(("embossed_edges", embossed_edges))

    # ---------------------------------------------------------------------------

    sketch = cv2.pencilSketch(cv2.GaussianBlur(img, (5,5), 0, 0))
    # images.append(("sketch", sketch))

    # ---------------------------------------------------------------------------

    style = cv2.stylization(gaussian_blur, sigma_s=10, sigma_r=0.1)
    images.append(("stylization", style))

    # ---------------------------------------------------------------------------

    hdr = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.1)
    images.append(("hdr", hdr))

    # ---------------------------------------------------------------------------

    invert = cv2.bitwise_not(img)
    images.append(("invert", invert))

    # ---------------------------------------------------------------------------

    ALPHA = 0.2
    canny_merge = cv2.merge((canny_edges, canny_edges, canny_edges))
    canninvert = cv2.addWeighted(canny_merge, ALPHA, invert, (1 - ALPHA), 0)
    images.append(("canninvert", canninvert))

    # ---------------------------------------------------------------------------

    for n, i in images:
        cv2.imshow(n, i)
    
    # cv2.imshow("original", img)
    # cv2.imshow("oil", oil)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    files = [f for f in pathlib.Path().glob("images/*.jpg")]
    for f in files:
        process_image(f)
        pass

if __name__ == "__main__":
    main()
