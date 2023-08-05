__copyright__ = "Copyright (C) 2020 piz2a. All rights reserved."

import numpy as np


def crop_image(image, coord_start: tuple, size: tuple):
    (y1, x1), (h, w) = coord_start, size
    return [row[x1: x1 + w] for row in image[y1: y1 + h]]


def reverse_image(image):
    return np.array([list(reversed(col)) for col in image])


def layer_image(image_buttom, image_top, coord: tuple):
    y, x = coord
    res = image_buttom
    for column, pixels in enumerate(image_top):
        for row, pixel in enumerate(pixels):
            res[y + column][x + row] = image_top[column][row]
    return res


def image2skin(input_path='input.png', log_msg=False, save_image=False, output_path='output.png'):
    import imageio
    from skimage.transform import resize
    from skimage import img_as_ubyte

    c = 4  # png

    def log(*args, **kwargs):
        if log_msg:
            print(*args, **kwargs)

    log(f'Loading {input_path}')
    face_image = img_as_ubyte(resize(imageio.imread(input_path), (32, 32)))

    log('Generating basic skin template...')
    result = np.zeros((64, 64, c)).astype(np.uint8)
    rect_list = [
        # rect size, rect coord, fill value
        [(32, 32), (0, 0), 255],
        [(8, 8), (0, 0), 0],
        [(8, 8), (0, 24), 0],
        [(4, 4), (16, 0), 0],
        [(4, 8), (16, 12), 0],
        [(16, 24), (16, 32), 255],
        [(4, 8), (16, 36), 0],
        [(4, 4), (16, 52), 0],
        [(16, 32), (48, 16), 255],
        [(4, 4), (48, 16), 0],
        [(4, 8), (48, 28), 0],
        [(4, 4), (48, 44), 0]
    ]
    for rect in rect_list:
        top = np.empty((rect[0][0], rect[0][1], c))
        top.fill(rect[2])
        layer_image(result, top, rect[1])

    log('Generating skin...')
    cut_list = [
        # crop coord, crop size, layer coord, is reversing
        [(0, 4), (8, 24), (8, 0), False],  # Head (hair)
        [(16, 12), (16, 4), (16, 4), False],  # Right leg (left mouth)
        [(20, 12), (12, 4), (20, 8), True],
        [(16, 16), (16, 4), (48, 20), False],  # Left leg (right mouth)
        [(20, 16), (12, 4), (52, 16), True],
        [(4, 12), (16, 8), (16, 20), False],  # Body (eyes & nose)
        [(20, 12), (4, 8), (16, 28), False],
        [(8, 20), (12, 4), (20, 28), False],  # Right arm (right eye)
        [(4, 20), (16, 4), (48, 36), False],
        [(8, 20), (12, 4), (52, 32), True],
        [(8, 8), (12, 4), (20, 16), False],  # Left arm (left eye)
        [(4, 8), (16, 4), (16, 44), False],
        [(8, 8), (12, 4), (20, 48), True]
    ]
    for cut in cut_list:
        cut_image = crop_image(face_image, cut[0], cut[1])
        if cut[3]:
            cut_image = reverse_image(cut_image)
        layer_image(result, cut_image, cut[2])

    if save_image:
        log(f'Saving skin to {output_path}')
        imageio.imwrite(output_path, result)

    log('Complete.')

    return result


if __name__ == '__main__':
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    import sys

    Tk().withdraw()

    initialdir = './'
    filetypes = [('PNG files', '*.png')]

    input_image = askopenfilename(initialdir=initialdir, title='Select Image', filetypes=filetypes)
    if not input_image:
        sys.exit(1)
    output_image = asksaveasfilename(initialdir=initialdir, title='Save As', filetypes=filetypes)
    if not output_image:
        sys.exit(1)
    if not output_image.endswith('.png'):
        output_image += '.png'

    image2skin(
        input_path=input_image,
        log_msg=True,
        save_image=True,
        output_path=output_image
    )
    input('Press ENTER to exit...')

del np
