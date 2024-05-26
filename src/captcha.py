import base64
from PIL import Image
import numpy as np
import traceback
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_solver(css_selector):
    return solvers_by_css_selector.get(css_selector)


def solver_rotated_image(driver, css_selector):
    print("challenge rotated_image initiated")
    images = driver.find_elements(By.CSS_SELECTOR, "img.csnl_cp_img")
    assert len(images) == 9
    images_src = [image.get_attribute("src") for image in images]
    index = _identify_rotated(images_src)
    print("challenge rotated_image solved", index)
    # click on the image
    images[index].click()
    driver.find_element(By.CSS_SELECTOR, "button#submit_csnl_cp").click()
    print("clicked submit_csnl_cp")


def _identify_rotated(images_src):
    lower_rows = []
    upper_rows = []
    left_columns = []
    right_columns = []
    for i, img in enumerate(images_src):
        if img.startswith("data:image/png;base64,"):
            img = img[len("data:image/png;base64,") :]
        img = base64.b64decode(img)
        with open(f"/tmp/image_{i}.png", "wb") as f:
            f.write(img)
        # image = Image.fromarray(img)
        image = Image.open(f"/tmp/image_{i}.png")
        size = image.size  # w,h
        lower_rows.append(
            np.matrix([image.getpixel((x, size[1] - 1)) for x in range(size[0])])
        )
        upper_rows.append(np.matrix([image.getpixel((x, 0)) for x in range(size[0])]))
        left_columns.append(np.matrix([image.getpixel((0, y)) for y in range(size[1])]))
        right_columns.append(
            np.matrix([image.getpixel((size[0] - 1, y)) for y in range(size[1])])
        )
    # only one can be rotated
    cumulative_differences = []
    r = lambda a: a[::-1]
    for i in range(9):
        if i == 0:
            diff_pairs_rows = [
                (r(upper_rows[0]), upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (r(left_columns[0]), left_columns[1]),
                (right_columns[1], left_columns[2]),
                (right_columns[3], left_columns[4]),
                (right_columns[4], left_columns[5]),
                (right_columns[6], left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 1:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (r(upper_rows[1]), upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], r(right_columns[1])),
                (r(left_columns[1]), left_columns[2]),
                (right_columns[3], left_columns[4]),
                (right_columns[4], left_columns[5]),
                (right_columns[6], left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 2:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (r(upper_rows[2]), upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], r(right_columns[2])),
                (right_columns[3], left_columns[4]),
                (right_columns[4], left_columns[5]),
                (right_columns[6], left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 3:
            diff_pairs_rows = [
                (lower_rows[0], r(lower_rows[3])),
                (r(upper_rows[3]), upper_rows[6]),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], left_columns[2]),
                (r(left_columns[3]), left_columns[4]),
                (right_columns[4], left_columns[5]),
                (right_columns[6], left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 4:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (lower_rows[1], r(lower_rows[4])),
                (r(upper_rows[4]), upper_rows[7]),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], left_columns[2]),
                (right_columns[3], r(right_columns[4])),
                (r(left_columns[4]), left_columns[5]),
                (right_columns[6], left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 5:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (lower_rows[2], r(lower_rows[5])),
                (r(upper_rows[5]), upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], left_columns[2]),
                (right_columns[3], left_columns[4]),
                (right_columns[4], r(right_columns[5])),
                (right_columns[6], left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 6:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], r(lower_rows[6])),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], left_columns[2]),
                (right_columns[3], left_columns[4]),
                (right_columns[4], left_columns[5]),
                (r(left_columns[6]), left_columns[7]),
                (right_columns[7], left_columns[8]),
            ]
        elif i == 7:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], r(lower_rows[7])),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], upper_rows[8]),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], left_columns[2]),
                (right_columns[3], left_columns[4]),
                (right_columns[4], left_columns[5]),
                (right_columns[6], r(right_columns[7])),
                (r(left_columns[7]), left_columns[8]),
            ]
        elif i == 8:
            diff_pairs_rows = [
                (lower_rows[0], upper_rows[3]),
                (lower_rows[3], upper_rows[6]),
                (lower_rows[1], upper_rows[4]),
                (lower_rows[4], upper_rows[7]),
                (lower_rows[2], upper_rows[5]),
                (lower_rows[5], r(lower_rows[8])),
            ]
            diff_pairs_columns = [
                (right_columns[0], left_columns[1]),
                (right_columns[1], left_columns[2]),
                (right_columns[3], left_columns[4]),
                (right_columns[4], left_columns[5]),
                (right_columns[6], left_columns[7]),
                (right_columns[7], r(right_columns[8])),
            ]
        # each row has shape (173, 4)
        diff_cum = np.array([0, 0, 0, 0])
        for row in diff_pairs_rows:
            diff_cum += np.sum(np.abs(row[0] - row[1]))
        for column in diff_pairs_columns:
            diff_cum += np.sum(np.abs(column[0] - column[1]))
        total = np.sum(diff_cum)
        cumulative_differences.append(total)
    print("cumulative differences", cumulative_differences)
    result = cumulative_differences.index(min(cumulative_differences))
    print("index minimizing diff", result)
    return result


