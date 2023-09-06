# Return a confusion matrix (numpy array) for the language 
# detection model from azure cognitive services
# and diplay an image of it
# (can save the image of the matrix).
#
# On the matrix graph:
# the languages on the left are the true languages
# the ones on the bottom are the guesses from the model

import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from get_texts_for_confusion_matrix import get_texts_dict
from interact_with_azure_api import guess_language



def graph_conf_matrix(conf_matrix, graph_save_path):
    
    norm_conf = []
    for i in conf_matrix:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j)/float(a))
        norm_conf.append(tmp_arr)
    
    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)

    ax.set_xlabel('Prediction')
    ax.set_ylabel('Label')

    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.Reds, 
                    interpolation='nearest')
    
    width, height = conf_matrix.shape
    
    for x in range(width):
        for y in range(height):
            ax.annotate(str(conf_matrix[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')
    
    cb = fig.colorbar(res)
    plt.xticks(range(width), languages[:width])
    plt.yticks(range(height), languages[:height])

    now = datetime.now()
    current_time = now.strftime('%H-%M-%S')

    if graph_save_path != None:
        save_str = os.path.join(graph_save_path, f'confusion_matrix_{current_time}.png')
        plt.savefig(save_str)
    plt.show()




def confusion_matrix(languages, nb_text_per_language, dataset_folder, 
                     api_key, labels_path, graph_save_path=None):   

    texts_dict = get_texts_dict(languages, nb_text_per_language, dataset_folder)
    conf_matrix = np.zeros((len(languages), len(languages)), dtype='int')

    for i, language in enumerate(languages):
        guesses = guess_language(texts_dict[language], api_key, labels_path)
        
        for guess in guesses:
            guess_index = languages.index(guess)
            conf_matrix[i, guess_index] += 1


    graph_conf_matrix(conf_matrix, graph_save_path)
    
    return conf_matrix




if __name__ == '__main__':

    api_key = input('Enter API access key:\n')

    labels_path = 'G:\OpenClassrooms\projet 1\P1_marzo_vincent\P1_01_scripts\Dataset project 1 AI Engineer\labels.csv'
    dataset_folder = 'G:\OpenClassrooms\projet 1\P1_marzo_vincent\P1_01_scripts\Dataset project 1 AI Engineer'

    languages = ['eng', 'fra', 'spa', 'por', 'hin']
    nb_text_per_language = 25

    conf_matrix = confusion_matrix(languages, nb_text_per_language, dataset_folder, 
                                   api_key, labels_path, graph_save_path='matrix graphs')    

    print(conf_matrix)
