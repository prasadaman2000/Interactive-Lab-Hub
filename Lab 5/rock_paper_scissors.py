
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import time

import tensorflow
import numpy as np
import cv2
import abc
import enum

class RPS_Moves(enum.Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

    @staticmethod
    def eval_from_str(str):
        d = {"Rock": RPS_Moves.Rock, "Paper": RPS_Moves.Paper, "Scissors": RPS_Moves.Scissors}
        try:
            return d[str]
        except:
            return None

class Agent(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def next_move():
        pass

    @abc.abstractmethod
    def move_history():
        pass

class CameraAgent(Agent):
    def __init__(self):
        super().__init__()
        self.labels=[]
        f = open("./RPS_model/labels.txt", "r")
        for line in f.readlines():
            if(len(line)<1):
                continue
            self.labels.append(line.split(' ')[1].strip())
        
        self.model = tensorflow.keras.models.load_model('./RPS_model/keras_model.h5')
        self.cap = cv2.VideoCapture(0)
        if self.cap is None or not self.cap.isOpened():
            raise("No camera")
        self.history = []
        self.last_image = None

    def next_move(self):
        ret, img = self.cap.read()

        self.last_image = img.copy()

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        size = (224, 224)
        img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
        #turn the image into a numpy array
        image_array = np.asarray(img)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = self.model.predict(data)
        prediction_label = self.labels[np.argmax(prediction)]
        self.history.append(prediction_label)

        return RPS_Moves.eval_from_str(prediction_label)

    def move_history(self):
        return self.history

    def show_last_image(self):
        cv2.imshow("last_image", self.last_image)
        cv2.waitKey(2000)

class RandomAgent(Agent):
    def __init__(self):
        self.history = []

    def next_move(self):
        import random

        choice = random.choice([RPS_Moves.Rock, RPS_Moves.Paper, RPS_Moves.Scissors])
        self.history.append(choice)

        return choice

    def move_history(self):
        return self.history

class RPS_Game:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.score1 = 0
        self.score2 = 0


    def determine_winner(self, a_1_move, a_2_move):
        if a_1_move == a_2_move:
            return 0

        if a_1_move == None or a_2_move == None:
            return 0

        if a_1_move == RPS_Moves.Rock and a_2_move == RPS_Moves.Scissors:
            return 1
        
        if a_1_move == RPS_Moves.Rock and a_2_move == RPS_Moves.Paper:
            return -1

        if a_1_move == RPS_Moves.Scissors and a_2_move == RPS_Moves.Rock:
            return -1
        
        if a_1_move == RPS_Moves.Scissors and a_2_move == RPS_Moves.Paper:
            return 1

        if a_1_move == RPS_Moves.Paper and a_2_move == RPS_Moves.Rock:
            return 1

        if a_1_move == RPS_Moves.Paper and a_2_move == RPS_Moves.Scissors:
            return -1
    

    def next(self):
        move_1 = self.agent_1.next_move()
        move_2 = self.agent_2.next_move()

        return move_1, move_2

    def update_game(self, move_1, move_2):

        winner = self.determine_winner(move_1, move_2)

        if winner == 1:
            self.score1 += 1
        elif winner == -1:
            self.score2 += 1
        
        return (self.score1, self.score2)


if __name__ == "__main__":
    agent1 = CameraAgent()
    agent2 = RandomAgent()

    game = RPS_Game(agent1, agent2)

    while True:
        print("rock")
        time.sleep(2)
        print("paper")
        time.sleep(2)
        print("scissors")
        time.sleep(2)
        print("shoot! wait for score update")
        move_1, move_2 = game.next()
        print(f"you played {move_1} and your opponent played {move_2}")

        player_score, computer_score = game.update_game(move_1, move_2)

        print(f"score is now you: {player_score}, computer: {computer_score}")