def solver_pizza(driver, css_selector):
    print("challenge pizza initiated")
    images = driver.find_elements(By.CSS_SELECTOR, "div#captcha-tile-container img")
    assert len(images) == 4
    images_src = [image.get_attribute("src") for image in images]
    try:
        solution = _identify_pizza(images_src)
    except Exception as e:
        print("challenge pizza failed to identify solution", e)
        print(traceback.format_exc())
        return
    print("challenge pizza identified solution", solution)
    # click on the images
    for i, rotation in enumerate(solution):
        for _ in range(rotation):
            images[i].click()
            time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button#captcha-submit-button").click()
    print("clicked submit pizza button")
    time.sleep(2)


def _identify_pizza(images_src):
    # borders is list of list of 4 elements:
    # [top, right, bottom, left] for each image
    borders = []
    for i, img in enumerate(images_src):
        if img.startswith("data:image/png;base64,"):
            img = img[len("data:image/png;base64,") :]
        img = base64.b64decode(img)
        with open(f"/tmp/image_{i}.png", "wb") as f:
            f.write(img)
        # image = Image.fromarray(img)
        image = Image.open(f"/tmp/image_{i}.png")
        size = image.size  # w,h
        # extract pixels
        top = np.matrix([image.getpixel((x, 0)) for x in range(size[0])])
        bottom = np.matrix([image.getpixel((x, size[1] - 1)) for x in range(size[0])])
        # reverse bottom to keep pixels in clockwise order
        bottom = bottom[::-1]
        left = np.matrix([image.getpixel((0, y)) for y in range(size[1])])
        right = np.matrix([image.getpixel((size[0] - 1, y)) for y in range(size[1])])
        # also reverse right
        right = right[::-1]
        borders.append([top, right, bottom, left])
    # now identify rotations that minimize differences
    best_rotations = [0, 0, 0, 0]
    min_diff = float("inf")
    for rot_first in range(4):
        for rot_second in range(4):
            for rot_third in range(4):
                for rot_fourth in range(4):
                    current_borders = [
                        np.roll(borders[0], rot_first),
                        np.roll(borders[1], rot_second),
                        np.roll(borders[2], rot_third),
                        np.roll(borders[3], rot_fourth),
                    ]
                    diff = _get_diff_value(current_borders)
                    if diff < min_diff:
                        min_diff = diff
                        best_rotations = [rot_first, rot_second, rot_third, rot_fourth]
                        print("new best rotations", best_rotations, min_diff)
    return best_rotations


