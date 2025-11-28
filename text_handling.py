from PIL import Image
import characters
import struct


def flip_bit_order(bits: int, bpp: int) -> int:
    """Flip the bit order of a value with given bits per pixel"""
    result = 0
    for i in range(bpp):
        if bits & (1 << i):
            result |= 1 << (bpp - 1 - i)
    return result


def create_glyph(glyph: int = 299, colors=None) -> Image.Image:
    if colors is None:
        colors = [(81, 81, 89), (170, 170, 178)]
    font = open('6_0.bin', mode='rb')
    font.seek(0x10 + 64 * (glyph - 1))
    pixel_data = font.read(64)
    pixels = struct.unpack(f'<{len(pixel_data) // 2}H', pixel_data)
    argb_buf = bytearray(16 * 16 * 4)

    for y in range(16):
        for x in range(16):
            index = (x // 8 + (y // 8) * 2) * 8 + y % 8
            shift = (x % 8) * 2
            value = flip_bit_order((pixels[index] >> (14 - shift)) & 0x0003, 2) * 0x55

            buf_index = (y * 16 + x) * 4
            if value == 170:
                r, g, b, a = colors[0] + (255,)
            elif value == 85:
                r, g, b, a = colors[1] + (255,)
            else:
                r, g, b, a = 0, 0, 0, 0
            argb_buf[buf_index + 0] = r  # Blue
            argb_buf[buf_index + 1] = g  # Green
            argb_buf[buf_index + 2] = b  # Red
            argb_buf[buf_index + 3] = a  # Alpha
            # print(value)

    # Create PIL Image from ARGB buffer
    char_img = Image.frombytes('RGBA', (16, 16), bytes(argb_buf))
    font.close()
    return char_img


def paste_glyph_onto_image(bg=None, glyph: int = 299, colors=None, coords: tuple = (24, 24)):
    if colors is None:
        colors = [(81, 81, 89), (170, 170, 178)]
    # bg: Image.Image = Image.open(f'mails/{bg}.png').convert('RGBA')
    # second: Image.Image = Image.open(f'glyphs/g{glyph}.png').convert('RGBA')
    second: Image.Image = create_glyph(glyph, colors)

    bg.paste(second, coords, second)
    second.close()


def paste_text_onto_image(bg=None, text="ADVENTURE!\nEXCITED!", colors=None, line=0, orig_cords=(24, 24)):
    if colors is None:
        colors = [(81, 81, 89), (170, 170, 178)]
    o_x = orig_cords[0]
    o_y = orig_cords[1] + 40 * line
    x = o_x
    y = o_y
    for letter in text:
        if letter == '\n':
            x = o_x
            y += 16
            continue
        if letter not in characters.characters:
            ind = characters.characters_kor.index(letter) + 0x401
        else:
            ind = characters.characters.index(letter)
        paste_glyph_onto_image(bg, ind, colors, coords=(x, y))
        if letter == ' ':
            x += 4
        elif ind >= 0x401:
            x += 11
        else:
            x += characters.widths[ind]
    # bg.save("output.png")
    # bg.close()


# paste_text_onto_image()
