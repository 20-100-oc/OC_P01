import os
import random



def get_indicies(languages, nb_text_per_language, dataset_folder_path):
    
    texts_count = [0 for i in range(len(languages))]
    texts_indices = [[] for i in range(len(languages))]

    with open(os.path.join(dataset_folder_path, 'y_test.txt'), 'r') as f:
        y_test = f.read()
        y_test_list = y_test.split('\n')

    # get indices of all texts we want from x_test by using y_test
    # the texts are selected at random
    selected_indicies = {}

    for language in languages:
        selected_indicies[language] = []
        good_language_indicies = []

        # pick all indicies that belong to a specific language
        for i in range(len(y_test_list)):
            if y_test_list[i] == language:
                good_language_indicies.append(i)

        # choose at random in the one-language indicies
        for n in range(nb_text_per_language):
            index = random.choice(good_language_indicies)
            selected_indicies[language].append(index)
            good_language_indicies.remove(index)

    return selected_indicies




def get_texts_dict(languages, nb_text_per_language, dataset_folder_path):
    '''
    From the dataset folder:
    extracts some texts (from x_test) and the language they are written in (y_test).
    Then return these organized in a dict.
    '''

    selected_indicies = get_indicies(languages, nb_text_per_language, dataset_folder_path)

    # open with utf-8 unicode because foreign languages
    with open(os.path.join(dataset_folder_path, 'x_test.txt'), 'r', encoding='utf8') as f:
        x_test = f.read()
        x_test_list = x_test.split('\n')

    texts_dict = {}
    for i, language in enumerate(languages):
        texts_dict[language] = []
        for index in selected_indicies[language]:
            texts_dict[language].append(x_test_list[index])

    return texts_dict





if __name__ == '__main__':

    dataset_folder_path = 'G:\OpenClassrooms\projet 1\Dataset project 1 AI Engineer'
    languages = ['eng', 'fra', 'hin', 'spa', 'ara']
    nb_text_per_language = 3

    texts_dict = get_texts_dict(languages, nb_text_per_language, dataset_folder_path)

    
    for key in texts_dict:
        print(key)
        print(len(texts_dict[key]), '\n')
        for text in texts_dict[key]:
            try:
                print(text, '\n')
            except:
                print('CAN\'T PRINT')
        print('\n')
    

    total_chars = 0
    for key in texts_dict:
        for i in range(nb_text_per_language):
            total_chars += len(texts_dict[key][i])
    print('Total number of characters =', total_chars)