def _get_diff_value(current_borders):
    diff = 0
    # 1st left with 2nd right (reversed)
    diff += np.sum(np.abs(current_borders[0][3] - current_borders[1][1][::-1]))
    # 3rd left with 4nd right (reversed)
    diff += np.sum(np.abs(current_borders[2][3] - current_borders[3][1][::-1]))
    # 1st bottom with 3th top (reversed)
    diff += np.sum(np.abs(current_borders[0][2] - current_borders[2][0][::-1]))
    # 2rd bottom with 4th top (reversed)
    diff += np.sum(np.abs(current_borders[1][2] - current_borders[3][0][::-1]))
    return diff


def solver_cat_in_box(driver, css_selector):
    print("challenge cat_in_box initiated")
    cat = driver.find_element(By.CSS_SELECTOR, "img#cat")
    # drag the cat in the box
    actions = ActionChains(driver)
    actions.move_to_element(cat)
    actions.click_and_hold()
    box = driver.find_element(By.CSS_SELECTOR, "img#box")
    actions.move_to_element(box)
    # make the box move away, let's catch the next time
    actions.pause(2)
    actions.perform()
    print("waiting for box to become green")
    # now wait that the box becomes green
    actions = ActionChains(driver)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.success"))
    )
    actions.release()
    actions.perform()
    print("cat released in box")
    time.sleep(2)


solvers_by_css_selector = {
    "div#_csnl_cp": solver_rotated_image,
    "div#rotate-captcha": solver_pizza,
    "div#dragdrop-captcha": solver_cat_in_box,
}

