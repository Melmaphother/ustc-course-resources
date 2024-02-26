from dataset import Dataset
from paillier import Paillier
from passive import LinearPassive
from comm import PassiveSocket
from transform import scale

if __name__ == "__main__":
    abs_path = "./cancer-passive-train.csv"
    active_ip = "127.0.0.1"
    active_port = 9999

    trainset = Dataset.from_csv(has_label=False, abs_path=abs_path)
    scale(trainset)

    cryptosystem = Paillier()
    messenger = PassiveSocket(active_ip=active_ip, active_port=active_port).get_messenger()

    active_party = LinearPassive(messenger=messenger)
    active_party.train(trainset)
