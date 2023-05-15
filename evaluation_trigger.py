from copy import deepcopy
from typing import List, Counter, Tuple

# EVENT_EXTRACTION_KEYS = ["trigger-P", "trigger-R", "trigger-F1", "role-P", "role-R", "role-F1"]
EVENT_EXTRACTION_KEYS = ["event-P", "event-R", "event-F1"]
EVENT_EXTRACTION_KEYS = ["trigger-P", "trigger-R", "trigger-F1"]


def event_list(filename):
    # creating the event_type list
    with open(filename, 'r', encoding='utf-8') as input_file:
        data = input_file.read().splitlines()
        all_events = []
        for line in enumerate(data):
            instance = line[1]
            # print(instance)
            count_eventtypes = instance.count("event_type")
            # print(count_eventtypes)
            event_types = []
            if count_eventtypes != 0:
                i = 0
                while i < count_eventtypes:
                    text = instance.split("'event_type': ")[i+1]
                    event = text.split("}")[0].replace("'", "")
                    if event not in event_types:
                        event_types.append(event)
                    i += 1
            else:
                event_types =[]
            # print(event_types)
            # print(100*"*")
            all_events.append(event_types)
    return all_events
def trigger_list(filename):
    # creating the triggers list
    with open(filename, 'r', encoding='utf-8') as input_file:
        data = input_file.read().splitlines()
        all_triggers = []
        for line in enumerate(data):
            instance = line[1]
            # print(instance)
            count_eventtypes = instance.count("event_type")
            # print(count_eventtypes)
            triggers = []
            if count_eventtypes != 0:
                i = 0
                while i < count_eventtypes:
                    text = instance.split("'trigger': ")[i+1]
                    trig = text.split(",")[0].replace("'", "")
                    if trig not in triggers:
                        triggers.append(trig)
                    i += 1
            else:
                triggers =[]
            # print(triggers)
            # print(100*"*")
            all_triggers.append(triggers)
    return all_triggers
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

    def count_instance(self, gold_list, pred_list, key):
        print("Gold:", gold_list)
        print(f"Pred_{key}:", pred_list)
        # self.gold_num += len(gold_list)
        # self.pred_num += len(pred_list)
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
        # dup_gold_list = deepcopy(gold_list)
        # for pred in pred_list:
        #     if pred in dup_gold_list:
        #         self.tp += 1
        #         dup_gold_list.remove(pred)



def main():
    pred_txt_filename = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/output/tgt_txt.json"
    pred_des_filename = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/output/tgt_des.json"
    gold_filename = "/Users/fshi0006/Desktop/Monash/workplace/blip/data/tgt_gt.json"
    for key in ["event", "trigger"]:
        if key == "event":
            function = event_list
        elif key == "trigger":
            function = trigger_list
        pred_txt_list = function(pred_txt_filename)
        pred_des_list = function(pred_des_filename)
        gold_list = function(gold_filename)

        print(30 * "*", f'{key} extraction results from Text only:', 40 * "*")
        txt_metric = Metric()
        txt_metric.count_instance(
            gold_list=gold_list,
            pred_list=pred_txt_list,
            key=key
        )
        txt_result = txt_metric.compute_f1(prefix='')
        print(f"text only {key} results:", txt_result)
        print('')
        # print(100 * "*")

        print(30 * "*", f'{key} extraction results from Text and Image Description:', 40 * "*")
        des_metric = Metric()
        des_metric.count_instance(
            gold_list=gold_list,
            pred_list=pred_des_list,
            key=key
        )
        des_result = des_metric.compute_f1(prefix='')
        print(f"text + Image Description {key} results:", des_result)
        print('')
        # print(100 * "*")

    # pred_event_txt_list = eventtype_list(pred_txt_filename)
    # pred_event_des_list = eventtype_list(pred_des_filename)
    # gold_event_list = eventtype_list(gold_filename)


    # txt_event_metric = Metric()
    # txt_event_metric.count_instance(
    #     gold_list=gold_event_list,
    #     pred_list=pred_event_txt_list
    # )
    # txt_event_result = txt_event_metric.compute_f1(prefix='')
    # print("text only results:", txt_event_result)


    # des_event_metric = Metric()
    # des_event_metric.count_instance(
    #     gold_list=gold_event_list,
    #     pred_list=pred_event_des_list
    # )
    # des_event_result = des_event_metric.compute_f1(prefix='')
    # print("text + Image Description results:", des_event_result)

if __name__ == "__main__":
    main()

