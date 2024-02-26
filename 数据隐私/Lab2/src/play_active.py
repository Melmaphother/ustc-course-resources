from active import LinearActive
from dataset import Dataset
from paillier import Paillier
from comm import ActiveSocket
from transform import scale

if __name__ == "__main__":
    abs_path = "./cancer-active-train.csv"
    active_ip = "127.0.0.1"
    active_port = 9999

    trainset = Dataset.from_csv(has_label=True, abs_path=abs_path)
    scale(trainset)

    cryptosystem = Paillier()
    messenger = ActiveSocket(active_ip=active_ip, active_port=active_port).get_messenger()

    active_party = LinearActive(cryptosystem=cryptosystem, messenger=messenger)
    active_party.train(trainset)
