from random import randrange

def generate_protocol(sequence_number: int, subject_number: int, gesture_number: int):
    for subject in range(0, subject_number):
        for sequence_num in range(1, sequence_number):
            sequence = []
            random_gesture_count = randrange(0, gesture_number) # number of gestures to be done in 1 sequence
            for gesture_num in range(0, random_gesture_count):
                sequence.append(randrange(0, gesture_number) + 1) # creation of the sequence
            print(f"subject no. {subject + 1} : {sequence}")


if __name__ == "__main__":
    sequence_number = 12
    subject_number = 10
    gesture_number = 12

    generate_protocol(sequence_number, subject_number, gesture_number)
    print(f"number of sequences : {sequence_number * subject_number}")




