import json
import os


def get_statistic(some_dir):
    def list_from_txt(txt_file):
        answer = []
        with open(txt_file) as f:
            lines = f.readlines()
        for i in lines:
            if (len(i.split(' '))) == 9:
                answer += [i.split(' ')[8][0]]
        return answer

    def all_symb(file_dir):
        annotate = [os.path.join(file_dir, i) for i in sorted(os.listdir(file_dir)) if i.endswith('.txt')]
        all_symb = []
        for i in annotate:
            all_symb += list_from_txt(i)
        return all_symb

    def CountFrequency(my_list):
        count = {}
        for i in my_list:
            count[i] = count.get(i, 0) + 1
        return count

    all_symbols = all_symb(some_dir)
    statistic = CountFrequency(all_symbols)

    with open(os.path.join(some_dir, 'statistic.md'), 'w') as file:
        file.write(json.dumps(statistic))