test_imgs_rotated = [
    "data:image/png;base64,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",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK0AAACtCAYAAADCr/9DAAAFKElEQVR4nOzd2W7iVhzH8f8BJhshLNmml32MPkIfpOpD9rYXvan6CNVkMQECCTshEFdYMR2lKQMZsP2zv5+LSpVGwxnlK+v4LKTw01+TPwwQkot7AMCmiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyiBZyCr/89uuPcQ8C2EShOOl8insQwCaYHkAO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UIO0UKO+/n3v/+MexDAJgqPxR+e4x4EsAmmB5BDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJBDtJCTc612xZ/N8nEPBFhXwbr9Y9cbFN1JaeDXyn3L51/iHhSwSmHxH+f7zrq9kg0GRSuX+1Y9GZhzftyDA95T+Pp/3PwlZ52HsvV6x/4i3kppSLxImvdfxGbzvGt3Ku7L7aX1h4eRjwpYYfXqwWxWcI3WqV17FzZ+2otsVMAKay15uafpnrutX9hdq8ZKA+JW2OQPu8HwyIajQ6suXtbKfea7iMPGmwvO953rPJ64Lzefrdsv7mZYwP/7+I7Y4mWt1a4y30XUvnsbl/kuorbRnHaVYL47Hh9YpdJjfRe7tNUDM27+knPtTmUxZfBH4/1t/t1AaCenvNz0+VPOa5wzZcAubG168B6mDNiFnZ+nXU4ZburnNpl+2vXnIf0iOwS+XGVodcrm+y6qz0X6RHtzwfed6/ZKwUGc4egg0s9GasRz3WY2K7h688zqzVNe1LCpnb6IfYsbjg5tMtm3WrVr5dIwzrFAR+wXG4MXtVa76rzGGU9drCP2aJdG4wN3dfvZHnrHcQ8FyZacaBdP3RffLZfHnp9jnboguRIVbchNnvbtyru0TrfE8hjeSmS0tjy3+1AOnrpTNiXwr8RGG3JP0z27rl8ET11AIVp7+9Rlrpt5EtGGgrnutXfJNZ9sk4rWwhUG1nUzTS7apdH4wC2eur3BUdxDQbR0ow1305r3Nbtr1exlLv1vwfpS8YN2g+GRu/IuueKTDamINjCb54MrPpzXTb30RPvKdXul4LsY2JBIrdRFa68XK4MNCQ7fpFIqo7VwQ6LdqbA0lj6pjXZpND7I3dQvuN6THumP1l6/d6zePOMlLR2yEe2r4CWN8wvyMhWthafGFtMFvpZfVuaitXAnrdE6teZ9lemCnkxGG3K9QZE1XT2ZjtbCNd3FdIGDNzIyH62Fxx2b9zXXaleYLiQf0X6t2z+2m/o5mxHJRrRvBF+Ud+3xXWMJRrTvCFYX6s0z6zyexD0W/BfRrhD86imvcWZzDpgnCT+Mbwmv9fBrpxKDaNcxm+edd3fOUcdkINp1vR51DO6jsSwWK6LdUHAf7dq74NBNfIj2I4KbEd4lh27iQbQfFOyiNVqn7KJFj2i/F7tokSPaLXBP073gSg/LYpEg2m2ZzfPm3Z1zWmz3iHaLghvAzfsad9F2658AAAD//wE0qcW6FB09AAAAAElFTkSuQmCC",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK0AAACtCAYAAADCr/9DAAADZElEQVR4nOzZz4rV5QPH8Tl6zu83OuOfGk2KrOwfUYGbNtUiaNWmbVDLILqHoBtoWTfQqi6iRYVBVoiuwlWZkag1kjaONpMzoYuBQWJGGvrOm3m9Vmf5gfPm4fnyjF88ffPkFITsGnoA3CvRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLzvidz949NvQIttbqaDT152Tm1vXJ/lsLe+eWzx86vvjDkRcWlyZ7VobethXGMzevTIYewdabvTE/mbv9Y35q6tmfvzy4Mhqv/vTA8YUTz7w1f2X/I0tD7/s3xkMP4L+xa/Wv0bFLp/Y9dvn07PdHX7n6xfNv/7a8ezp58rrT7jCj1ZXRc+c/P/jGV+8/PHtzPnloiXaHOnzt3PSbJ947et/1C7nroWh3sNvfM69/+8FDk+UbqQ5SY9l69y/88v/Xznx0ZOgd90K0TD1x8bt9j186tXfoHZslWu54+ewnh4besFmi5Y65a+enn7xwcmboHZshWtY8dfGb2aE3bIZoWfPor2dmRqu3RkPv2IhoWTO9tDA+fPXc/4besRHRss6Bxcvb/pVMtKxzYPHytn8hEy3r7Fm6tnvoDRsRLTmiJUe05IiWHNGSI1pyREuOaMkRLTmiJUe05IiWHNGSI1pyxh+/+uGPQ4/gbi+d/XTu6Qtf7x96x3Y0/n3mweWhR3C3P/Yc9r/8A9cDckRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkvN3AAAA//+9cWf5vLgIWwAAAABJRU5ErkJg",
    "data:image/png;base64,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",
    "data:image/png;base64,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",
    "data:image/png;base64,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",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK0AAACtCAYAAADCr/9DAAADO0lEQVR4nOzYP2sdVAPH8d40D025PFWs1ZZQ61Dxz+AQHaygDoK7bjo5uvqOxHeg0M3FIRDoUKSYpUacCtqkbWKVkJBcidChS0HEnPtNP583cH7DdzjnLF67ubt2as69/+NXz6/8fP254z73xtWPN1df/+zecZ/Lky2MHgD/lGjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOSIlhzRkiNackRLjmjJES05oiVHtOQsjh4wz97e+Ob8wuxgMnoHjxPtE0xmh5O3Nr49P3oHj3M9IEe05IiWHNGSI1pyREuOaMkRLTmiJUe05IiWHNGSI1pyGtFOFmajJzA/EtE+XHr2YPQG5kci2p2lF/ZHb2B+JKLdeuby3ugNzI9EtPeny/vb0xeFy98S0R755cLKw9EbmA+ZaG9d+XBnNpn4RaAT7ea5K3u3L73z++gdjJeJ9sjqa59uHZ7+3+HoHYyVinZ7emn/+zc+/230DsZKRXvkh5c/2lm//MGD0TsYJxftke/e/OLu7eV3t0fvYIxktIcLi7PrK1/+euOVTzZ9Jzx9Jtdu7q6NHvFvLG+tL723/vWFiw82zo7ewvHIR/vI1Ttr01fvrP7/pc1b0zP7f5wevYf/zomJ9pHJ7GBy8f5PZ879eXdxundv8ezuzumFUy4RJ8mJi5aTL/kQ4+kmWnJES45oyREtOaIlR7TkiJYc0ZIjWnJES45oyREtOaIlR7TkiJYc0ZIjWnJES45oyREtOaIlR7TkiJYc0ZIjWnJES45oyREtOaIlR7TkiJYc0ZIjWnJES45oyREtOaIlR7Tk/BUAAP//An5lQnHr5rcAAAAASUVORK5C",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK0AAACtCAYAAADCr/9DAAAFBElEQVR4nOzdz07jRgDH8ZnEBJLYDpt/kATYQx+hpz30FfqSfYM+xV6qvfXWO0sggZCE8CeeKi6hRagt7AaPf873IyEhIZQ5fGWNZ8ZO8OnL4rPB5iXLkj09b5r5zZ7voRRNyfcACqtUTlyve+Ea8bXvoRQN0b4na53pNK9ctz1yq9+xEUSbhTicm/7h0ATlpe+hFAHRZqW6e5cc9c7cbuXO91DUEW2GbBAszVFvaBrR1PdYlBFt1qx1rtO6dAedC1cuJb6Ho4hofYnqN2Y1Xajs3Pseihqi9Wln58Ec989cWJ/7HooSovXNWmcOOyPXaY0Ny2KvQrR50YhmjmWxVyHaPKnu3rnj/ldTqy58DyXPiDZvyuXE9Q/OXXN/4nsoeUW0edXcn7he95xlsZeINs/qtcVqusAu2nNEm3Psor1EtArWu2jd9siVWBYjWiVxOGcXjWj1VCr36S5aHM58D8UXolVkrTPd9nhbD90QrbKofpOuLuzt3voeSpaIVly6ujA43KrNCKItgtV0obk/SfoHW3F2gWgLxNaqt9twdoFoi2Z9dqHTGhf1CWCiLapGNDMnxdwCJtoi29l5MEe9YdFu0oi26J7dpAUPvoezCUS7JdKbtJNeIZ5HI9ptUion6fNo4jtpRLuNHnfSVJfGiHZL2SBYPi2NiV11iXbbNaLZX+cX9mTOLxAtHp+OOBy6VvNSYUOCaPG3D/FUYUOCaPHcekMix1ddosVLq1jXV90cznWJFv8uveo+znVz9EAl0eL/fYin7mRwmpd1XaLFqzyt63bbI9/ruoHPD4egOJy72t6tOR837HRW8zEErrR4s3Rd97Azcr3uuY+TY0SLb1evLdzHwdf0C/4yXB4jWnyf9Rf8HffOsnqUnWixGZXKfbopkcEBHG7EsFmNaObq1YUZXcZ2Mq2/x0dwpcXGpTdq3fY46R8M3+NleUSLd2Nr1dv0ZXmt5uUmpwxEi/f1eI4hPbO7oTc9Ei0ysZ4yuMH3f6k10SJb1d27dMrQbY++9b1jrB7Ajzicu6h+Y8ZX0erHOmdf+69caeHP44tE3MfB6Vvex0C08O7pLMPgdbtqRIv8WM13j3pDd9C5MP+xvsucFvkT1W9cWFuYybRmx5exeViW//lnokU+rea7jWjm4nBuxpPQXF1FdpmkMwOiRb6lN2uNa7MfztzFVWQm1yHRQkOpnKRHID/EU27EIMUGwZJoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoIYdoISf46fdfWr4HAbxF8OMfvxItpDA9gByihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihRyihZzgtx9+vvA9COAt7Kcvi8++BwG8BdMDyCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayCFayPkzAAD///eOWfpztbu6AAAAAElFTkSuQmCC",
    "data:image/png;base64,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",
]


def main():
    _identify_rotated(test_imgs_rotated)


if __name__ == "__main__":
    main()
