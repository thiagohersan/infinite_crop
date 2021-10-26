def image_to_mask_array(img, ALPHA_THRESHOLD = 0xF0):
    width, height = img.size
    return [[0x01 if img.getpixel((c, r))[3] > ALPHA_THRESHOLD else 0x00 for c in range(width)] for r in range(height)]

# https://stackoverflow.com/a/30418912
def get_largest_opaque_rectangle_crop(mask, DESIRED_RATIO = 3.0):
    mask_height = mask.shape[0]
    mask_width = mask.shape[1]

    running_width = np.array([[0] * mask_width for _ in range(mask_height)])
    running_height = np.array([[0] * mask_width for _ in range(mask_height)])

    max_area = 0
    max_crop = (0, 0, 0, 0)

    for r in range(mask_height):
        for c in range(mask_width):
            if mask[r][c] == 0x00:
                continue

            if r == 0:
                running_height[r][c] = 1
            else:
                running_height[r][c] = running_height[r - 1][c] + 1

            if c == 0:
                running_width[r][c] = 1
            else:
                running_width[r][c] = running_width[r][c - 1] + 1

            minw = running_width[r][c]

            for dh in range(running_height[r][c]):
                minw = min(minw, running_width[r - dh][c])
                area = (dh + 1) * minw
                aspect_ratio = float(minw) / float(dh + 1) if (mask_width >= mask_height) else float(dh + 1) / float(minw)

                if area > max_area and aspect_ratio > DESIRED_RATIO:
                    max_area = area
                    max_crop = (
                        float(c - minw + 1) / float(mask_width),
                        float(r - dh) / float(mask_height),
                        float(c) / float(mask_width),
                        float(r) / float(mask_height)
                    )

    return max_crop
