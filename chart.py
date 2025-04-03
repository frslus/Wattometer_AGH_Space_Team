import pygame as pg
import datetime
import math


class Chart:
    def __init__(self, pos: (float, float), axis: (float, float), title, screen):
        self.CHART_COLOR = (200, 0, 0)
        self.AXIS_WIDTH = 2
        self.JOINT_SIZE = 4
        self.AXIS_COLOR = (255, 255, 255)
        self.AXIS_COLOR2 = (0, 255, 255)
        self.ARROW_WIDTH = 8
        self.ARROW_LENGTH = 10
        self.CHART_WIDTH = 2
        self.GRID_WIDTH = 1
        self.GRID_COLOR = (64, 64, 64)
        self.screen = screen
        self.pos = pos
        self.axis = axis
        self.axe_x = pg.Rect(pos[0] + self.AXIS_WIDTH, pos[1] + axis[1], axis[0], self.AXIS_WIDTH)
        self.axe_y = pg.Rect(pos[0], pos[1], self.AXIS_WIDTH, axis[1])
        delta_j = (self.JOINT_SIZE - self.AXIS_WIDTH) // 2
        self.joint = pg.Rect(pos[0] - delta_j, pos[1] + axis[1] - delta_j, self.JOINT_SIZE, self.JOINT_SIZE)
        delta_ax1 = self.AXIS_WIDTH + self.axis[0]
        delta_ax2 = self.axis[1] + (self.AXIS_WIDTH // 2) - (self.ARROW_WIDTH // 2)
        delta_ax3 = self.axis[1] + (self.AXIS_WIDTH // 2) + (self.ARROW_WIDTH // 2)
        delta_ax4 = self.axis[1] + (self.AXIS_WIDTH // 2)
        self.arrow_x = [(pos[0] + delta_ax1, pos[1] + delta_ax2),
                        (pos[0] + delta_ax1, pos[1] + delta_ax3),
                        (pos[0] + delta_ax1 + self.ARROW_LENGTH, pos[1] + delta_ax4)]
        delta_ay1 = (self.ARROW_WIDTH // 2) - (self.AXIS_WIDTH // 2)
        delta_ay2 = (self.ARROW_WIDTH // 2) + (self.AXIS_WIDTH // 2)
        self.arrow_y = [(pos[0] - delta_ay1, pos[1]),
                        (pos[0] + delta_ay2, pos[1]),
                        (pos[0] + (self.AXIS_WIDTH // 2), pos[1] - self.ARROW_LENGTH)]
        self.grid_x = [
            (pos[0] + self.axis[0] * (1 / 3), pos[1], pos[0] + self.axis[0] * (1 / 3), pos[1] + self.axis[1]),
            (pos[0] + self.axis[0] * (2 / 3), pos[1], pos[0] + self.axis[0] * (2 / 3), pos[1] + self.axis[1])]
        self.grid_y = []
        self.start_time = self.microtime(datetime.datetime.today())
        self.timespan = 30000000  # μs - TU MOŻNA WPISAĆ CZAS NA OSI X
        self.value_span = (0, 100)
        self.data = []
        self.min_data = None
        self.max_data = None
        self.labels_x = [0, (self.timespan / 3) / 1000000, 2 * (self.timespan / 3) / 1000000, self.timespan / 1000000]
        self.labels_y = []
        self.x_unit = None
        self.y_unit = None
        self.font_small = pg.font.Font(None, 20)
        self.font_medium = pg.font.Font(None, 25)
        self.font_large = pg.font.Font(None, 30)
        self.title = title

    @staticmethod
    def microtime(date):
        date_str = str(date)
        hour = int(date_str[11:13])
        minute = int(date_str[14:16])
        second = int(date_str[17:19])
        microsecond = int(date_str[20:])
        microtime = hour * (60 * 60 * 1000000) + minute * (60 * 1000000) + second * 1000000 + microsecond
        return microtime

    def datapoint_pos(self, it):
        pos_x = self.pos[0] + self.axis[0] * (self.data[it][0] - self.start_time) / self.timespan
        pos_y = self.pos[1] + self.axis[1] - self.axis[1] * (self.data[it][1] - self.value_span[0]) / (
                self.value_span[1] - self.value_span[0])
        return pos_x, pos_y

    def draw(self):
        for line in self.grid_x:
            pg.draw.line(self.screen, self.GRID_COLOR, (line[0], line[1]), (line[2], line[3]), self.GRID_WIDTH)
        for line in self.grid_y:
            pg.draw.line(self.screen, self.GRID_COLOR, (line[0], line[1]), (line[2], line[3]), self.GRID_WIDTH)
        for it in range(1, len(self.data)):
            pg.draw.line(self.screen, self.CHART_COLOR, self.datapoint_pos(it - 1), self.datapoint_pos(it),
                         self.CHART_WIDTH)
        pg.draw.rect(self.screen, self.AXIS_COLOR, self.axe_x)
        pg.draw.rect(self.screen, self.AXIS_COLOR, self.axe_y)
        pg.draw.rect(self.screen, self.AXIS_COLOR, self.joint)
        pg.draw.polygon(self.screen, self.AXIS_COLOR, self.arrow_y)
        pg.draw.polygon(self.screen, self.AXIS_COLOR, self.arrow_x)
        for label in self.labels_x:
            text = self.font_small.render(f"{label:.2f}", True, "white")
            text_block = text.get_rect()
            text_block.center = (
            self.pos[0] + self.axis[0] * label * 1000000 / self.timespan, self.pos[1] + self.axis[1] + 15)
            self.screen.blit(text, text_block)
        for label in self.labels_y:
            text = self.font_small.render(f"{label:.2f}", True, "white")
            text_block = text.get_rect()
            text_block.center = (self.pos[0] - 25,
                                 self.pos[1] + self.axis[1] - self.axis[1] * (label - self.value_span[0]) /
                                 (self.value_span[1] - self.value_span[0]))
            self.screen.blit(text, text_block)
        text = self.font_large.render(self.title, True, "white")
        text_block = text.get_rect()
        text_block.center = (self.pos[0] + self.axis[0] // 2, self.pos[1] - 15)
        self.screen.blit(text, text_block)
        if self.x_unit is not None:
            text = self.font_medium.render(self.x_unit, True, "white")
            text_block = text.get_rect()
            text_block.center = (self.pos[0] + self.axis[0] + 25 + len(self.x_unit), self.pos[1] + self.axis[1])
            self.screen.blit(text, text_block)
        if self.y_unit is not None:
            text = self.font_medium.render(self.y_unit, True, "white")
            text_block = text.get_rect()
            text_block.center = (self.pos[0], self.pos[1] - 25)
            self.screen.blit(text, text_block)

    def feed(self, data):
        self.data.append((self.microtime(datetime.datetime.today()), data))
        self.update_axis_span()

    def update_axis_span(self):
        if len(self.data) > 0:
            if self.data[-1][0] - self.start_time > self.timespan:
                self.start_time = self.data[-1][0] - self.timespan
            i = 0
            while self.data[i][0] < self.start_time:
                i += 1
            self.data = self.data[i:]
            self.min_data = min([self.data[i][1] for i in range(len(self.data))])
            self.max_data = max([self.data[i][1] for i in range(len(self.data))])
        if self.min_data != self.max_data:
            delta = self.max_data - self.min_data
            self.value_span = (self.min_data - 0.1 * delta, self.max_data + 0.1 * delta)
        else:
            if self.min_data is None:
                self.value_span = (-1, 1)
            else:
                self.value_span = (self.min_data - 1, self.min_data + 1)
        cell = int(math.log(self.value_span[1] - self.value_span[0], 10)) + 1
        grid_span = int(10 ** cell)
        grid_lines = (self.value_span[1] - self.value_span[0]) // grid_span
        while grid_lines < 3:
            grid_span /= 2
            grid_lines = (self.value_span[1] - self.value_span[0]) // grid_span
            if grid_lines >= 3:
                break
            grid_span /= 2
            grid_lines = (self.value_span[1] - self.value_span[0]) // grid_span
            if grid_lines >= 3:
                break
            grid_span /= 5
            grid_lines = (self.value_span[1] - self.value_span[0]) // grid_span
        grid_pos = 0
        self.grid_y = []
        self.labels_y = []
        while grid_pos > self.value_span[0]:
            grid_pos -= grid_span
        while grid_pos < self.value_span[1]:
            if self.value_span[0] < grid_pos:
                self.grid_y.append((self.pos[0],
                                    self.pos[1] + self.axis[1] - self.axis[1] * (grid_pos - self.value_span[0]) /
                                    (self.value_span[1] - self.value_span[0]),
                                    self.pos[0] + self.axis[0],
                                    self.pos[1] + self.axis[1] - self.axis[1] * (grid_pos - self.value_span[0]) /
                                    (self.value_span[1] - self.value_span[0])))
                self.labels_y.append(grid_pos)
            grid_pos += grid_span

    def reset(self):
        self.data = []
        self.min_data = None
        self.max_data = None
        self.start_time = self.microtime(datetime.datetime.today())
        self.update_axis_span()
