from OpenGL.GLU import gluLookAt


class glLibCamera:
    def __init__(self, pos, center, upvec=[0, 1, 0]):
        self.pos = pos
        self.targetpos = pos
        self.center = center
        self.targetcenter = center
        self.upvec = upvec
        self.targetupvec = upvec
        self.change_speed = 0.1

    def set_target_pos(self, new_target_pos):
        self.targetpos = new_target_pos

    def set_target_center(self, new_target_center):
        self.targetcenter = new_target_center

    def set_target_up_vector(self, new_target_up_vector):
        self.targetupvec = new_target_up_vector

    def set_change_speed(self, value):
        self.change_speed = value

    def update(self):
        pos_diff = [self.pos[0] - self.targetpos[0],
                    self.pos[1] - self.targetpos[1],
                    self.pos[2] - self.targetpos[2]]
        cen_diff = [self.center[0] - self.targetcenter[0],
                    self.center[1] - self.targetcenter[1],
                    self.center[2] - self.targetcenter[2]]
        upv_diff = [self.upvec[0] - self.targetupvec[0],
                    self.upvec[1] - self.targetupvec[1],
                    self.upvec[2] - self.targetupvec[2]]
        self.pos = [self.pos[0] - (pos_diff[0] * self.change_speed),
                    self.pos[1] - (pos_diff[1] * self.change_speed),
                    self.pos[2] - (pos_diff[2] * self.change_speed)]
        self.center = [self.center[0] - (cen_diff[0] * self.change_speed),
                       self.center[1] - (cen_diff[1] * self.change_speed),
                       self.center[2] - (cen_diff[2] * self.change_speed)]
        self.upvec = [self.upvec[0] - (upv_diff[0] * self.change_speed),
                      self.upvec[1] - (upv_diff[1] * self.change_speed),
                      self.upvec[2] - (upv_diff[2] * self.change_speed)]

    def set_camera(self):
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                  self.center[0], self.center[1], self.center[2],
                  self.upvec[0], self.upvec[1], self.upvec[2])
