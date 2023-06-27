from random import randrange
from PIL import Image
import os

def generate_protocol(sequence_number: int, subject_number: int, gesture_number: int):
    gestures = {
        1: "up_down",
        2: "right_left",
        3: "circle_right",
        4: "circle_left",
        5: "v_right",
        6: "v_left",
        7: "m_left",
        8: "m_right",
        9: "s_left",
        10: "s_right",
        11: "tide_left",
        12: "tide_right"
    }
    
    for subject in range(subject_number):
        for sequence_num in range(sequence_number):
            sequence = []
            random_gesture_count = randrange(1, gesture_number)  # number of gestures to be done in 1 sequence
            for gesture_num in range(random_gesture_count):
                sequence.append(randrange(1, gesture_number + 1))  # creation of the sequence

            image_width = 100
            image_height = 100
            sequence_image = Image.new('RGB', (image_width * random_gesture_count, image_height))

            for index, gesture in enumerate(sequence):
                gesture_name = gestures[gesture]
                gesture_image_path = f"images/{gesture_name}.png"  # replace with the actual path
                gesture_image = Image.open(gesture_image_path)

                gesture_image = gesture_image.resize((image_width, image_height))
                sequence_image.paste(gesture_image, (index * image_width, 0))

            sequence_image_path = f"../images_saved/sequences/subject{subject + 1}_sequence{sequence_num + 1}.png"
            os.makedirs(os.path.dirname(sequence_image_path), exist_ok=True)
            sequence_image.save(sequence_image_path)

            print(f"Subject no. {subject + 1} - Sequence {sequence_num + 1}: {sequence}")


if __name__ == "__main__":
    sequence_number = 20
    subject_number = 2
    gesture_number = 12

    generate_protocol(sequence_number, subject_number, gesture_number)
    print(f"Number of sequences: {sequence_number * subject_number}")
