import utils.file_utils as file_utils

from sequence_gesture import SequenceGesture

if __name__ == "__main__":
    seq1:SequenceGesture = file_utils.get_gesture_file_content("data/our_datas/new/processed/seq13.csv")
    seq1.shift_timestamp()
    seq1.init_norms()
    seq1.build_angles()
    seq1.compensate_gravity()
    seq1.init_norms()
    #seq1.moyenne_acc()
    #seq1.plot()
