from io import BytesIO

from PIL import Image
import bytereaders
import characters
import consts
import enums
import gamechecker
import text_handling


class SAV:
    def __init__(self, path):
        self.file_name = path
        self.data = open(path, 'rb').read()
        self.version = gamechecker.gameversionchecker(self.data)
        self.gen = self.get_generation(self.version)
        # self.lang = 2
        self.consts_offsets = consts.offsets[self.gen][self.version]
        self.lang = bytereaders.read8(self.data, self.consts_offsets['TRAINER_LANGUAGE'])
        self.block_offset = 0

        if self.gen == 4:
            self.current_block = self.get_current_block()
            self.block_offset = consts.sizes[4]['SIZE_2BLOCKS'] * self.current_block
        # self.started_date = bytereaders.read32(self.data,
        #                                        self.consts_offsets['STARTED_DATE'])
        # self.league_date = bytereaders.read32(self.data,
        #                                       self.block_offset + self.consts_offsets['LEAGUE_DATE'])
        self.player_name = characters.get_player_name(self.data,
                                                      self.block_offset + self.consts_offsets['TRAINER_NAME'],
                                                      self.gen)
        # self.gender = bytereaders.read8(self.data,
        #                                 self.block_offset + self.consts_offsets['TRAINER_GENDER'])
        self.player_id = bytereaders.read16(self.data,
                                            self.block_offset + self.consts_offsets['TRAINER_ID'])
        self.player_sid = bytereaders.read16(self.data,
                                             self.block_offset + self.consts_offsets['TRAINER_SID'])
        self.party_size = bytereaders.read32(self.data,
                                             self.block_offset + self.consts_offsets['PARTY_COUNT'])

    def get_generation(self, version):
        gens = {
            1:
                ['RB', 'G', 'Y'],
            2:
                ['GS', 'C'],
            3:
                ['RS', 'E', 'FRLF'],
            4:
                ['DP', 'Pt', 'HGSS'],
            5:
                ['BW', 'B2W2']
        }

        for gen in range(1, 10):
            if version in gens[gen]:
                return gen

    def get_current_block(self):
        if self.gen == 4:
            block1_savecount = bytereaders.read32(self.data, consts.sizes[4][self.version]['SIZE_SMALL'] - 16)
            block2_savecount = bytereaders.read32(self.data, consts.sizes[4][self.version]['SIZE_SMALL'] + 0x40000 - 16)
            return block1_savecount < block2_savecount

    def __repr__(self):
        nl = '\n'
        return f"{self.file_name}: This is a {self.gen}" \
               f"{'st' if self.gen == 1 else 'nd' if self.gen == 2 else 'rd' if self.gen == 3 else 'th'} generation " \
               f"{self.version} file of {self.player_name}, who started journey on " \
               f"{self.player_name}'s trainer ID is {self.player_id} and SID " \
               f"is {self.player_sid}\n" \
               f"{self.player_name} has {self.party_size} pokemon in party, them " \
               f"being:\n"

    def read_mail(self, ind: int):
        mail = MAIL(self.data[self.block_offset + self.consts_offsets['MAIL_OFFSET'] + ind * 0x38:self.block_offset +
                                                                                                  self.consts_offsets[
                                                                                                      'MAIL_OFFSET'] + ind * 0x38 + 0x38],
                    self.lang, self.version)
        return mail.export_image(ind)


class MAIL:
    def __init__(self, data, lang, version):
        self.data = data
        self.lang = lang
        self.version = version
        # self.TID = bytereaders.read16(self.data)
        # self.SID = bytereaders.read16(self.data, 2)
        self.gender = bytereaders.read8(self.data, 4)
        # male - 0 female - 1
        self.type = bytereaders.read8(self.data, 7)
        self.name = characters.get_player_name(self.data, 8, 4)
        self.messages = [
            [bytereaders.read16(self.data, 0x20 + mail_ind * 8), bytereaders.read16(self.data, 0x22 + mail_ind * 8),
             bytereaders.read16(self.data, 0x24 + mail_ind * 8), bytereaders.read16(self.data, 0x26 + mail_ind * 8)]
            for mail_ind in range(3)]
        self.mons = []
        for poke_ind in range(3):
            offs = 0x1C - 2 * poke_ind
            if bytereaders.read8(self.data, offs + 1) == 0x20:
                self.mons.append(bytereaders.read8(self.data, offs) - 7)
            elif bytereaders.read16(self.data, offs) == 0xffff:
                self.mons.append('idk')
            else:
                if self.version == "HGSS":
                   self.mons.append(bytereaders.read16(self.data, offs) - 7)
                elif self.version == 'DP' or self.version == 'Pt':
                    self.mons.append(bytereaders.read8(self.data, offs) - 7 + 256)
        self.actual_messages = self.convert_messages(self.messages)

    def convert_messages(self, messages: list, lang=None):
        if lang is None:
            lang = self.lang
        out = []
        for message in messages:
            if message[0] == 65535:
                out.append('')
            else:
                out.append(enums.messages[message[0]][message[1]][lang]
                           .replace("$", enums.words[message[2]][self.lang]
                           if "$" in enums.messages[message[0]][message[1]][lang] else '')
                           .replace("^", enums.words[message[3]][self.lang]
                           if "^" in enums.messages[message[0]][message[1]][lang] else ''))
        return out

    def export_image(self, ind):
        if self.type == 255:
            return False
        bg: Image.Image = Image.open(f'mails/{enums.mail_types[self.type]}.png').convert('RGBA')
        for k, phrase in enumerate(self.actual_messages):
            text_handling.paste_text_onto_image(bg, phrase, enums.mail_colors[self.type], line=k)
        text_handling.paste_text_onto_image(bg, self.name, enums.mail_colors[self.type], 0, (168, 161))
        x = 32
        for i in self.mons:
            if i == 'idk':
                x += 40
            else:
                icon: Image.Image = Image.open(f'sprites/{i:04d}.png').convert('RGBA')
                bg.paste(icon, (x, 144), icon)
                icon.close()
                x += 40
        buffer = BytesIO()
        bg.save(buffer, format="PNG")

        bg.close()
        return buffer
