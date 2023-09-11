import pygame
import time
from settings import PLAYING, PAUSED, STOPPED, SCREEN_START


class Animation:
    def __init__(self, frames, loop=True):
        self._images = []
        self._durations = []
        self._start_times = None
        self._transformed_images = []

        self._state = STOPPED 
        self._loop = loop  
        self._rate = 1.0
        self._visibility = True  

        self._playing_start_time = 0 
        self._paused_start_time = 0 

        if frames != '_copy': 
            self.num_frames = len(frames)
            assert self.num_frames > 0, 'Must contain at least one frame.'
            for i in range(self.num_frames):
                frame = frames[i]
                assert type(frame) in (list, tuple) and len(frame) == 2, 'Frame {} has incorrect format.'.format(i)
                assert type(frame[0]) in (str, pygame.Surface), 'Frame {} image must be a string filename or a pygame. ' \
                                                                'Surface'.format(i)
                assert frame[1] > 0, 'Frame %s duration must be greater than zero.'.format(i)
                if type(frame[0]) == str:
                    frame = (pygame.image.load(frame[0]), frame[1])
                self._images.append(frame[0])
                self._durations.append((frame[1]))
            self._start_times = self._get_start_times()

    def _get_start_times(self):
        '''
        Get the start time based on the _durations list
        '''
        start_times = [0]
        for i in range(self.num_frames):
            start_times.append(start_times[-1] + self._durations[i])
        return start_times

    def reverse(self):
        '''
        Reverses the order of the animations.
        '''
        self.elapsed = self._start_times[-1] - self.elapsed
        self._images.reverse()
        self._transformed_images.reverse()
        self._durations.reverse()

    def get_copy(self):
        return self.getCopies(1)[0]

    def get_copies(self, num_copies=1):
        ret_val = []
        for i in range(num_copies):
            new_anim = Animation('_copy', loop=self.loop)
            new_anim._images = self._images[:]
            new_anim._transformed_images = self._transformed_images[:]
            new_anim._durations = self._durations[:]
            new_anim._start_times = self._start_times[:]
            new_anim.num_frames = self.num_frames
            ret_val.append(new_anim)
        return ret_val

    def blit(self, dest_surface, dest):
        '''
        Draws the corresponding frame of the animation at the specified location
        '''
        if self.is_finished():
            self.state = STOPPED
        if not self._visibility or self._state == STOPPED:
            return
        frame_num = find_start_time(self._start_times, self.elapsed)
        dest_surface.blit(self.get_frame(frame_num), dest)

    def get_frame(self, frame_num):
        if not self._transformed_images:
            return self._images[frame_num]
        else:
            return self._transformed_images[frame_num]
        
    def get_current_frame(self):
        return self.get_frame(self.current_frame_num)
    
    def clearTransforms(self):
        self._transformed_images = []

    def make_transforms_pernament(self):
        self._images = [pygame.Surface(surfObj.get_size(), 0, surfObj) for surfObj in self._transformed_images]
        for i in range(len(self._transformed_images)):
            self._images[i].blit(self._transformed_images[i], SCREEN_START)

    def blit_frame_num(self, frame_num, dest_surface, dest):
        '''
        Draws the specified frame of the animation object
        '''
        if self.is_finished():
            self.state = STOPPED
        if not self._visibility or self.state == STOPPED:
            return
        dest_surface.blit(self.get_frame(frame_num), dest)

    def blit_frame_at_time(self, elapsed, dest_surface, dest):
        '''
        Draws frames for already elapsed seconds
        '''
        if self.is_finished():
            self.state = STOPPED
        if not self._visibility or self.state == STOPPED:
            return
        frame_num = find_start_time(self._start_times, elapsed)
        dest_surface.blit(self.get_frame(frame_num), dest)

    def is_finished(self):
        return not self._loop and self.elapsed >= self._start_times[-1]

    def play(self, start_time=None):
        '''
        Start playing the animation
        '''

        if start_time is None:
            start_time = time.time()

        if self._state == PLAYING:
            if self.is_finished():

                self._playing_start_time = start_time
        elif self._state == STOPPED:
            self._playing_start_time = start_time
        elif self._state == PAUSED:
            self._playing_start_time = start_time - (self._paused_start_time - self._playing_start_time)
        self._state = PLAYING

    def pause(self, start_time=None):
        if start_time is None:
            start_time = time.time()

        if self._state == PAUSED:
            return 
        elif self._state == PLAYING:
            self._paused_start_time = start_time
        elif self._state == STOPPED:
            rightNow = time.time()
            self._playing_start_time = rightNow
            self._paused_start_time = rightNow
        self._state = PAUSED

    def stop(self):
        if self._state == STOPPED:
            return 
        self._state = STOPPED

    def _propSetElapsed(self, elapsed):
        '''
        Set the elapsed time to a specific value
        '''
        elapsed += 0.00001

        if self._loop:
            elapsed = elapsed % self._start_times[-1]
        else:
            elapsed = get_in_between_value(0, elapsed, self._start_times[-1])

        rightNow = time.time()
        self._playing_start_time = rightNow - (elapsed * self.rate)

        if self.state in (PAUSED, STOPPED):
            self.state = PAUSED 
            self._paused_start_time = rightNow

    def _propGetElapsed(self):
        if self._state == STOPPED:
            return 0

        if self._state == PLAYING:
            elapsed = (time.time() - self._playing_start_time) * self._rate
        elif self._state == PAUSED:
            elapsed = (self._paused_start_time - self._playing_start_time) * self._rate
        if self._loop:
            elapsed = elapsed % self._start_times[-1]
        else:
            elapsed = get_in_between_value(0, elapsed, self._start_times[-1])
        elapsed += 0.00001
        return elapsed

    elapsed = property(_propGetElapsed, _propSetElapsed)

def get_in_between_value(lowerBound, value, upperBound):
    if value < lowerBound:
        return lowerBound
    elif value > upperBound:
        return upperBound
    return value

def find_start_time(start_times,target):
    assert start_times[0] == 0
    lb = 0 
    ub = len(start_times) - 1

    if len(start_times) == 0:
        return 0
    if target >= start_times[-1]:
        return ub - 1

    while True:
        i = int((ub - lb) / 2) + lb

        if start_times[i] == target or (start_times[i] < target < start_times[i + 1]):
            if i == len(start_times):
                return i - 1
            else:
                return i

        if start_times[i] < target:
            lb = i
        elif start_times[i] > target:
            ub = i



