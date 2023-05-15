from copy import deepcopy
from typing import List, Counter, Tuple

# EVENT_EXTRACTION_KEYS = ["trigger-P", "trigger-R", "trigger-F1", "role-P", "role-R", "role-F1"]
EVENT_EXTRACTION_KEYS = ["role-P", "role-R", "role-F1"]
EVENT_EXTRACTION_KEYS = ["arg-P", "arg-R", "arg-F1"]

def role_list(filename, schema):
    # creating the event_type list
    event_list = list(schema.keys())
    # print(event_list)
    with open(filename, 'r', encoding='utf-8') as input_file:
        data = input_file.read().splitlines()
        all_roles = []
        for line in enumerate(data):
            instance = line[1]
            # print(100*"*")
            # print(instance)
            count_eventtypes = instance.count("event_type")
            # print(count_eventtypes)
            list_role_arg = []
            if count_eventtypes != 0:
                i = 0
                while i < count_eventtypes:
                    text = instance.split("'event_type':")[i+1]
                    event = text.split(",")[0].replace("'", "").replace(" ", "")
                    if event in event_list:
                        # print(event)
                        roles = schema[event]
                        # print(roles)
                        for r in roles:
                            if r in instance:
                                # print(r)
                                text_r = text.split(f"'{r}':")[1]
                                arg = text_r.split(",")[0].replace("}", "").replace("]", "")
                                if arg != '':
                                    arg = arg.replace("'", "")
                                role_arg = f"'{r}':" + f"'{arg}'"
                            else:
                                role_arg = f"'{r}':" + "''"
                            # print(role_arg)
                            list_role_arg.append(role_arg)
                    i += 1
            # print(list_role_arg)
            all_roles.append(list_role_arg)
    return all_roles

class Metric:
    def __init__(self):
        self.tp = 0.
        self.gold_num = 0.
        self.pred_num = 0.

    @staticmethod
    def safe_div(a, b):
        if b == 0.:
            return 0.
        else:
            return a / b

    def compute_f1(self, prefix=''):
        tp = self.tp
        pred_num = self.pred_num
        gold_num = self.gold_num
        p, r = self.safe_div(tp, pred_num), self.safe_div(tp, gold_num)
        return {prefix + 'tp': tp,
                prefix + 'gold': gold_num,
                prefix + 'pred': pred_num,
                prefix + 'P': p * 100,
                prefix + 'R': r * 100,
                prefix + 'F1': self.safe_div(2 * p * r, p + r) * 100
                }

    def count_instance(self, gold_list, pred_list):
        print("Gold:", gold_list)
        print("Pred:", pred_list)
        for g in range(len(gold_list)):
            dup_gold = deepcopy(gold_list[g])
            for j in range(len(dup_gold)):
                self.gold_num += 1
        for p in range(len(pred_list)):
            dup_pred = deepcopy(pred_list[p])
            for j in range(len(dup_pred)):
                self.pred_num += 1

        for item in range(len(gold_list)):
            dup_gold = deepcopy(gold_list[item])
            dup_pred = deepcopy(pred_list[item])
            for j in range(len(dup_pred)):
                if dup_pred[j] in dup_gold:
                    self.tp += 1


def main():
    schema = {"Life.Die": ["Agent", "Victim", "Instrument", "Place"],
              "Contact.Phone-Write": ["Entity", "Instrument", "Place"],
              "Movement.Transport": ["Agent", "Vehicle", "Destination", "Origin", "Artifact"],
              "Conflict.Attack": ["Instrument", "Target", "Place", "Attacker"],
              "Justice.Arrest-Jail": ["Agent", "Instrument", "Place", "Person"],
              "Transaction.Transfer-Money": ["Giver", "Recipient", "Money"],
              "Conflict.Demonstrate": ["Entity", "Police", "Instrument", "Place"],
              "Contact.Meet": ["Participant", "Place"]}
    pred_txt_filename = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/output/tgt_txt_full.json"
    pred_des_filename = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/output/tgt_des_full.json"
    gold_filename = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/full_tgt_gt.json"
    pred_txt_list = role_list(pred_txt_filename, schema)
    gold_list = role_list(gold_filename, schema)
    pred_des_list = role_list(pred_des_filename, schema)


    print(30 * "*", f'role-argument extraction results from Text only:', 40 * "*")
    txt_metric = Metric()
    txt_metric.count_instance(
        gold_list=gold_list,
        pred_list=pred_txt_list
    )
    txt_result = txt_metric.compute_f1(prefix='')
    print(f"text only role-argument results:", txt_result)
    print('')

        #
    print(30 * "*", f' role-argument extraction results from Text and Image Description:', 40 * "*")
    des_metric = Metric()
    des_metric.count_instance(
        gold_list=gold_list,
        pred_list=pred_des_list
    )
    des_result = des_metric.compute_f1(prefix='')
    print(f"text + Image Description role-argument results:", des_result)


if __name__ == "__main__":
    main()

